import re
import os
import subprocess
import shutil
import filecmp

input_files = sorted(os.listdir("input"))
input_file_pattern = re.compile(r"instruction_(.+)\.txt")
failed_tests = list()

# File checking
if not os.path.exists("CPU.out"):
    raise ValueError("CPU.out does not exist")
for input_file in input_files:
    match = input_file_pattern.match(input_file)
    if match is None:
        raise ValueError(f"Invalid input file name: {input_file}")
    test_id = match[1]
    output_file_name = f"output_{test_id}.txt"
    if not os.path.exists(os.path.join("output", output_file_name)):
        raise ValueError(f"{input_file} exists but {output_file_name} does not exist")

# Execute tests
for input_file in input_files:
    print(f"Executing test for {input_file} ... ", end="")
    match = input_file_pattern.match(input_file)
    test_id = match[1]
    output_file_name = f"output_{test_id}.txt"
    shutil.copyfile(os.path.join("input", input_file), "instruction.txt")
    subprocess.run(["./CPU.out"], stdout=subprocess.DEVNULL)
    passed = filecmp.cmp("output.txt", os.path.join("output", output_file_name))
    if passed:
        print("Passed")
    else:
        print("Failed")
        failed_tests.append(input_file)

# Output result
print("=" * 40)
print("Result:")
if failed_tests:
    for test_name in failed_tests:
        print(f"Test {test_name} failed!")
else:
    print("All tests passed!")