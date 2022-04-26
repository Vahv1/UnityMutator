import os
import shutil
import UnityMutator
import ResultsParser
import time
from os import path
from pathlib import Path
from datetime import datetime

# Mutations created by CREAM must be moved to this folder before running Unity tests
CREAM_MUTATED_PROJECTS_FOLDER = Path("E:/kurssit/GRADU/ts3_afterUOI/MutatedCode")

RESULTS_FOLDER = Path("E:/kurssit/GRADU/UnityMutator/Results")
MUTATION_RUN_RESULTS_FOLDER = Path("")  # This should be set-up with timestamp as folder name when mutation is started
TEMP_RESULTS_FILE_PATH = Path("E:/kurssit/GRADU/UnityMutator/unity_test_results.xml")
TEMP_RESULTS_LOG_PATH = Path("E:/kurssit/GRADU/UnityMutator/unity_test_log.txt")


def run_tests_for_cream_mutated_files():
    mutated_projects = os.listdir(CREAM_MUTATED_PROJECTS_FOLDER)

    # Run unity tests for each folder containing mutated unity project
    for proj in mutated_projects:
        project_path = CREAM_MUTATED_PROJECTS_FOLDER / proj

        UnityMutator.run_unity_tests(project_path)
        print(f"Test run ready, moving results.xml to {MUTATION_RUN_RESULTS_FOLDER}")

        # Get results-file path and extension separately
        results_file_name = path.splitext(path.basename(TEMP_RESULTS_FILE_PATH))[0]
        results_file_ext = path.splitext(path.basename(TEMP_RESULTS_FILE_PATH))[1]
        # Get mutation name, Gradu_AOR1 --> AOR1
        mutation_name = proj.__str__().split('_')[1]
        # Name results-file as unity_test_results_AOR1.xml -format
        new_results_file_name = results_file_name + "_" + mutation_name + results_file_ext

        # Create subfolder for results of this mutation as mutation_AOR1 -format
        mutation_results_path = MUTATION_RUN_RESULTS_FOLDER / f"mutation_{mutation_name}"
        os.mkdir(mutation_results_path)
        # Move test results to subfolder
        new_results_file_path = mutation_results_path / new_results_file_name
        shutil.move(TEMP_RESULTS_FILE_PATH, new_results_file_path)

        # Create data file to same subfolder
        f = open(mutation_results_path/f"mutation_data_{mutation_name}.xml", "w")

        # Can't get old line and new line from CREAM results
        '''
        xml_old_line = ResultsParser.escape_xml(old_line).strip()
        xml_new_line = ResultsParser.escape_xml(mutated_line).strip()
        '''

        f.write(f"<mutation_data original=\"Unknown (See matching mutant from CREAM) \""
                f" mutation=\"Unknown (See matching mutant from CREAM)\""
                f" line_number=\"Unknown (See matching mutant from CREAM)\""
                f" file_name=\"{mutation_name}\"> </mutation_data>")
        f.close()

        # Can't create copy of mutated script because can't get info which script was mutated by CREAM
        '''
        # Create a copy of the mutated script to same subfolder
        f = open(f"{mutation_results_path}/{file_name}", 'w')
        f.writelines(mutated_script_lines)
        f.close()
        '''

        print("--------------------------------------")


def main():
    start_time = time.time()

    print("This is Unity Mutator - CreamUnityTestRunner\n"
          "A program for running Unity-tests on Cream generated mutants of Unity-projects\n"
          "======================================")

    # Create and set name for MUTATION_RUN_RESULTS_FOLDER where Unity test results of each mutation will be saved
    t = datetime.now()
    global MUTATION_RUN_RESULTS_FOLDER
    results_path = RESULTS_FOLDER/f"results_CREAM_{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
    os.mkdir(results_path)
    MUTATION_RUN_RESULTS_FOLDER = results_path

    run_tests_for_cream_mutated_files()

    ResultsParser.parse_results_to_html(MUTATION_RUN_RESULTS_FOLDER)

    # Stop execution timer
    end_time = time.time()
    print(f"Execution took {end_time-start_time} seconds")


if __name__ == "__main__":
    main()
