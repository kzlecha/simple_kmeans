from kmeans import KMeans
from numpy import array
from pandas import DataFrame, Series

import unittest


class TestKMeans(unittest.TestCase):
    '''
    Class for testing KMeans clustering
    '''
    def test_kmeans(self):
        '''
        test to see if the kmeans clustering will crash.
        Since KMeans is a random algorithm that only finds a local solution
        attempting to determine the "correctness" is impossible
        '''
        data = DataFrame([[1,0,1,0],
                          [2,1,3,0],
                          [0,2,1,0],
                          [5,6,5,6],
                          [7,6,6,7],
                          [7,5,6,7]])
        
        # kmeans must take scaled data
        # standardize with mean normalization
        data=(data-data.mean())/data.std()

        k = 2

        # run kmeans
        kmeans = KMeans(k)
        centroids, memberships = kmeans.fit_predict(data)

        # membership must be in range of 0 to k-1 inclusive
        for membership in memberships:
            if membership not in range(0,k):
                assert False

    def test_euc_dist(self):
        '''
        test to ensure euclidian distance is calculated correctly
        Formula:
            dist = sqrt(sum((a[1]+b[1])^2 + ... + (a[n]+b[n])^2))
        '''
        data = DataFrame([[1,0], [0,0]])
        vector = array([0,0])
        distance = [1,0]

        dist = KMeans()._euclidian_distance(data.values,vector)
        for i in range(0,1):
            self.assertEqual(dist[i], distance[i])

    def test_check_input(self):
        '''
        test to ensure that the input returns false if is empty or has NaN
        '''
        data = DataFrame()
        self.assertFalse(KMeans()._check_input(data))

        data = DataFrame([[0,1,2],
                          [None, 2, 3],
                          [3,4,5]])
        self.assertFalse(KMeans()._check_input(data))

        data = data.dropna()
        self.assertTrue(KMeans()._check_input(data))

    def test_has_converged(self):
        '''
        test to ensure convergence occurs only when the centroids stop changing
        '''
        data = DataFrame([[0,0,0], [4,4,4], [-4,-4,-4]])
        centroids = DataFrame([[1,0,0], [3,4,3], [-2,-3,-4]]).values
        memberships = Series([0,1,2], index=data.index)

        self.assertFalse(KMeans(k=3)._has_converged(data,centroids,memberships))

        centroids = DataFrame([[0,0,0], [4,4,4], [-4,-4,-4]]).values
        self.assertTrue(KMeans(k=3)._has_converged(data,centroids,memberships))


# run the unittests
if __name__ == "__main__":
    unittest.main()
