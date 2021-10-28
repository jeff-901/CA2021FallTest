import subprocess
import unittest
import os
import sys

files = os.listdir()
for f in files:
    if f[-2:] == ".s" or f[-2:] == ".S":
        SCRIPT_NAME = f

class Test(unittest.TestCase):
    def setUp(self):
        self.timeout = 30
        self.maxDiff = None
        self.script_name = ["jupiter", SCRIPT_NAME]

    def run_testcase(self, name):
        with open(os.path.join("input", f"{name}.txt")) as fin:
            input_data = fin.read()
        with open(os.path.join("output", f"{name}.txt")) as fin:
            ans = fin.read()
        input_data = input_data.split("\n")[:-1]
        input_data = [ele.replace(" ", "\n") + "\n" for ele in input_data]
        ans = ans.split("\n")[:-1]
        for i in range(0, len(input_data)):
            print(i + 1)
            data = input_data[i]
            output = subprocess.check_output(
                self.script_name,
                text=True,
                timeout=self.timeout,
                input=data,
            )
            self.assertEqual(output.split("\n")[0], ans[i])

    def test_01_sample1(self):
        self.run_testcase("sample1")


if __name__ == "__main__":
    unittest.main()
