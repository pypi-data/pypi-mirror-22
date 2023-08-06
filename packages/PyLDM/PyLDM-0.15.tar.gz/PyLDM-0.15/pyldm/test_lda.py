import unittest
import numpy as np
from fit.data import Data
from fit.lda import LDA

class TestLDA(unittest.TestCase):
    ##################################################################
    # Except where otherwise noted, the data loaded from the test    #
    # matrix IS USED AS THE DECAY MATRIX instead of the data matrix. #
    # This is to simplify computations during for the purpose of     #
    # testing.                                                       #
    ##################################################################
    def setUp(self):
        print("in setUp()")
        self.data = Data("data/test_mat.csv")
        self.data.updateIRF(0, 0, 0, 0)
        self.lda = LDA(self.data)
        self.U = np.array([[-1., 0, 0, 0], [0, 0, 1., 0], [0, -1., 0, 0], [0, 0, 0, 1.]])
        self.S = np.diag([5., 4., 3., 2.])
        self.Vt = np.array([[0, 0, 1., 0], [0, -1., 0, 0], [-1., 0, 0, 0], [0, 0, 0, 1.]])
        self.taus = np.array([0.5, 1., 2., 4.])
        self.alphas = np.array([0, 1])


        self.lda.updateParams(self.taus, self.alphas, "L2", np.identity(4), True)
        self.D = np.array([[1, 1, 1, 1], [1./64., 1./8., 2**(0.5)/4., 2**(0.25)/4.],
                           [1./256., 1./16., 1./4., 1./2.], [1./1024., 1./32., 2**(0.5)/8., 8**(0.25)/4]])

    def tearDown(self):
        print("in tearDown()")
        del self.data
        del self.lda
        del self.U
        del self.S
        del self.Vt
        del self.taus
        del self.alphas
        del self.D

    def test_load(self):
        print("In test_load()")
        self.assertIsInstance(self.data, Data)

    def test_shape(self):
        print("In test_shape()")
        self.assertEqual(self.data.data.shape, (4, 4))

    def test_genD(self):
        print("In test_genD()")
        self.lda.genD()
        D = self.lda.D
        self.assertAlmostEqual(D[1, 1], self.D[1, 1])

    def test_genD2(self):
        print("In test_genD2()")
        self.lda.genD()
        D = self.lda.D
        self.assertAlmostEqual(D[-1, 3], self.D[-1, 3])

    def test_solve_L2(self):
        # Alpha = 0
        print("In test_solve_L2()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        x_opt = self.lda._solve_L2(0)
        soln = np.array([[-0.00520833, -0.0416667, -0.117851, -0.198201], [0.000976563, 0.015625, 0.0625, 0.125], 
                         [-0.2, -0.2, -0.2, -0.2], [0.000488281, 0.015625, 0.0883883, 0.210224]])
        self.assertAlmostEqual(x_opt[2, 3], soln[2, 3], delta=1e-8)

    def test_solve_L2_2(self):
        # Alpha = 0
        print("In test_solve_L2_2()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        x_opt = self.lda._solve_L2(0)
        soln = np.array([[-0.00520833, -0.0416667, -0.117851, -0.198201], [0.000976563, 0.015625, 0.0625, 0.125], 
                         [-0.2, -0.2, -0.2, -0.2], [0.000488281, 0.015625, 0.0883883, 0.210224]])
        self.assertAlmostEqual(x_opt[1, 2], soln[1, 2], delta=1e-8)

    def test_solve_L2_3(self):
        # Alpha = 1
        print("In test_solve_L2_3()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        x_opt = self.lda._solve_L2(1)
        soln = np.array([[-0.0046875, -0.0375, -0.106066, -0.178381], [0.000919118, 0.0147059, 0.0588235, 0.117647],
                         [-0.192308, -0.192308, -0.192308, -0.192308], [0.000390625, 0.0125, 0.0707107, 0.168179]])
        self.assertAlmostEqual(x_opt[3, 0], soln[3, 0], delta=1e-8)

    def test_solve_L2_4(self):
        # Alpha = 1
        print("In test_solve_L2_4()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        x_opt = self.lda._solve_L2(1)
        soln = np.array([[-0.0046875, -0.0375, -0.106066, -0.178381], [0.000919118, 0.0147059, 0.0588235, 0.117647],
                         [-0.192308, -0.192308, -0.192308, -0.192308], [0.000390625, 0.0125, 0.0707107, 0.168179]])
        self.assertAlmostEqual(x_opt[1, 0], soln[1, 0], delta=1e-8)

    def test_calc_H_and_S(self):
        # Alpha = 0
        print("In test_calc_H_and_S()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(0)
        H_sol = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.assertAlmostEqual(H[1, 1], H_sol[1, 1], delta=1e-8)

    def test_calc_H_and_S2(self):
        # Alpha = 0
        print("In test_calc_H_and_S2()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(0)
        S_sol = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.assertAlmostEqual(S[3, 3], S_sol[3, 3], delta=1e-8)

    def test_calc_H_and_S3(self):
        # Alpha = 1
        print("In test_calc_H_and_S3()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(1)
        H_sol = np.array([[25./26., 0, 0, 0], [0, 9./10., 0, 0], [0, 0, 16./17., 0], [0, 0, 0, 4./5.]])
        self.assertAlmostEqual(H[0, 0], H_sol[0, 0], delta=1e-8)

    def test_calc_H_and_S4(self):
        # Alpha = 1
        print("In test_calc_H_and_S4()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(1)
        H_sol = np.array([[25./26., 0, 0, 0], [0, 9./10., 0, 0], [0, 0, 16./17., 0], [0, 0, 0, 4./5.]])
        self.assertAlmostEqual(H[0, 3], H_sol[0, 3], delta=1e-8)

    def test_calc_H_and_S5(self):
        # Alpha = 1
        print("In test_calc_H_and_S5()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(1)
        S_sol = np.array([[9./10., 0, 0, 0], [0, 16./17., 0, 0], [0, 0, 25./26., 0], [0, 0, 0, 4./5.]])
        self.assertAlmostEqual(S[3, 3], S_sol[3, 3], delta=1e-8)

    def test_calc_H_and_S6(self):
        # Alpha = 1
        print("In test_calc_H_and_S6()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        H, S = self.lda._calc_H_and_S(1)
        S_sol = np.array([[9./10., 0, 0, 0], [0, 16./17., 0, 0], [0, 0, 25./26., 0], [0, 0, 0, 4./5.]])
        self.assertAlmostEqual(S[1, 2], S_sol[1, 2], delta=1e-8)

    def test_calc_k(self):
        print("In test_calc_k()")
        self.lda.alphas = np.linspace(-10, 10, 101)
        x = np.linspace(-10, 10, 101)
        y = x**2 + 5
        k = self.lda._calc_k(x, y)
        # Max curvature for the parabola should be at the inflection point.
        self.assertEqual(k.argmax(), 50)

    def test_L1_min(self):
        print("In test_L1_min()")
        self.lda.x_opts[:, :, 0] = np.array([[100, 10, 3, .1], [3, 1, 34, -10], [.5, 31, -4, 2], [10, 21, -5, 1]])
        x = self.lda._L1_min(self.U, self.D, 0)
        # Should be similar to ordinary least squares solution because using orthogonal matrix
        soln = np.transpose(self.U).dot(self.D)
        self.assertAlmostEqual(x[1, 1], soln[1, 1], delta=1e-8)

    def test_L1_min2(self):
        print("In test_L1_min2()")
        self.lda.x_opts[:, :, 0] = np.array([[100, 10, 3, .1], [3, 1, 34, -10], [.5, 31, -4, 2], [10, 21, -5, 1]])
        x = self.lda._L1_min(self.U, self.D, 0)
        # Should be similar to ordinary least squares solution because using orthogonal matrix
        soln = np.transpose(self.U).dot(self.D)
        self.assertAlmostEqual(x[2, 3], soln[2, 3], delta=1e-8)

    def test_L1_min3(self):
        print("In test_L1_min3()")
        self.lda.x_opts[:, :, 0] = np.array([[100, 10, 3, .1], [3, 1, 34, -10], [.5, 31, -4, 2], [10, 21, -5, 1]])
        x = self.lda._L1_min(self.U, self.D, 100)
        # Should be zero because of high alpha value
        soln = np.zeros([4, 4])
        self.assertEqual(x[3, 0], soln[3, 0])

    def test_L1_min4(self):
        print("In test_L1_min4()")
        self.lda.x_opts[:, :, 0] = np.array([[100, 10, 3, .1], [3, 1, 34, -10], [.5, 31, -4, 2], [10, 21, -5, 1]])
        x = self.lda._L1_min(self.U, self.D, 100)
        # Should be zero because of high alpha value
        soln = np.zeros([4, 4])
        self.assertEqual(x[2, 2], soln[2, 2])

    def test_elnet(self):
        pass
        # Makes use of same function as LASSO
        #print("In test_elnet()")

    def test_tsvdInv(self):
        print("In test_tsvdInv()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        S = np.diag([1./5., 1./4., 0, 0])
        soln = np.transpose(self.Vt).dot(S).dot(np.transpose(self.U))
        D_plus = self.lda._tsvdInv(2)
        self.assertEqual(D_plus[3, 0], soln[3, 0])

    def test_tsvd(self):
        print("In test_tsvd()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        S = np.diag([1./5., 1./4., 0, 0])
        soln = np.transpose(self.Vt).dot(S).dot(np.transpose(self.U)).dot(self.D)
        x = self.lda._tsvd(2)
        self.assertEqual(x[1, 3], soln[1, 3])

    def test_tsvd2(self):
        print("In test_tsvd2()")
        A = self.lda.A
        self.lda.A = self.D
        self.lda.D = A
        S = np.diag([1./5., 1./4., 0, 0])
        soln = np.transpose(self.Vt).dot(S).dot(np.transpose(self.U)).dot(self.D)
        x = self.lda._tsvd(2)
        self.assertEqual(x[0, 0], soln[0, 0])
        
if __name__ == '__main__':
    unittest.main()
