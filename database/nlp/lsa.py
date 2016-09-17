#!/usr/bin/env python 2
"""Perform LSA analysis on spreadsheet, find clusters of comments and name them"""

from gensim import corpora, models, similarities, matutils
from sklearn import metrics
import numpy as np
#import igraph
from scipy.spatial.distance import cosine, euclidean
from scipy.linalg import norm
import csv
import json, ujson
import xlrd
import re
import os
import sys
import xlwt
import math
import utilities as utils
import pickle
import redis

# Debug Settings
np.seterr(all='raise')

# so cluster results are repeatable
RSEED = 5

DEFAULT_NUMTOPICS=15
DEFAULT_CLUSTER_METHOD= ""
DEFAULT_LSI_MODEL="wiki"
DEFAULT_EPS=0.2
DEFAULT_MINSAMPLES=25
DEFAULT_NUMCLUSTERS=30
COSINE_THRESHOLDS = [55,65,70,80,90]
COSINE_CUTOFF = 0.55 # Default Value
BLOCK_SIZE = 10000
AVG_CLUSTER_SIZE = 40
USE_DEFAULT_THRESHOLD = True

THISDIR = os.path.dirname(os.path.realpath(__file__))

def safe_cosine(v1, v2):
    """larger numbers are closer together"""
    if (norm(v1)==0) | (norm(v2)==0):
        return 0.0
    dist = 1-cosine(v1, v2)
    if math.isnan(dist):
        return 0.0
    return dist

def safe_cosine_distance(v1, v2):
    """smaller numbers mean they are closer together"""
    cos = cosine(v1, v2)
    if math.isnan(cos):
        return 2
    return cos

def get_phrases(text):
    return re.split("[\.\?\!\,\"\;\:]", text)

def load_wikipedia_model():
    print "loading wikipedia dictionary and model..."
    dictionary = pickle.load(open(os.path.join(THISDIR, "lsi-models/wiki_en_dict.pickle")))
    lsi = pickle.load(open(os.path.join(THISDIR, "lsi-models/wiki_en_lsi_200.pickle")))
    return dictionary, lsi

def load_amazon_model():
    print "loading amazon review dictionary and model..."
    dictionary = pickle.load(open(os.path.join(THISDIR, "lsi-models/amazon_dict.pickle")))
    lsi = pickle.load(open(os.path.join(THISDIR, "lsi-models/amazon_lsi_200.pickle")))
    return dictionary, lsi

def load_twitter_model(self):
    print "loading twitter dictionary and model..."
    dictionary = pickle.load(open(os.path.join(THISDIR, "lsi-models/twitter_dict_nosw_.pickle")))
    lsi = pickle.load(open(os.path.join(THISDIR, "lsi-models/twitter_lsi_200_nosw_.pickle")))
    return dictionary, lsi

STATUS_MESSAGE = "Analyzing Text..."

class CommentCluster:

    def __init__(self, original_rows, headers, textcol, dictionary=None, lsi=None, model=None):
        '''

        :param original_rows: list of text extracted from a csv, where each list item is a Datable Candidate's answer.
        :param headers: Labels for each row of the original csv
        :param textcol: 0 index of the column in "original_rows" with the text for analysis by this program
        :param dictionary:
        :param lsi:
        :param model:
        :return:
        '''

        # prepare rows for lsi analysis and clustering
        self.original_rows = original_rows
        # self.headers = headers # Shouldn't need this in the long run.
        # self.textcol = textcol
        if dictionary != None and lsi != None:
            self.set_model(dictionary, lsi)
        elif model == "wiki" or model == None:
            self.load_wikipedia_model()
        elif model == "amazon":
            self.load_amazon_model()
        elif model =="twitter":
            self.load_twitter_model()
        # if model == "self":
        #     self.create_lsi_model()

    def prepare_documents(self):
        self.get_documents_from_rows()
        self.prepare_word_list()
        self.create_input_matrix()

    def load_wikipedia_model(self):
        self.dictionary, self.lsi = load_wikipedia_model()

    def load_amazon_model(self):
        self.dictionary, self.lsi = load_amazon_model()

    def load_twitter_model(self):
        self.dictionary, self.lsi = load_twitter_model()

    def set_model(self, dictionary, lsi):
        self.dictionary = dictionary
        self.lsi = lsi

    def get_documents_from_rows(self):
        self.documents = [utils.sanitize(row[self.textcol]) for row in self.original_rows]
        print "Number of documents: %i" % len(self.documents)

    def find_words_used_once(self, texts):
        """Find words that appear only once"""
        all_tokens = sorted(sum(texts, []))
        tokens_once = []
        count = 0
        prev = None
        for t in all_tokens:
            count += 1
            if t != prev:
                if count == 1 and prev != None:
                    tokens_once.append(t)
                count = 0
            prev = t
        return tokens_once


    def prepare_word_list(self):
        """Create words lists from documents"""
        print "pre-processing text..."
        self.texts = [[word.lower() for word in utils.tokenize(document) if word not in utils.SW] for document in self.documents]
        self.word_counts = [float(len(text)) for text in self.texts]

    def create_input_matrix(self):
        """Create the corpus matrix"""
        print "preparing matrix for lsa..."
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]

    def create_lsi_model(self, numtopics):
        """Create LSI Model from rows"""
        print "creating dictionary..."
        self.dictionary = corpora.Dictionary(self.texts)
        print "performing lsa..."
        self.lsi = models.lsimodel.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=numtopics)


    def calculate_lsi_transformed_corpus_matrix(self):
        """Find the documents represented as vectors in LSI space"""
        self.transformed = matutils.corpus2dense(self.lsi[self.corpus_tfidf], len(self.lsi.projection.s)).T
        # normalize the vectors because only the vector orientation represents semantics
        transformed_norms = np.sum(self.transformed**2,axis=-1)**(1./2)
        # avoid dividing by zero
        transformed_norms[ transformed_norms==0] = 1
        self.transformed = self.transformed / transformed_norms.reshape(len(transformed_norms),1)

    def calculate_cosine_matrix(self):
        """Compute the cosine matrix for the transformed document vectors. This method is fast but uses much memory."""
        # self.transformed is normalized, so we can speed up calculations by skipping that step
        return self.transformed.dot(self.transformed.T)

    def calculate_sparse_cosine_matrix(self, cosine_cutoff=COSINE_CUTOFF):
        # This method is slower but uses far less memory.
        # use blocks for speed and sparsify output for memory efficiency
        num_blocks = max(1, int(round(float(len(self.transformed)) / BLOCK_SIZE)))
        num_rows = int(len(self.transformed) / num_blocks)
        splits = [[x, x*num_rows, (x+1)*num_rows] for x in range(num_blocks)]
        splits[-1][2] = len(self.transformed) # make sure we reach the end
        cosine_matrix = [[] for x in range(len(self.transformed))]
        for split1, begin1, end1 in splits:
            for split2, begin2, end2 in splits[:split1+1]:
                part = self.transformed[begin1:end1].dot(self.transformed[begin2:end2].T)
                for n, row in zip(range(begin1, end1), part):
                    above_cutoff = np.where(row >= cosine_cutoff)[0] # Was using global COSINE_CUTOFF
                    cosine_matrix[n].extend([(w+begin2, row[w]) for w in above_cutoff if w+begin2 < n])
        return cosine_matrix


    def calculate_cosine_distance_matrix(self):
        """Compute the cosine distance matrix for the transformed document vectors"""
        #numdocs = len(self.transformed)
        cosine_matrix = self.calculate_cosine_matrix()
        return 1 - cosine_matrix

    def get_total_tfidf(self, ngram, idx):
        parts = [x[0] for x in self.dictionary.doc2bow(ngram.split(" "))]
        total = 0
        for part in parts:
            try:
                total += self.cluster_corpus_tfidf_map[idx][part]
            except KeyError:
                pass
        return total

    def write_data_tables_json(self, outfilepath):
        """Write metrics and clusters to a json file"""
        utils.write_data_tables_json(self.original_rows, self.headers)

    def analyze(self, numtopics=DEFAULT_NUMTOPICS, cluster_method=DEFAULT_CLUSTER_METHOD, eps=DEFAULT_EPS, min_samples=DEFAULT_MINSAMPLES, num_clusters=DEFAULT_NUMCLUSTERS):
        self.prepare_documents()
        if len(self.documents) > 0:
            self.calculate_lsi_transformed_corpus_matrix()
            cosine_cutoff = self.threshold_cosine_optimally()
            self.do_cluster_analysis(method=cluster_method, eps=eps, min_samples=min_samples, num_clusters=num_clusters)


if __name__ == '__main__':

    filename = sys.argv[1]
    textcol = int(sys.argv[2])
    output = sys.argv[3]

    headers, rows = utils.get_spreadsheet_rows(filename, textcol)
    cc = CommentCluster(rows, headers, textcol, model="wiki")
    cc.analyze()
    cc.write_clusters_to_workbook(output+".xls")
    #cc.write_cluster_stats("cluster_stats.csv")
    #cc.write_force_graph_json(output+".json")

    for name, values in cc.sorted_clusters.items():
        print name, len(values)

    # print "Silhoutte score: ", cc.calculate_silhouette_score()
    # centralities = [x[-1] for rows in cc.sorted_clusters.values() for x in rows]

    # import matplotlib.pyplot as plt
    # fig1 = plt.figure()
    # ax = fig1.add_subplot(111)
    # n, bins, patches = ax.hist(centralities, 50, normed=False)
    # plt.savefig("plots/centrality_histogram.png")
    # plt.show()
