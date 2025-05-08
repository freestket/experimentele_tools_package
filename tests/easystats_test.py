import unittest
import sys
sys.path.append("..")
import src.experimentele_tools_package.easystats as STAT

class EasyStatsTest(unittest.TestCase):
    
    def test_bereken_gemiddelde(self):
        same_measurements = [5 for _ in range(0, 500)]
        avg = STAT.bereken_gemiddelde(same_measurements)
        self.assertEqual(5, avg)

        simple_list = [5, 6, 8, 7, 2, 6, 3, 4, 2, 1, 0, 4, 5]
        avg = STAT.bereken_gemiddelde(simple_list)
        self.assertAlmostEqual(4.076923077, avg)

    def test_bereken_variantie_gekend_gemiddelde(self):
        ...

    def test_bereken_variantie_ongekend_gemiddelde(self):
        ...

    def test_foutpropagatie_som(self):
        ...

    def test_foutpropagatie_product(self):
        ...

    def test_foutpropagatie_algemeen(self):
        ...
