from math import *
import numpy as np
import matplotlib.pyplot as plt

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
def import_db_as_df():
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
    client = MongoClient() #client = MongoClient('localhost:27017')
    db = client.DC2_CP #db = client.database_name
    collection = db.general_info #collection = db.collection_name
    data = pd.DataFrame(list(collection.find())) #continue with this. <>
    
    ## preview data
    #print "data.size", data.size
    #print "data.head", data.head
    #with pd.option_context('display.max_rows', 10, 'display.max_columns', 10):
    #    print data.ix[:5,:5]
    #print data.ix[:5,:5]
    
    return data



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


#num_questions = len(vector_1)
#all_yes = np.array([1]*num_questions)
#all_no  = np.array([0]*num_questions)
#MAX_DIFF = np.sqrt( np.sum(np.square( all_yes-all_no )) )
def get_max_diff(v1):
    return sqrt(float(len(v1)))

# <>
def compare_T1(v1,v2):
    # Compare all questions of a certain type, and return value of 0-1
    return answer_diffs # value 0-1

# <>
def question_similarity(v1,v2):
    #print "---"
    #print v1
    #print v2
    equal = np.array(v1)==np.array(v2) # Future tests look at each question separately as they are much more complicated that T/F
    ### <> what if not exactly equal but close? machine error?
    #print equal
    xx = np.where(equal)[0]
    #print xx
    answer_diffs = np.zeros(len(v1))
    #print answer_diffs
    answer_diffs[xx] = 1
    #print answer_diffs
    # return vectors between 0 and 1 for each question
    #print "---"    
    return answer_diffs

def get_normalized_EuclidDist(vector_differences,maximum_difference):
    '''
    AKA "candidate_difference"
    '''
    
    #print "candidate_difference | vector_differences: ", vector_differences
    #print "candidate_difference | MAX_DIFF: ", MAX_DIFF        
    
    return np.sqrt(np.sum(np.square(np.array(vector_differences))))/maximum_difference # diff = np.array(v1)-np.array(v2)

def get_two_candidate_sim(v_1,v_2):
    #    print "get_two_candidate_sim | vector1: ", vector1
    #    print "get_two_candidate_sim | vector2: ", vector2
    
    max_diff = get_max_diff(v_1)
    #print "get_two_candidate_sim | MAX_DIFF: ", MAX_DIFF #ok
    
    v_diff = np.array(v_1)-np.array(v_2) # may need abs()?
    #print "get_two_candidate_sim | v_diff: ", v_diff
    
    num = np.sqrt( np.sum(np.square( np.array(v_diff) )) )
    #print "get_two_candidate_sim | num: ", num
    
    candidateDifference = get_normalized_EuclidDist(v_diff, max_diff)
    #print "get_two_candidate_sim | candidateDifference: ", candidateDifference

    candidateSimilarity = 1 - candidateDifference
    #print "get_two_candidate_sim | candidateSimilarity: ", candidateSimilarity
    
    
    #print question_similarity(vector1,vector2)
    
    return candidateSimilarity

def get_candidate_sim_matrix(data):
    
    # 1. get subset of dataframe
    df = data.loc[:, ['is_BD_sales_or_client_relationships', 
                      'is_citizen',
                      'is_comm_organizer',
                      'is_freelance']]
    num_candidates = df.shape[0]

    candidate_sim_matrix = np.eye(num_candidates) # initialize candidate_sim_matrix
    
    # loop for all unique pairs
    for i in range(num_candidates - 1):
        for j in range(i+1, num_candidates):
            candidateSimilarity = get_two_candidate_sim(df.ix[i,:],
                                                        df.ix[j,:])
            candidate_sim_matrix[i,j] = candidateSimilarity
            candidate_sim_matrix[j,i] = candidateSimilarity

    return candidate_sim_matrix #matrix of NxN candidates with answer difference values between 0-1

def test():
#    method_0_SimpleDiffSimilarity(vector_3, vector_6)
#    method_1_RootSumSqSimilarity(vector_3, vector_6)
#    method_2_cosineCoefSimilarity(vector_3, vector_6)
#    method_3_JaccardCoefSimilarity(vector_3, vector_6)
#    method_4_DiceCoefSimilarity(vector_3, vector_6)
#    method_5_EuclidDistSimilarity(vector_3, vector_6)
#    method_6_NormEuclidDistSimilarity(vector_3, vector_6)
#    method_7_WeightEuclidDistSimilarity(vector_3, vector_6)
#    #print "np.square([1,2,3]): ", np.square([1,2,3]) 
#    #print "np.sum(np.square([1,2,3])): ", np.sum(np.square([1,2,3]))
    TF = False
    if TF:
        vector_1 = [True,True,False,True,False]
        vector_2 = [True,True,False,True,False]
        vector_3 = [True,False,False,False,False]
        vector_4 = [False,False,False,False,False]
        vector_5 = [True,True,True,True,True]
        vector_6 = [False,False,True,False,True] #opposite of vector_1
    else:
        vector_1 = [1,1,0,1,0]
        vector_2 = [1,1,0,1,0]
        vector_3 = [1,0,0,0,0]
        vector_4 = [0,0,0,0,0]
        vector_5 = [1,1,1,1,1]
        vector_6 = [0,0,1,0,1] #opposite of vector_1
        #7,8 for testing MAX_DIFF to be 1
        vector_7 = np.ones(5)
        vector_8 = np.zeros(5)

    #print "test | vector_1: ", vector_1
    #print "test | vector_3: ", vector_3
    
    #vector1 = vector_1
    #vector2 = vector_6
    
    #print "candidateSimilarity:", get_two_candidate_sim(vector_8, vector_8)

def test_M():
    data1 = import_db_as_df()
    M = get_candidate_sim_matrix(data1)
    
    #print M
    #np.savetxt("candidate_sim_matrix.csv", M, delimiter=",")
    #plt.imshow(M, cmap='hot', interpolation='nearest')
    plt.imshow(M, cmap='rainbow', interpolation='nearest')

def main():
    #test()
    test_M()

if __name__ == '__main__':
    main()




'''

>>> import numpy as np
>>> a = [3,5,6]
>>> b = [3,7,2]
>>> list(np.array(a) - np.array(b)) #for converting from np 'array' to 'list'
[0, -2, 4]

'''