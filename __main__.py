import os
import re
import sys
from pathlib import Path
from subprocess import call, run

# INIT
try:
    cmpl_name = sys.argv[1]
    program_name = sys.argv[2]
except IndexError:
    exit("you should write options: compiler_name program_name")

working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent
run_msg = testing_directory.joinpath("test")
print(run_msg)
run(f'{cmpl_name} -o {run_msg} {working_directory.joinpath(program_name)}')
if not testing_directory.joinpath('test.exe').is_file():
    exit('cant compile program')
cases_directory = testing_directory.joinpath('tests')

EPS = 0.001

def read_to_array(n, file):
    array = []
    a = file.readline().strip(" \n")

    if re.search("solution", a) is not None:
        return a
    else:
        array.append(float(a))

    for _ in range(1, n):
        elem = float(file.readline())
        array.append(elem)
    return array


class Test:
    def __init__(self, num):
        # this is a constructor for an existing Test
        # if you want to generate new one, use testGenerator
        self.num = num

    def run(self, group_name):
        result_filename = testing_directory .joinpath("test_output")
        result = True
        try:
            input_filename = f"{cases_directory}/{group_name}/test{self.num}.in"
            output_filename = f"{cases_directory}/{group_name}/test{self.num}.out"
            code_filename = f"{cases_directory}/{group_name}/test{self.num}.code"

            result_code = call(f"{run_msg} \"{input_filename}\" {result_filename}")

            if result_code != 0:
                try:
                    with open(code_filename) as code_file:
                        code = int(code_file.read())
                        return result_code == code
                except IOError:
                    return False

            with open(input_filename, "r") as input_file, \
                    open(output_filename, "r") as output_file, \
                    open(result_filename, "r") as current_res:

                n = int(input_file.readline())
                s = [0] * (n + 1)

                for i in range(n):
                    s[i] = list(map(float, input_file.readline().split()))

                x = read_to_array(n, output_file)
                correct = read_to_array(n, current_res)
                result = self.check(x, correct, n)
        except ValueError:
            result = False
        finally:
            print(f"\tTest {self.num}:".ljust(10), "Passed" if result else "FAILED")
            try:
                os.remove(result_filename)
            finally:
                return result

    def check(self, first, second, n):
        if type(first) != type(second):
            return False

        if type(first) == type(second) == str:
            return first == second

        for i in range(n):
            if abs(first[i] - second[i]) > EPS:
                return False
        return True


class Group:
    def __init__(self, name, frm, to):
        self.tests = []
        for i in range(frm, to + 1):
            self.tests.append(Test(i))
        self.name = name

    def log(self):
        print(f"\n{self.name} Tests:\n")


class Tester:
    def __init__(self, groups):
        self.groups = groups

    def run(self):
        success = 0
        count = 0
        for group in self.groups:
            group.log()
            for test in group.tests:
                if test.run(group.name):
                    success += 1
                count += 1
        print("\n   " + "-" * 28 + "\n")
        if success == count:
            print("\tTests: PASSED")
        else:
            print("\tTests: FAILED")
            print(f"\tPassed: {success}/{count}")
        print()


def check_solution(n, coef, var):
    res = 0
    for i in range(n):
        for j in range(n):
            res += coef[i][j] * var[j]
        res -= coef[i][n]
        print(res)
        if abs(res) > EPS:
            return False
    return True


group1 = Group("Google Drive", 1, 13)
group2 = Group("Very Small Number", 14, 53)
group3 = Group("Small Number", 54, 68)
group4 = Group("Moderate Number", 69, 80)
group5 = Group("Moderate Number", 81, 100)
group6 = Group("No solution", 101, 110)
group7 = Group("Many solutions", 111, 140)
group8 = Group("Eps", 141, 160)
group9 = Group("Small floats", 161, 200)
group10 = Group("Combining large and small numbers", 201, 210)
group11 = Group("Error Handling", 211, 214)
group12 = Group("Float No solution", 213, 284)

groups = [group1, group2, group3, group4,
          group5, group6, group7, group8,
          group9, group10, group11, group12]

tester = Tester(groups)
tester.run()