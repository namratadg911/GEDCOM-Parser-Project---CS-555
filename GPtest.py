import unittest
import GEDCOM_Parser_Sprint1_v1
from prettytable import PrettyTable
import inspect
import GEDCOM_Parser_Sprint1_v1
from GEDCOM_Parser_Sprint1_v1 import Parser, us01_check_before_today, us03_birth_before_death, \
    us02_birth_before_marriage, us35_birth_inlast_30days, us36_death_inlast_30days, us42_reject_illegitimate_dates, \
    us04_marriage_before_divorce, us05_marriage_before_death
import logging


class TestUserStories(unittest.TestCase):
    logging.basicConfig(filename='gedcom.log', filemode='w', format='%(levelname)-2s : %(message)s', level=logging.INFO)

    rint = Parser()
    indi, fam, log = rint.main()
    rint.print_dicts(indi, fam)
    log_func = {
        ("US21", "HUSB"): lambda x: f"US21: FAM: {x[0]}: Husband ({x[1]}) has incorrect gender",
        ("US21", "WIFE"): lambda x: f"US21: FAM: {x[0]}: Wife ({x[1]}) has incorrect gender",
        ("US22", "FAM"): lambda x: f"US22: FAM: {x}: Family already exists",
        ("US22", "INDI"): lambda x: f"US22: INDI: {x}: Individual already exists",
        ("US42", "BIRT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Birth Date {x[1]}",
        ("US42", "DEAT"): lambda x: f"US42: INDI: {x[0]}: Illegitimate date for Death Date {x[1]}",
        ("US42", "MARR"): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Marriage Date {x[1]}",
        ("US42", "DIV"): lambda x: f"US42: FAM: {x[0]}: Illegitimate date for Divorce Date {x[1]}"
    }
    for x in log:
        logging.error(log_func[x[0], x[1]](x[2]))

    # Start of Sprint 1
    def test_US01(self):
        """Tests if the date from the dictionary is before today's date"""

        user_story = inspect.stack()[0][3].replace('test_', '')

        for id, records in self.indi.items():
            with self.subTest(id=id):
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')

                if birth_date1 is None:
                    logging.error(
                        f"{user_story} : INDI : {id} : Birth Date is not known ")
                    out = False
                else:
                    check_birth = us01_check_before_today(birth_date1)
                    if check_birth is False:
                        logging.error(
                            f"{user_story} : INDI : {id} : Birth Date {birth_date1} is before today's date.")
                    self.assertTrue(check_birth)

                if death_date1 is not None:
                    check_death = us01_check_before_today(death_date1)
                    if check_death is False:
                        logging.error(
                            f"{user_story} : INDI : {id} : Death Date {death_date1} is before today's date.")
                    self.assertTrue(check_death)

        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is None:
                    logging.error(
                        f"{user_story} : FAM : {id} : Marriage Date is not known ")
                else:
                    check_marr = us01_check_before_today(marr_date1)
                    if check_marr is False:
                        logging.error(
                            f"{user_story} : FAM : {id} : Marriage Date {marr_date1} is before today's date.")
                    self.assertTrue(check_marr)

                if div_date1 is not None:
                    check_div = us01_check_before_today(div_date1)
                    if check_div is False:
                        logging.error(
                            f"{user_story} : FAM : {id} : Divorce Date {div_date1} is before today's date.")
                    self.assertTrue(check_div)

    def test_US02(self):
        """Birth Date before marriage between spouses"""
        list_of_truth = us02_birth_before_marriage()
        self.assertNotIn('No', list_of_truth)

    def test_US03(self):

        list_of_truth = us03_birth_before_death()
        self.assertNotIn('No', list_of_truth)

    def test_US21(self):
        """Test the logging and printing of correct gender for roles"""
        print(f"\nThere is {len([i for i in self.log if i[0] == 'US21'])} Error Found For User Story 21: ")
        x = PrettyTable(["Test", "Case", "Spec"])
        for i in self.log:
            if i[0] == 'US21':
                x.add_row(i)
        print(x)

    def test_US22(self):
        """Test if the Family ID and the Individual ID are Unique"""
        print(f"\nThere is {len([i for i in self.log if i[0] == 'US22'])} Error Found For User Story 22: ")
        x = PrettyTable(["Test", "Case", "Spec"])
        for i in self.log:
            if i[0] == 'US22':
                x.add_row(i)
        print(x)
        ik = self.indi.keys()
        fk = self.fam.keys()
        self.assertEqual(len(ik), len(set(ik)))
        self.assertEqual(len(fk), len(set(fk)))

    def test_US35(self):
        """List birthdays in last 30 days"""
        x = PrettyTable(["ID", "Name", "Birthday"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                birth = record.get('BIRT')
                name = record.get('NAME')
                if birth is not None:
                    check_birth = us35_birth_inlast_30days(birth)
                    if check_birth is True:
                        x.add_row([id, name, birth])
        logging.info(f" US35: INDI: List all birthdays in the last 30 days \n {x}")

    def test_US36(self):
        """List death date in last 30 days"""
        x = PrettyTable(["ID", "Name", "Death"])
        for id, record in self.indi.items():
            with self.subTest(id=id):
                death = record.get('DEAT')
                name = record.get('NAME')
                check_death = us36_death_inlast_30days(death)
                if check_death is True:
                    x.add_row([id, name, death])
        logging.info(f" US36: INDI: List all deaths in the last 30 days \n {x}")

    def test_US42(self):
        """Tests if the illegitimate dates are rejected"""

        for id, records in self.indi.items():
            with self.subTest(id=id):
                birth_date1 = records.get('BIRT')
                death_date1 = records.get('DEAT')
                name = records.get('NAME')
                if birth_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(birth_date1))
                if death_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(death_date1))

        for id, records in self.fam.items():
            with self.subTest(id=id):
                marr_date1 = records.get('MARR')
                div_date1 = records.get('DIV')

                if marr_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(marr_date1))
                if div_date1 is not None:
                    self.assertTrue(us42_reject_illegitimate_dates(div_date1))

    # End of Sprint-1

    # Start of Sprint-2

    def test_US04(self):
        list_of_truth = us04_marriage_before_divorce()
        self.assertNotIn('No', list_of_truth)

    def test_US05(self):
        list_of_truth = us05_marriage_before_death()
        self.assertNotIn('No', list_of_truth)




if __name__ == '__main__':
    unittest.main()