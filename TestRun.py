from enum import Enum
from dataclasses import dataclass


class TestResult(Enum):
    FAILED = 0
    PASSED = 1


@dataclass
class TestRun:
    def __init__(self, final_result, tests_run, tests_passed, tests_failed, original_line="",
                 mutated_line="", mutation_line_number=0, mutated_file_name = "", full_script = ""):
        self.final_result = final_result
        self.tests_run = tests_run
        self.tests_passed = tests_passed
        self.tests_failed = tests_failed
        self.original_line = original_line
        self.mutated_line = mutated_line
        self.mutation_line_number = mutation_line_number
        self.mutated_file_name = mutated_file_name
        self.full_script = full_script

