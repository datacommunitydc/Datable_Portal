from math import *
import numpy as np


'''
create similarity matrix between all candidates
    Whos most like each other?
        n*n matrix, n = each candidates. [0,1]
        Score off of questions in DB
        % same 100, and not at all = 0%
        “Root sum sq” for composites 
        start work on similarity matrix on all well-structured questions(fields)
            Start w simple yes/no questions, then advance
        Use numpy for lin. Alg.

References:
[1] https://en.wikipedia.org/wiki/Cosine_similarity
[2] http://bioinformatics.oxfordjournals.org/content/22/18/2298.full
[3] https://en.wikipedia.org/wiki/Euclidean_distance
[4] https://www.mathworks.com/matlabcentral/answers/293532-how-to-calculate-normalized-euclidean-distance-on-two-vectors?requestedDomain=www.mathworks.com
[5] http://www.econ.upf.edu/~michael/stanford/maeb4.pdf

'''
print "=============\n"


# 1. import MongoDB as pandas df, to process with numpy.
def importMongoDB():
    '''
    -> pull data from mongodb to python for analysis.
    “Pymongo” lib
        Check old work from Udacity course
    “Monary” lib
        https://monary.readthedocs.io/index.html
        Types https://monary.readthedocs.io/reference.html?highlight=type
        https://www.youtube.com/watch?v=oteFpXIKBYg
        https://monary.readthedocs.io/examples/string.html 
        https://monary.readthedocs.io/installation.html 
    http://alexgaudio.com/2012/07/07/monarymongopandas.html 
    https://docs.mongodb.com/getting-started/python/insert/
    http://stackoverflow.com/questions/17805304/how-can-i-load-data-from-mongodb-collection-into-pandas-dataframe?noredirect=1&lq=1
    http://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas?noredirect=1&lq=1
    http://djcinnovations.com/index.php/archives/164
    http://djcinnovations.com/index.php/archives/103
    '''


# 2. generate sensitivity matrix

# 2.1. get 2 candidates

# 2.2. get similarity between 2 candidates
    '''
    Measures of similarity between two vectors
        Euclidean distance
        1-norm
        ∞-norm
        => Cosine measure (most widely used in lit.)
        Gabriel graph
        A measure derived from a consensus matrix
        Other ideas: Delaunay triangulation, Hamming distance or variation
    '''
vector_1 = [True,True,False,True,False]
vector_2 = [True,True,False,True,False]
vector_3 = [True,False,False,False,False]
vector_4 = [False,False,False,False,False]
vector_5 = [True,True,True,True,True]
vector_6 = [False,False,True,False,True] #opposite of vector_1

num_questions = len(vector_1)
all_yes = np.array([1]*num_questions)
all_no  = np.array([0]*num_questions)
MAX_DIFF = np.sqrt( np.sum(np.square( all_yes-all_no )) )

def compute_sumSq(v1, v2):
    if len(v1) == len(v2):
        sumSq_AB = 0
        sumSq_AA = 0
        sumSq_BB = 0
        for i in range(0, len(v1)):
            sumSq = sumSq + (1.0 - (v1[i] - v2[i])**2) / len(v1)
        print "Root sum sq similarity: ", sqrt(sumSq)
    else:
        print "Error: Input vectors of different lengths."

def method_0_SimpleDiffSimilarity(v1, v2):
    if len(v1) == len(v2):        
        print "Simple diff similarity: ", np.sum( (np.ones(len(v1)) - abs(np.array(v1)-np.array(v2))) / float(len(v1)) )
    else:
        print "Error: Input vectors of different lengths."

def method_1_RootSumSqSimilarity(v1, v2):
    '''
    similar to Euclidean distance, just adjusting for 0 values.
    
    [3]
    '''
    if len(v1) == len(v2):
        sumSq = 0
        for i in range(0, len(v1)):
            #sumSq = sumSq + (v1[i] - v2[i])**2 #round 0: goes the wrong way.
            sumSq = sumSq + (1.0 - (v1[i] - v2[i])**2) / len(v1)
        print "Root sum sq similarity: ", sqrt(sumSq)
    else:
        print "Error: Input vectors of different lengths."

def method_2_cosineCoefSimilarity(v1, v2):    
    '''
    "The cosine similarity function (CSF) is the most widely reported measure of
    vector similarity. The virtue of the CSF is its sensitivity to the relative
    importance of each word (Hersh and Bhupatiraju, 2003b). "
    
    [1], [2]
    '''
    if len(v1) == len(v2):
        if (np.all(v1 == np.zeros(len(v1))) or np.all(v2 == np.zeros(len(v1)))):
            print "Error: One vector has all 0 elements. Default to 0 for cosine similarity."
            print "cosine similarity: ", 0
        else:
            print "cosine similarity: ", np.dot(v1,v2) / sqrt( np.sum(np.square(v1)) * np.sum(np.square(v2)) )
    else:
        print "Error: Input vectors of different lengths."

def method_3_JaccardCoefSimilarity(v1, v2):    
    '''
    "The Jaccard Coefficient, in contrast, measures similarity as the proportion 
    of (weighted) words two texts have in common versus the words they do not 
    have in common (Van Rijsbergen, 1979)."
    
    [2]
    '''
    if len(v1) == len(v2):
        if (np.all(v1 == np.zeros(len(v1))) and np.all(v2 == np.zeros(len(v1)))):
            print "Error: Both vectors have all 0 elements. Default to 0 for Jaccard Coefficient."
            print "Jaccard Coefficient: ", 0
        else:
            print "Jaccard Coefficient: ", 1.0*np.dot(v1,v2) / ( np.sum(v1) + np.sum(v2) - np.dot(v1,v2) )
    else:
        print "Error: Input vectors of different lengths."

def method_4_DiceCoefSimilarity(v1, v2):    
    '''
    "Dice's coefficient simply measures the words that two texts have in common 
    as a proportion of all the words in both texts."
    
    [2]
    '''
    if len(v1) == len(v2):
        if (np.all(v1 == np.zeros(len(v1))) and np.all(v2 == np.zeros(len(v1)))):
            print "Error: Both vectors have all 0 elements. Default to 0 for Dice Coefficient."
            print "Dice Coefficient: ", 0
        else:
            print "Dice Coefficient: ", 2.0*np.dot(v1,v2) / ( np.sum(v1) + np.sum(v2) )
    else:
        print "Error: Input vectors of different lengths."

def compare_T1(v1,v2):
    # Compare all questions of a certain type, and return value of 0-1
    return answer_diffs # value 0-1

def question_similarity(v1,v2):

    equal = np.array(v1)==np.array(v2) # Future tests look at each question separately as they are much more complicated that T/F
    xx = np.where(equal)[0]
    answer_diffs = np.array([0]*len(v1))
    answer_diffs[xx] = 1

    # return vectors between 0 and 1 for each question
    return answer_diffs

def candidate_similarity(diff):

    return np.sqrt( np.sum(np.square( np.array(diff) )) ) / MAX_DIFF

def candidate_matrix():

    return #matrix of NxN candidates with answer difference values between 0-1

def method_5_EuclidDistSimilarity(v1,v2):
    '''
    Euclidean distance.
    
    [3]
    '''
    if len(v1) == len(v2):
        print "Euclidean Distance similarity: ", np.sqrt( np.sum(np.square( np.array(v1)-np.array(v2) )) ) / MAX_DIFF
    else:
        print "Error: Input vectors of different lengths."

def method_6_NormEuclidDistSimilarity(v1, v2):
    '''
    Normalized Euclidean distance.
    
    [4]
    '''
    if len(v1) == len(v2):
        print "Norm. Euclidean Distance similarity: ", sqrt( np.sum(np.square( np.array(v1)-np.array(v2) )) ) / float(len(v1))
    else:
        print "Error: Input vectors of different lengths."

def method_7_WeightEuclidDistSimilarity(v1, v2):
    '''
    Weighted Euclidean distance.
    
    [5]
    '''
    if len(v1) == len(v2):
        print "Weight. Euclidean Distance similarity: ", sqrt( np.sum(np.square( (np.array(v1)-np.array(v2))/float(len(v1)) )) )
    else:
        print "Error: Input vectors of different lengths."
        
# 2.3. repeat for all unique pairs


# 3. output compiled sensitivity matrix.



def test():
    method_0_SimpleDiffSimilarity(vector_3, vector_6)
    method_1_RootSumSqSimilarity(vector_3, vector_6)
    method_2_cosineCoefSimilarity(vector_3, vector_6)
    method_3_JaccardCoefSimilarity(vector_3, vector_6)
    method_4_DiceCoefSimilarity(vector_3, vector_6)
    method_5_EuclidDistSimilarity(vector_3, vector_6)
    method_6_NormEuclidDistSimilarity(vector_3, vector_6)
    method_7_WeightEuclidDistSimilarity(vector_3, vector_6)
    #print "np.square([1,2,3]): ", np.square([1,2,3]) 
    #print "np.sum(np.square([1,2,3])): ", np.sum(np.square([1,2,3]))

def main():
    test()

if __name__ == '__main__':
    main()




'''

>>> import numpy as np
>>> a = [3,5,6]
>>> b = [3,7,2]
>>> list(np.array(a) - np.array(b)) #for converting from np 'array' to 'list'
[0, -2, 4]

'''