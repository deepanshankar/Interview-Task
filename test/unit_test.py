import sys
sys.path.insert(1, '../src')

from assignment import process_input        # import function from Assignment
import pandas as pd
import unittest


class TestForErrorCodes(unittest.TestCase):

    def test_empty(self):
        """
        Test for empty input
        """
        data = ""
        df = process_input([data], True)
        self.assertTrue(df["Error Code"].empty, "Processed input is not empty as expected")

    def test_valid(self):
        """
        Tests for valid test input
        """
        data = "L1&1&AB"
        df = process_input([data], True)
        error_test = pd.Series(["E01", "E01", "E05"])
        self.assertTrue(df["Error Code"].equals(error_test), "Processed input for L1 section do not produce error codes"
                                                             "as expected")

    def test_invalid_section(self):
        """
        Test for invalid section not given in definitions
        """
        data = "L6&1&AB"
        df = process_input([data], True)
        self.assertTrue(df["Error Code"].empty, "Not as expected for invalid sections")

    def test_missing_subsection(self):
        """
        Tests missing subsection case
        """
        data = "L3"
        df = process_input([data], True)
        error_test = pd.Series(["E05"])
        self.assertTrue(df["Error Code"].equals(error_test), "Fails in Error Codes for missing sub-sections")

    def test_input_exceeds_subsections(self):
        """
        Test for exceeding sub-sections in inputs than defined in definitions
        """
        data = "L3&b&1&Ab&34"
        df = process_input([data], True)
        error_test = pd.Series(["E01"])
        self.assertTrue(df["Error Code"].equals(error_test), "Fails for input greater than subsections in standard "
                                                             "definition")

    def test_input_space(self):
        """
        Test for inputs with space
        """
        data = "L3& "
        df = process_input([data], True)
        error_test = pd.Series(["E01"])
        self.assertTrue(df["Error Code"].equals(error_test), "Fails for space in inputs")

    def test_non_characters(self):
        """
        Test for inputs other than numbers and characters
        """
        data = "L3&."
        df = process_input([data], True)
        error_test = pd.Series(["E02"])
        self.assertTrue(df["Error Code"].equals(error_test), "Fails for data type other than numbers or characters")

    def test_invalid_input(self):
        """
        Test for invalid sections
        """
        data = "invalid&string"
        df = process_input([data], True)
        self.assertFalse(not df["Error Code"].empty, "Fails for data type other than numbers or characters")


if __name__ == "__main__":
    unittest.main()
