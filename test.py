import unittest

from ordinalni_kalkulator import *

class TestComparation(unittest.TestCase):
    def test_natural_to_ordinal(self):
        r = Ordinal([(w,3),(y,1)])
        t = Ordinal(3)

        self.assertEqual(3,t)

        self.assertNotEqual(3,w)
        self.assertNotEqual(3,r)

        self.assertTrue(w > 1)
        
    def test_ordinal_to_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        r = Ordinal([(w,3),(y,1)])
        s = Ordinal([(Ordinal([(y,1)]),3),(y,1)])
        t = Ordinal(3)

        self.assertEqual(r,s)
        self.assertNotEqual(w,r)
        self.assertNotEqual(w,t)

        self.assertFalse(p == o)
        self.assertTrue(o < p)
        self.assertTrue(w < p)
        self.assertFalse(w > p)
        self.assertFalse(p == w)

        

class TestAddition(unittest.TestCase):
    def test_natural_add_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])

        test1add = Ordinal([(o,1),(z,4)])
        self.assertEqual(p+3,test1add)

        self.assertEqual(3+p,p)

    def test_ordinal_add_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])

        test1add = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,1)]),1),(z,1)])
        self.assertEqual(o + p, test1add)

        test2add = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,1)]),1),(Ordinal([(y,1)]),3),(y,1)])
        self.assertEqual(p + o, test2add)

class TestSubstaction(unittest.TestCase):
    def test_natural_sub_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        t = Ordinal(3)

        self.assertEqual(p-1,p)

        self.assertEqual(3-t,z)

    def test_ordinal_sub_ordinal(self):
        t = Ordinal(3)
        u = Ordinal([(w,3),(t,5),(y,1),(z,4)])
        v = Ordinal([(w,3),(t,3),(z,5)])

        test1sub = Ordinal([(t,2),(y,1),(z,4)])
        self.assertEqual(u - v, test1sub)

        self.assertEqual(v + test1sub, u)

class TestMultiplication(unittest.TestCase):
    def test_natural_mul_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])

        test1mul = Ordinal([(w,6),(y,1)])
        self.assertEqual(o*2,test1mul)

        self.assertEqual(2*o,o)

    def test_ordinal_mul_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])

        test1mul = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,2)]),3),(Ordinal([(Ordinal([(y,1)]),3),(y,1),(z,1)]),1)])
        self.assertEqual(p * o, test1mul)

class TestDivision(unittest.TestCase):
    def test_natural_div_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        t = Ordinal(3)

        test1div = Ordinal([(o,1)])
        self.assertEqual(p // 2,test1div)
        self.assertEqual(p % 2,y)

        self.assertEqual(3 // t,y)
        self.assertEqual(3 % t,z)

    def test_ordinal_mul_ordinal(self):
        m = Ordinal([(w,1),(Ordinal(3),2),(Ordinal(2),5),(z,4)])
        n = Ordinal([(Ordinal(2),4),(y,7),(z,5)])

        test1div = Ordinal([(w,1),(y,2),(z,1)])
        self.assertEqual(m // n, test1div)

        test2div = Ordinal([(Ordinal(2),1),(z,4)])
        self.assertEqual(m % n, test2div)
        
        self.assertEqual(n*test1div + test2div, m)


class TestExponentation(unittest.TestCase):
    def test_natural_pow_ordinal(self):
        o = Ordinal([(w,3),(y,1)])

        test1exp = Ordinal([(Ordinal([(w,3),(z,1)]),1)])
        self.assertEqual(2**o,test1exp)

    def test_ordinal_pow_ordinal(self):
        o = Ordinal([(w,3),(y,1)])

        test1exp = Ordinal([(Ordinal([(y,1),(z,1)]),1),(w,1)])
        self.assertEqual((w+1)**(w+1), test1exp)

        test2exp = Ordinal([(Ordinal([(w,3),(Ordinal(2),1)]),1)])
        self.assertEqual(o**o, test2exp)
    

class TestSummation(unittest.TestCase):
    def test_natural_ordinal(self):
        t = Ordinal(4)

        test1 = Ordinal([(Ordinal(3),1),(Ordinal(2),3),(y,3),(z,3)])
        self.assertEqual(Ordinal.Isummation(lambda j: (w+j)**j, t),test1)

    def test_ordinal_ordinal(self):
        test1 = Ordinal([(Ordinal(2),7),(y,2)])
        self.assertEqual(Ordinal.Isummation(lambda j: j*w+w*j, w+3), test1)

        test2 = Ordinal([(Ordinal(2),1)])
        self.assertEqual(Ordinal.Isummation(lambda j: j, w*2), test2)


class TestProduct(unittest.TestCase):
    def test_natural_ordinal(self):
        t = Ordinal(3)

        test1 = Ordinal([(Ordinal(3),1),(Ordinal(2),2),(y,2),(z,1)])
        self.assertEqual(Ordinal.Iproduct(lambda j: (w+j)**j, t),test1)

    def test_ordinal_ordinal(self):
        test1 = Ordinal([(Ordinal([(y,3),(z,2)]),4)])
        self.assertEqual(Ordinal.Iproduct(lambda j: j + w, w*3 + 2), test1)

        test2 = Ordinal([(Ordinal([(Ordinal(2),1)]),1)])
        self.assertEqual(Ordinal.Iproduct(lambda j: w ** (w + j), w), test2)

if __name__ == '__main__':
    w = Ordinal.omega
    z = Ordinal.zero
    y = Ordinal.one
    
    unittest.main()
