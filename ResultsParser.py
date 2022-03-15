# Parses Unity test result information from multiple .xml-files into a single readable .html-document

import xml.etree.ElementTree as ET
from os import path
from os import listdir
from pathlib import Path
from jinja2 import Environment, PackageLoader
from TestRun import TestRun
from TestRun import TestResult

# TODO TEMP FOR TESTING
RESULTS_FOLDER = Path("E:/kurssit/GRADU/UnityMutator/Results/results_2022_3_15_14_25_3")

# Names of css-classes for highlighting killed and survived mutants in html
KILLED_CSS_CLASS = "killed"
SURVIVED_CSS_CLASS = "survived"


# Escapes characters from given string to it's valid xml
def escape_xml(s):
    escaped_s = s.replace("&", "&amp;").replace("\'", "&apos;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
    return escaped_s


def escape_html(s):
    escaped_s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return escaped_s


# Returns test results read from Unity Test Framework's results.xml file as a TestResult-object
def str_to_test_result(result_str):
    if result_str == "Failed(Child)" or result_str == "Failed":
        return "killed"
    elif result_str == "Passed":
        return "survived"


def parse_test_run(result_file_path, data_file_path, full_script=None):
    """
    Creates a TestRun-object containing info from a test run of a single mutation.
    If no full_script is given, assumes that test run was parsed from CREAM test run results
    and because of that full_script couldn't be obtained.
    """
    # Get results and data as element tree
    result_root = ET.parse(result_file_path).getroot()
    data_root = ET.parse(data_file_path).getroot()

    # Read data from .xmls to variables
    final_result = str_to_test_result(result_root.attrib["result"])
    tests_run = result_root.attrib["total"]
    tests_passed = result_root.attrib["passed"]
    tests_failed = result_root.attrib["failed"]
    original_line = data_root.attrib["original"]
    mutated_line = data_root.attrib["mutation"]
    mutation_line_number = data_root.attrib["line_number"]
    mutated_file_name = data_root.attrib["file_name"]

    if full_script is not None:
        # Read the whole mutated script so it can be displayed in html-page
        full_script_file = open(full_script, 'r')
        script_lines = full_script_file.readlines()
        # Escaped needed characters for html-validity
        escaped_script_lines = [escape_html(line) for line in script_lines]
        # Add <code> and </code> tags to code line starts and ends
        formatted_script_lines = ["<code>" + line.replace('\n', '</code>\n') for line in escaped_script_lines]

        # Format mutated line using correct css-class
        mutated_script_line = formatted_script_lines[int(mutation_line_number) - 1]
        css_class = SURVIVED_CSS_CLASS if final_result == TestResult.PASSED else KILLED_CSS_CLASS
        mutated_script_line = mutated_script_line.replace("<code>", f"<code class=\"{css_class}\">")

        # Ending /code tag because end of file probably doesn't have new line which would have been replaced earlier
        formatted_script_lines.append("</code>")
        # Change the mutated line in formatted_script_lines list
        formatted_script_lines[int(mutation_line_number) - 1] = mutated_script_line

        # Concatenate lines to a single string for easy displaying in .html
        formatted_script = ''.join(formatted_script_lines)
    else:
        formatted_script = "No full script available, if this test run was done to CREAM mutants then see CREAM log" \
                           " for full scripts."

    # Create TestRun object with all data
    test_run = TestRun(final_result, tests_run, tests_passed, tests_failed, original_line,
                       mutated_line, mutation_line_number, mutated_file_name, formatted_script)

    return test_run


# Returns dictionary of data related to whole set of test runs
def get_mutation_set_data(test_runs):
    total_mutations = len(test_runs)

    if total_mutations <= 0:
        print("get_mutation_set_data was given a list of 0 mutations")
        print("THIS SHOULD NOT HAPPEN")

    survived = get_survived_amt(test_runs)  # Passed test set means mutation survived
    killed = total_mutations - survived   # Failed test set means mutation was killed
    mutation_score = killed / total_mutations

    data_dict = {
        "total_mutations": total_mutations,
        "survived": survived,
        "killed": killed,
        "mutation_score": mutation_score
    }
    return data_dict


# Returns amount of passed tests from a list of test runs
def get_survived_amt(test_runs):
    survived = 0
    for t in test_runs:
        if t.final_result == "survived":
            survived += 1
    return survived


# Creates html-file of results with given parameters
def create_html(test_runs):

    mutation_set_data = get_mutation_set_data(test_runs)

    env = Environment(loader=PackageLoader('UnityMutator'))
    template = env.get_template('index.html')

    root = path.dirname(path.abspath(__file__))
    filename = path.join(root, 'html', 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            test_runs=test_runs,
            total_amt=mutation_set_data["total_mutations"],
            survived_amt=mutation_set_data["survived"],
            killed_amt=mutation_set_data["killed"],
            mutation_score=mutation_set_data["mutation_score"]
        ))


def parse_results_to_html(results_folder):
    """
    Main function that forms html report from given folder containing Unity test run results and mutation data
    related to the test runs.
    """
    # Create a list of TestRun-objects containing info from test run of each mutation
    test_runs = []

    # Get absolute path of folders in results_folder
    result_folders = [results_folder/file for file in listdir(results_folder)]

    # Go through all test run results and data and parse a list of TestRuns from them
    for directory in result_folders:
        result_file, data_file, full_script = None, None, None
        for file in listdir(directory):
            if "results" in file:
                result_file = f"{directory}/{file}"
            elif "data" in file:
                data_file = f"{directory}/{file}"
            elif path.splitext(file)[1] == ".cs":
                full_script = f"{directory}/{file}"
            else:
                print("Unexpected file in test results folder:")
                print(directory/file)
        # print(f"parsing next: {result_file}, {data_file}")
        test_run = parse_test_run(result_file, data_file, full_script)
        test_runs.append(test_run)

    # Create .html-file containing summary of mutation set results
    create_html(test_runs)


def main():
    parse_results_to_html(RESULTS_FOLDER)


if __name__ == "__main__":
    main()
    print("Ran ResultsParser.py")
else:
    print("ResultsParser.py was imported from another module")
