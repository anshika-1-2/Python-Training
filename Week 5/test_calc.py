import unittest
import calc

from calc import add


class TestCalc(unittest.TestCase):
    def test_add(self):
        
        self.assertEqual(add(2, 3), 5)

        self.assertEqual(calc.add(2, -2), 0)

    def test_subtract(self):
        result = calc.subtract(5, 3)
        self.assertEqual(result, 2)
        
        
    def test_multiply(self):
        result = calc.multiply(4, 3)
        self.assertEqual(result, 12)
        
    def test_divide(self):
        result = calc.divide(10, 2)
        self.assertEqual(result, 5)
        