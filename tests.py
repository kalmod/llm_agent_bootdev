# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


class TestGetFileInfo(unittest.TestCase):
    # def test_valid_path_A(self):
    #     print("\n VALID_PATH_A - run test")
    #     result = get_files_info("calculator", ".")
    #     print("\n", result)
    #     self.assertNotIn("Error:", result)
    #
    # def test_valid_path_B(self):
    #     print("\n VALID_PATH_B - run test")
    #     result = get_files_info("calculator", "pkg")
    #     print("\n", result)
    #     self.assertNotIn("Error:", result)
    #
    # def test_invalid_path_A(self):
    #     print("\n INVALID_PATH_A - run test")
    #     result = get_files_info("calculator", "/bin")
    #     print("\n", result)
    #     self.assertIn("Error:", result)
    #
    # def test_invalid_path_B(self):
    #     print("\n INVALID_PATH_B - run test")
    #     result = get_files_info("calculator", r"../")
    #     print("\n", result)
    #     self.assertIn("Error:", result)

    def test_get_file_content_pass_truncate(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertIn("truncated at 10000", result)

    def test_get_file_content_pass_A(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertIn("main()", result)

    def test_get_file_content_pass_B(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertIn("class Calculator:", result)

    def test_get_file_content_fail_A(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertIn("Error:", result)


if __name__ == "__main__":
    unittest.main()
