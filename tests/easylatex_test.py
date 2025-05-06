import unittest
import sys
sys.path.append(".")
from src.experimentele_tools_package import easylatex as LATEX

class EasyLatexTest(unittest.TestCase):
    
    
    def test_generate_latex_table(self):
        
        test_table = ""
        test_table += "\\begin{table}[h!]\n"
        test_table += "\t\\centering\n"
        test_table += "\t\\caption{Dit is een tabel}\n"
        test_table += "\t\\begin{tabular}{|c|c|c|c|}\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\t$f$ [Hz] & $|x|$ [mm] $\\pm 1\\% & $\\phi$ [$^\\circ$] $\\pm 5\\%$ & $R = \\frac{U}{I}\\ [\\frac{\\volt}{\\ampere}]$ \\\\\n"
        test_table += "\t\t\\hline\\hline\n"
        test_table += "\t\ta_11 & a_21 & a_31 & a_41 \\\\\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\ta_12 & a_22 & a_32 & a_42 \\\\\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\ta_13 & a_23 & a_33 & a_43 \\\\\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\ta_14 & a_24 & a_34 & a_44 \\\\\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\ta_15 & a_25 & a_35 & a_45 \\\\\n"
        test_table += "\t\t\\hline\n"
        test_table += "\t\\end{tabular}\n"
        test_table += "\t\\label{tab:tabel1}\n"
        test_table += "\\end{table}"

        header = ["$f$ [Hz]", "$|x|$ [mm] $\\pm 1\\%", "$\\phi$ [$^\\circ$] $\\pm 5\\%$", "$R = \\frac{U}{I}\\ [\\frac{\\volt}{\\ampere}]$"]
        kol1 = ["a_11", "a_12", "a_13", "a_14", "a_15"]
        kol2 = ["a_21", "a_22", "a_23", "a_24", "a_25"]
        kol3 = ["a_31", "a_32", "a_33", "a_34", "a_35"]
        kol4 = ["a_41", "a_42", "a_43", "a_44", "a_45"]
        data = [kol1, kol2, kol3, kol4]

        table = LATEX.generate_latex_table(data, header, "Dit is een tabel", "tabel1")
        self.assertEqual(test_table, table)


        