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
        self.assertFalse(3 > t)
        
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
        a = 3
        b = p

        test1add = Ordinal([(o,1),(z,4)])
        self.assertEqual(p+3,test1add)

        self.assertEqual(3+p,p)

        b += 3
        self.assertEqual(b,test1add)

        a += o
        self.assertEqual(a,o)
        

    def test_ordinal_add_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        b = p

        test1add = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,1)]),1),(z,1)])
        self.assertEqual(o + p, test1add)

        test2add = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,1)]),1),(Ordinal([(y,1)]),3),(y,1)])
        self.assertEqual(p + o, test2add)

        b += o
        test3add = Ordinal([(o,1),(w,3),(y,1)])
        self.assertEqual(b, test3add)

        b += b
        test4add = Ordinal([(o,2),(w,3),(y,1)])
        self.assertEqual(b, test4add)


class TestSubstaction(unittest.TestCase):
    def test_natural_sub_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        t = Ordinal(3)
        a = 3
        b = p

        self.assertEqual(p-1,p)

        self.assertEqual(3-t,z)

        b -= 3
        self.assertEqual(b,p)

        a -= t
        self.assertEqual(a,z)

    def test_ordinal_sub_ordinal(self):
        t = Ordinal(3)
        u = Ordinal([(w,3),(t,5),(y,1),(z,4)])
        v = Ordinal([(w,3),(t,3),(z,5)])
        c = u

        test1sub = Ordinal([(t,2),(y,1),(z,4)])
        self.assertEqual(u - v, test1sub)

        self.assertEqual(v + test1sub, u)

        c -= v
        self.assertEqual(c, test1sub)

        c -= c
        self.assertEqual(c, z)


class TestMultiplication(unittest.TestCase):
    def test_natural_mul_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        a = 2
        b = o

        test1mul = Ordinal([(w,6),(y,1)])
        self.assertEqual(o*2,test1mul)

        self.assertEqual(2*o,o)

        a *= o
        self.assertEqual(a,o)

        b *= 2
        self.assertEqual(b,test1mul)
        

    def test_ordinal_mul_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        p = Ordinal([(o,1),(Ordinal.zero,1)])
        s = Ordinal([(y,1),(z,1)])
        b = p

        test1mul = Ordinal([(Ordinal([(Ordinal([(y,1)]),3),(y,2)]),3),(Ordinal([(Ordinal([(y,1)]),3),(y,1),(z,1)]),1)])
        self.assertEqual(p * o, test1mul)

        b *= o
        self.assertEqual(b, test1mul)

        s *= s
        test2mul = Ordinal([(Ordinal(2),1),(y,1),(z,1)])
        self.assertEqual(s, test2mul)


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

        b1 = p
        b1 //= 2
        self.assertEqual(b1,test1div)

        b2 = p
        b2 %= 2
        self.assertEqual(b2,y)

        a1 = 3
        a1 //= t
        self.assertEqual(a1,y)

        a2 = 3
        a2 %= t
        self.assertEqual(a2,z)

    def test_ordinal_div_ordinal(self):
        m = Ordinal([(w,1),(Ordinal(3),2),(Ordinal(2),5),(z,4)])
        n = Ordinal([(Ordinal(2),4),(y,7),(z,5)])

        test1div = Ordinal([(w,1),(y,2),(z,1)])
        self.assertEqual(m // n, test1div)

        test2div = Ordinal([(Ordinal(2),1),(z,4)])
        self.assertEqual(m % n, test2div)
        
        self.assertEqual(n*test1div + test2div, m)

        m1 = m
        m1 //= n
        self.assertEqual(m1, test1div)

        m2 = m
        m2 %= n
        self.assertEqual(m2, test2div)

        m //= m
        self.assertEqual(m, 1)

        n %= n
        self.assertEqual(n, 0)


class TestExponentation(unittest.TestCase):
    def test_natural_pow_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        s = Ordinal([(y,1),(z,1)])
        a = 2
        b = s

        test1exp = Ordinal([(Ordinal([(w,3),(z,1)]),1)])
        self.assertEqual(2**o,test1exp)

        test2exp = Ordinal([(Ordinal(2),1),(y,1),(z,1)])
        self.assertEqual(s**2,test2exp)

        a **= o
        self.assertEqual(a,test1exp)

        b **= 2
        self.assertEqual(b,test2exp)

    def test_ordinal_pow_ordinal(self):
        o = Ordinal([(w,3),(y,1)])
        s = Ordinal([(y,1),(z,1)])

        test1exp = Ordinal([(Ordinal([(y,1),(z,1)]),1),(w,1)])
        self.assertEqual(s**s, test1exp)

        test2exp = Ordinal([(Ordinal([(w,3),(Ordinal(2),1)]),1)])
        self.assertEqual(o**o, test2exp)

        s **= w
        test3exp = Ordinal([(w,1)])
        self.assertEqual(s, test3exp)

        o **= o
        self.assertEqual(o, test2exp)


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
    z = Ordinal.zero
    y = Ordinal.one
    
    unittest.main()
