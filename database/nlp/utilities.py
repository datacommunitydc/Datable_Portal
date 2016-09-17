#!/usr/bin/env python 2

import os
import sys
import bleach
import csv
import _csv
import xlrd
import xlwt
import re
import magic
import ujson
import redis
import codecs
import numpy as np
from time import time

#WORD = re.compile("[\w\-]+\'[a-z]+|[A-Za-z]+\'[\w\-]+|[\w\-]+")
WORD = re.compile("(([A-Za-z]\.)+)|([0-9]{1,2}:[0-9][0-9])|(([A-za-z]+\'){0,1}\w+(\-\w+){0,1}(\'[a-z]+){0,1})")
EMAIL_OR_URL = re.compile("(\w|-)+@(\w|-)+\.(\w|-)+|http.+")

thisdir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(thisdir,"stopwords.txt")) as handle:
    SW = [x[:-1] for x in handle.readlines()]

with open(os.path.join(thisdir,"prepositions.txt")) as handle:
    PREPS = [x[:-1] for x in handle.readlines()]

csv.field_size_limit(sys.maxsize)

# Copied from http://stackoverflow.com/questions/9177820/python-utf-16-csv-reader
# Needed by the csv reader if the file is not utf-8 or ascii
class Recoder(object):
    def __init__(self, stream, decoder, encoder, eol='\r\n'):
        self._stream = stream
        self._decoder = decoder if isinstance(decoder, codecs.IncrementalDecoder) else codecs.getincrementaldecoder(decoder)(errors='replace')
        self._encoder = encoder if isinstance(encoder, codecs.IncrementalEncoder) else codecs.getincrementalencoder(encoder)()
        self._buf = ''
        self._eol = eol
        self._reachedEof = False

    def read(self, size=None):
        if size is None:
            r = self._stream.read()
        else:
            r = self._stream.read(size)
        raw = self._decoder.decode(r, size is None)
        return self._encoder.encode(raw)

    def __iter__(self):
        return self

    def __next__(self):
        if self._reachedEof:
            raise StopIteration()
        while True:
            line,eol,rest = self._buf.partition(self._eol)
            if eol == self._eol:
                self._buf = rest
                return self._encoder.encode(line + eol)
            raw = self._stream.read(1024)
            if raw == '':
                self._decoder.decode(b'', True)
                self._reachedEof = True
                return self._encoder.encode(self._buf)
            self._buf += self._decoder.decode(raw)
    next = __next__

    def close(self):
        return self._stream.close()

# helper functions
def sanitize(element):
    """Remove links and email addresses from a string"""
    element = bleach.clean(element)
    if not (isinstance(element, str) or isinstance(element, unicode)):
        element = str(element)
    return re.sub(EMAIL_OR_URL, "", element).strip()

def get_mime_type(inf):
    return magic.from_file(inf, mime=True)

def get_encoding(buf):
    if len(buf) > 0:
        m = magic.Magic(mime_encoding=True)
        encoding = m.from_buffer(buf)
        if encoding == "binary":
            raise Error("Unexpected character encoding. Please provide text in a standard encoding.")
        try:
            buf[:100].decode(encoding)
        except LookupError:
            print "Warning, unable to lookup decoder for %s, using default: utf-8" % encoding
            return "utf-8"
        print "Detected %s encoding..." % encoding
        return encoding
    return "utf-8"

def encode_if_necessary(element, force_text=False):
    """Encode unicode as utf-8 if it is a string or unicode object, otherwise, convert strings that are numbers"""
    if not force_text:
        if isinstance(element, int) or isinstance(element, float):
            return element
        try:
            return int(element)
        except ValueError:
            pass
        try:
            value = float(element)
            # don't return nan because we can't json encode it.
            if not np.isnan(value):
                return value
        except ValueError:
            pass
    if isinstance(element,unicode):
        return element.encode("utf-8", errors="ignore")
    return element

def decode_if_necessary(element, encoding):
    if isinstance(element, str):
        return element.decode(encoding, "ignore")
    return element

def tokenize(text):
    for match in WORD.finditer(text):
        yield match.group()

def ngrams(tokens, n):
    # filter ngrams to not contain repeating words and not end with prepositions
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-(n-1)) if len(set(tokens[i:i+n])) == n and tokens[i+n-1] not in PREPS]

def bigrams(tokens):
    return ngrams(tokens, 2)

def trigrams(tokens):
    return ngrams(tokens, 3)

def quadgrams(tokens):
    return ngrams(tokens, 4)

def get_plain_text_rows(filepath):
    print "Splitting plain text..."
    header = ["Text"]
    text = open(filepath, 'rbU').read(512)
    encoding = get_encoding(text)
    rows = [[x.strip().decode(encoding, "ignore")] for x in text.split("\n\n")]
    return header, rows
