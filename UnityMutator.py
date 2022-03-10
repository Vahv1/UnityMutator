# TODO Create MutatedScripts-folder at start of execution and delete it at the end
# TODO TEHÄÄNKÖ MUTAATIOO OLLENKAAN SCIRPTS-ALAKANSIOISSA OLEVILLE SKRIPTEILLE?
# TODO MITÄ JOS SAMALLA RIVILLÄ MONTA MUTATOITAVAA ESIM. TRANSFORM.FORWARD JA TRANSFORM.UP
# TODO MULTILINE COMMENTIT MUTATOIDAAN MYÖS, MITÄHÄN SILLE VOIS TEHDÄ
# TODO SCRIPTSTYLE PITÄÄ PALAUTTAA HTML KANSIOON JOKA LAITTAA RIVINUMEROT
import os
import shutil
from pathlib import Path
from os import path
from os import listdir
from datetime import datetime
from MutationOperator import MutationOperator
from distutils.dir_util import copy_tree
import subprocess
import time
import ResultsParser

UNITY_SCRIPT_FOLDER = ""
UNITY_TAG_MANAGER_ASSET = ""
UNITY_PROJECT_TAGS = []
TAG_MANAGER_LINE_START = "  - "  # Lines containing Tags start with this in TagManager.asset
# NOTE! This assumes original project has all scripts in a folder named "Scripts". Otherwise problems may occur.
MUTATED_SCRIPTS_FOLDER = "E:/kurssit/GRADU/UnityMutator/MutatedScripts/Scripts"
BACKUP_SCRIPTS_FOLDER = "E:/kurssit/GRADU/UnityMutator/BackupScripts"
RESULTS_FOLDER = Path("E:/kurssit/GRADU/UnityMutator/Results")
MUTATION_RUN_RESULTS_FOLDER = Path("")  # This should be set-up with timestamp as folder name when mutation is started
TEMP_RESULTS_FILE_PATH = "E:/kurssit/GRADU/UnityMutator/unity_test_results.xml"
TEMP_RESULTS_LOG_PATH = "E:/kurssit/GRADU/UnityMutator/unity_test_log.txt"
COROUTINE_MOCK_UP_PATH = "E:/kurssit/GRADU/UnityMutator/CoroutineMockUp.cs"
CS_FILE_TYPE = ".cs"
MUTATED_FILE_AFFIX = "_mutated_"

# Must be initialized with list of MutationOperator-objects
MUT_OPS = []

# Not a perfect list as comment line can also start with '*' but that can also be multiplication operator...
C_SHARP_COMMENT_SYNTAX = ["//", "/*", "*/"]


def init_mutation_operators():
    # TODO this should be done elsewhere more cleanly
    MUT_OPS.append(MutationOperator("start", [" Start()", " Start ()"], "mutate_start"))
    MUT_OPS.append(MutationOperator("awake", [" Awake()", " Awake ()"], "mutate_awake"))
    MUT_OPS.append(MutationOperator("update", [" Update()", " Update ()"], "mutate_update"))
    MUT_OPS.append(MutationOperator("fixed_update", [" FixedUpdate()", " FixedUpdate ()"], "mutate_fixed_update"))
    MUT_OPS.append(MutationOperator("destroy", [" Destroy(", " Destroy ("], "mutate_destroy"))
    MUT_OPS.append(MutationOperator("instantiate", [" Instantiate(", " Instantiate (", ".Instantiate(", ".Instantiate ("], "mutate_instantiate"))
    MUT_OPS.append(MutationOperator("gameobject_find", [" GameObject.Find(", " GameObject.Find ("], "mutate_gameobject_find"))
    MUT_OPS.append(MutationOperator("get_child", [".GetChild(", ".GetChild ("], "mutate_get_child"))
    MUT_OPS.append(MutationOperator("compare_tag", [".CompareTag(", ".CompareTag ("], "mutate_compare_tag"))
    MUT_OPS.append(MutationOperator("find_objects_with_tag", [".FindGameObjectsWithTag(", ".FindGameGameObjectsWithTag ("], "mutate_find_objects_with_tag"))
    MUT_OPS.append(MutationOperator("find_with_tag", [".FindWithTag(", ".FindWithTag ("], "mutate_find_with_tag"))
    MUT_OPS.append(MutationOperator("set_active", [".SetActive(", ".SetActive ("], "mutate_set_active"))
    MUT_OPS.append(MutationOperator("load_scene", [".LoadScene(", ".LoadScene ("], "mutate_scene_load"))
    MUT_OPS.append(MutationOperator("invoke", [" Invoke(", " Invoke ("], "mutate_invoke"))
    MUT_OPS.append(MutationOperator("invoke_repeating", [" InvokeRepeating(", " InvokeRepeating ("], "mutate_invoke_repeating"))
    MUT_OPS.append(MutationOperator("add_listener", [".AddListener(", ".AddListener ("], "mutate_add_listener"))
    MUT_OPS.append(MutationOperator("vector3_direction", ["Vector3."], "mutate_vector3_direction"))
    MUT_OPS.append(MutationOperator("vector2_direction", ["Vector2."], "mutate_vector2_direction"))
    MUT_OPS.append(MutationOperator("transform_direction", ["transform.up", "transform.forward", "transform.right"], "mutate_transform_direction"))
    MUT_OPS.append(MutationOperator("deltatime", ["Time.deltaTime"], "mutate_deltatime"))
    MUT_OPS.append(MutationOperator("fixed_deltatime", ["Time.fixedDeltaTime"], "mutate_fixed_deltatime"))
    MUT_OPS.append(MutationOperator("transform_parent", ["transform.parent"], "mutate_transform_parent"))
    MUT_OPS.append(MutationOperator("transform_set_parent", [".SetParent(", ".SetParent ("], "mutate_transform_set_parent"))
    MUT_OPS.append(MutationOperator("vector_axis", [".x", ".y", ".z"], "mutate_vector_axis"))
    MUT_OPS.append(MutationOperator("coroutine", ["StartCoroutine(", "StartCoroutine ("], "mutate_coroutine"))


def get_mut_op(name):
    """ Returns MutationOperator object by given name """
    for op in MUT_OPS:
        if op.name is name:
            return op


''' =================== MUTATION OPERATORS =================== '''


# TODO full_script_lines parametrin voi ottaa pois niistä missä ei tarvita
# Mutates Start()-lines
def mutate_start(line, full_script_lines):
    # Don't mutate Start() to Awake() if there is already Awake()-method in the script
    for script_line in full_script_lines:
        for syntax in get_mut_op("awake").syntax:
            if syntax in script_line:
                print("Script already contains both awake and start methods, so not mutating line with start()")
                return None
    else:
        new_line = line.replace("Start()", "Awake()").replace("Start ()", "Awake ()")
        return new_line


# Mutates Awake()-lines
def mutate_awake(line, full_script_lines):
    # Don't mutate Awake() to Start() if there is already Start()-method in the script
    for script_line in full_script_lines:
        for syntax in get_mut_op("start").syntax:
            if syntax in script_line:
                print("Script already contains both start and awake methods, so not mutating line with awake()")
                return None
    else:
        new_line = line.replace("Awake()", "Start()").replace("Awake ()", "Start ()")
        return new_line


# Mutates Update()-lines
def mutate_update(line, full_script_lines):
    # Don't mutate Update() to FixedUpdate() if there is already FixedUpdate()-method in the script
    for script_line in full_script_lines:
        for syntax in get_mut_op("fixed_update").syntax:
            if syntax in script_line:
                print("Script already contains both fixedupdate and update methods, so not mutating line with update()")
                return None
    else:
        new_line = line.replace("Update()", "FixedUpdate()").replace("Update ()", "FixedUpdate ()")
        return new_line


# Mutates FixedUpdate()-lines
def mutate_fixed_update(line, full_script_lines):
    # Don't mutate FixedUpdate() to Update() if there is already Update()-method in the script
    for script_line in full_script_lines:
        for syntax in get_mut_op("update").syntax:
            if syntax in script_line:
                print("Script already contains both update and fixedupdate methods, so not mutating line with fixedupdate()")
                return None
    else:
        new_line = line.replace("FixedUpdate()", "Update()").replace("FixedUpdate ()", "Update ()")
        return new_line


def mutate_deltatime(line, full_script_lines):
    new_line = line.replace("Time.deltaTime", "Time.fixedDeltaTime")
    return new_line


def mutate_fixed_deltatime(line, full_script_lines):
    new_line = line.replace("Time.fixedDeltaTime", "Time.deltaTime")
    return new_line


# Mutated Destroy()-lines by replacing parameter with null --> no object destroyed
def mutate_destroy(line, full_script_lines):
    new_line = replace_single_parameter(line, "Destroy")
    return new_line


# Mutate Instantiate()-lines by replacing parameter with gameObject --> object duplicate created
def mutate_instantiate(line, full_script_lines):
    new_line = replace_single_parameter(line, "Instantiate", mutated_parameter="gameObject", multiple_parameters=True)
    return new_line


def mutate_gameobject_find(line, full_script_lines):
    new_line = replace_single_parameter(line, "GameObject.Find", "\"InvalidObjectName\"")
    return new_line


def mutate_get_child(line, full_script_lines):
    # Get a number that isn't used in line, so we won't mutate used index to itself
    unused_index = 0
    for i in range(0, 10):
        if str(i) not in line:
            unused_index = i
            break

    # Give unused_index as the mutation parameter
    mutated_parameter = str(unused_index)
    new_line = replace_single_parameter(line, "GetChild", mutated_parameter)

    return new_line


def mutate_compare_tag(line, full_script_lines):
    mutated_tag = get_unused_tag(line)
    # Add quotes to tag so mutated parameter is correct syntax
    mutated_parameter = "\"" + mutated_tag + "\""
    # Create mutated line and script
    new_line = replace_single_parameter(line, "CompareTag", mutated_parameter)

    return new_line


def mutate_find_objects_with_tag(line, full_script_lines):
    mutated_tag = get_unused_tag(line)
    # Add quotes to tag so mutated parameter is correct syntax
    mutated_parameter = "\"" + mutated_tag + "\""
    # Create mutated line and script
    new_line = replace_single_parameter(line, "FindGameObjectsWithTag", mutated_parameter)

    return new_line


def mutate_find_with_tag(line, full_script_lines):
    mutated_tag = get_unused_tag(line)
    # Add quotes to tag so mutated parameter is correct syntax
    mutated_parameter = "\"" + mutated_tag + "\""
    # Create mutated line and script
    new_line = replace_single_parameter(line, "FindWithTag", mutated_parameter)

    return new_line


def mutate_set_active(line, full_script_lines):
    # Create new parameter that reverses the bool value of old parameter
    old_parameter = get_parameters(line, "SetActive")
    mutated_parameter = f"!({old_parameter})"
    # Create mutated line and script
    new_line = replace_single_parameter(line, "SetActive", mutated_parameter)

    return new_line


def mutate_scene_load(line, full_script_lines):
    new_line = replace_single_parameter(line, "LoadScene", "\"InvalidSceneName\"", multiple_parameters=True)
    return new_line


def mutate_invoke(line, full_script_lines):
    new_line = replace_single_parameter(line, "Invoke", "\"InvalidMethodName\"", multiple_parameters=True)
    return new_line


def mutate_invoke_repeating(line, full_script_lines):
    new_line = replace_single_parameter(line, "InvokeRepeating", "\"InvalidMethodName\"", multiple_parameters=True)
    return new_line


def mutate_add_listener(line, full_script_lines):
    """ Mutates onClick.AddListener and <unityEvent>.AddListener """

    new_line = replace_single_parameter(line, "AddListener", "delegate {}")
    return new_line


def mutate_vector3_direction(line, full_script_lines):
    if "Vector3.forward" in line:
        new_line = line.replace("Vector3.forward", "Vector3.back")
    elif "Vector3.back" in line:
        new_line = line.replace("Vector3.back", "Vector3.forward")
    elif "Vector3.up" in line:
        new_line = line.replace("Vector3.up", "Vector3.down")
    elif "Vector3.down" in line:
        new_line = line.replace("Vector3.down", "Vector3.up")
    elif "Vector3.right" in line:
        new_line = line.replace("Vector3.right", "Vector3.left")
    elif "Vector3.left" in line:
        new_line = line.replace("Vector3.left", "Vector3.right")
    elif "Vector3.zero" in line:
        new_line = line.replace("Vector3.zero", "Vector3.one")
    elif "Vector3.one" in line:
        new_line = line.replace("Vector3.one", "Vector3.zero")
    else:
        print("mutate_vector3_direction called but given line didn't contain Vector.direction")
        print(line)
        return None

    return new_line


def mutate_vector2_direction(line, full_script_lines):
    if "Vector2.up" in line:
        new_line = line.replace("Vector2.up", "Vector2.down")
    elif "Vector2.down" in line:
        new_line = line.replace("Vector2.down", "Vector2.up")
    elif "Vector2.right" in line:
        new_line = line.replace("Vector2.right", "Vector2.left")
    elif "Vector2.left" in line:
        new_line = line.replace("Vector2.left", "Vector2.right")
    elif "Vector2.zero" in line:
        new_line = line.replace("Vector2.zero", "Vector2.one")
    elif "Vector2.one" in line:
        new_line = line.replace("Vector2.one", "Vector2.zero")
    else:
        print("mutate_vector2_direction called but given line didn't contain Vector.direction")
        print(line)
        return None

    return new_line


# NOTE! possibility for bad code if there exists properties called x, z, y in custom classes
def mutate_vector_axis(line, full_script_lines):
    # Mutate x and y only between each other so works with 2D-vectors too
    if ".x" in line:
        new_line = line.replace(".x", ".y")
    elif ".y" in line:
        new_line = line.replace(".y", ".x")
    elif ".z" in line:
        new_line = line.replace(".z", ".x")
    else:
        print("mutate_vector3_axis was called but given line didn't contain syntax with .x, .y or .z")
        print(line)
        return None

    return new_line


def mutate_transform_direction(line, full_script_lines):
    if "transform.forward" in line:
        new_line = line.replace("transform.forward", "transform.up")
    elif "transform.up" in line:
        new_line = line.replace("transform.up", "transform.right")
    elif "transform.right" in line:
        new_line = line.replace("transform.right", "transform.forward")
    else:
        print("mutate_transform_direction called but given line didn't contain transform.direction")
        print(line)
        return None

    return new_line


# NOTE! May create bad code in rare cases because this just replaces line after "transform.parent = " with "null;"
def mutate_transform_parent(line, full_script_lines):
    if "transform.parent = " in line:
        splitter = "transform.parent = "
    elif "transform.parent=" in line:
        splitter = "transform.parent"
    else:
        print("Tried to mutate transform.parent assignment but no correct syntax found in line, this should NOT happen")
        print(f"line: {line}")
        return None
    old_line_start = line.split(splitter)[0]
    new_line = old_line_start + splitter + "null;"

    return new_line


def mutate_transform_set_parent(line, full_script_lines):
    old_parameters = get_parameters(line, "SetParent")
    # Don't create mutation if parent is already set as null in original
    if "null" in old_parameters:
        return None
    # Mutate parent to be set as null
    new_line = replace_single_parameter(line, "SetParent", "null", multiple_parameters=True)
    return new_line

# TODO hajoo koska luo scripts kansion ennen copy_treetä, mieti ratkasu
def mutate_coroutine(line, full_script_lines):
    # First need to create a script containing valid coroutine so coroutine calls can be mutated to use that
    os.makedirs(MUTATED_SCRIPTS_FOLDER)
    shutil.copyfile(COROUTINE_MOCK_UP_PATH, MUTATED_SCRIPTS_FOLDER + "/CoroutineMockUp.cs")
    # Mutate new line to call coroutine declared in CoroutineMockUp.cs
    new_line = replace_single_parameter(line, "StartCoroutine", "CoroutineMockUp.EmptyCoroutine()")
    return new_line


''' =================== PROGRAM FUNCTIONS =================== '''


def get_unused_tag(line):
    """ Returns Tag in Unity-Project that is not used on the given line"""
    mutated_tag = UNITY_PROJECT_TAGS[0]

    # Take new tag if selected tag was already used on the line
    tag_index = 0
    while mutated_tag in line:
        tag_index += 1
        mutated_tag = UNITY_PROJECT_TAGS[tag_index]
    return mutated_tag


def get_method_start_syntax(line, method_name):
    """ Returns syntax how given method is actually typed in given line of code
        Either "MethodName(" or "MethodName ("  """

    if method_name + "(" in line:
        return method_name + "("
    elif method_name + " (" in line:
        return method_name + " ("
    else:
        print(f"Couldn't find starting syntax for given method name ({method_name}) in the line: {line}")


# Returns string of parameter(s) given to a method in a given line of c#-code
def get_parameters(line, method_name):

    # Get syntax that starts the method in given line.
    method_start_syntax = get_method_start_syntax(line, method_name)

    # First split after method starting bracket
    split_after_method_open_bracket = line.split(method_start_syntax)
    # Save the whole line after method starting bracket
    line_after_method_start = split_after_method_open_bracket[1]

    # Index of character where method parameters end
    parameter_end_index = 0

    # Need to split after closing bracket when mutating single parameter method
    opened_brackets = 0
    # Go through string after method start syntax, and save index of method closing bracket (ends parameter)
    for i in range(0, len(line_after_method_start)):
        if line_after_method_start[i] == '(':
            opened_brackets += 1
        # If we got closing bracket and had no unclosed open brackets then save index and stop loop
        elif line_after_method_start[i] == ')':
            if opened_brackets <= 0:
                parameter_end_index = i
                break
            else:
                opened_brackets -= 1

    # Parameters are string from method opening bracket to method closing bracket
    method_parameters = line_after_method_start[0:parameter_end_index]
    return method_parameters


def replace_single_parameter(line, method_name, mutated_parameter="null", multiple_parameters=False):
    """ Replaces parameter of given method in a line of c#-code
    multiple_parameters = False --> splits from closing bracket | multiple_parameters = True --> splits from comma
    NOTE! Can only replace a single single parameter method or first parameter in multi-parameter method """

    # Get syntax that starts the method in given line.
    method_start_syntax = get_method_start_syntax(line, method_name)

    # If there are commas in the line (indicating multiple parameters) then use comma as parameter_end_char
    if ',' in line and multiple_parameters:
        parameter_end_char = ','
    # Otherwise assume there's only one parameter and parameter end char is closing bracket
    else:
        parameter_end_char = ')'

    # First split after method starting bracket
    first_split = line.split(method_start_syntax)
    # Save the line start before method name
    old_line_start = first_split[0]
    # Save the whole line after method starting bracket
    line_after_method_start = first_split[1]

    # Index of character where parameter ends
    parameter_end_index = 0

    # Need to split after closing bracket when mutating single parameter method
    if not multiple_parameters:
        opened_brackets = 0
        # Go through string after method start syntax, and save index of method closing bracket (ends parameter)
        for i in range(0, len(line_after_method_start)):
            if line_after_method_start[i] == '(':
                opened_brackets += 1
            # If we got closing bracket and had no unclosed open brackets then save index and stop loop
            elif line_after_method_start[i] == ')':
                if opened_brackets <= 0:
                    parameter_end_index = i
                    break
                else:
                    opened_brackets -= 1
    # Need to split after comma when mutating multiple parameter method, NOTE! only mutates first parameter
    else:
        # Go through string after method start syntax, and save index of first comma (ends parameter)
        for i in range(0, len(line_after_method_start)):
            if line_after_method_start[i] == parameter_end_char:
                parameter_end_index = i
                break

    # Save the line end after after method end bracket and INCLUDING method end bracket
    old_line_end = line_after_method_start[parameter_end_index:]
    # Assemble new line of code with mutated parameter
    mutated_line = old_line_start + method_start_syntax + mutated_parameter + old_line_end
    # print(f"{old_line_start}|{method_start_syntax}|{mutated_parameter}|{old_line_end}")

    return mutated_line


# Checks given line for any syntax matching mutation operators and returns matching operator or None if not found
def get_mutation_operator(code_line):
    for op in MUT_OPS:
        for syntax in op.syntax:
            if syntax in code_line:
                return op
    print("get_mutation_operator called but given code line didn't contain any syntax matching to mutation operators")
    print(code_line)
    return None


# Copies all scripts from Unity projects Scripts-folder to a new folder except for given script (that is being mutated)
def copy_non_mutated_scripts(new_dir_path, exception_file_name):
    # Copy Script folder's contents to given new folder
    shutil.copytree(BACKUP_SCRIPTS_FOLDER, new_dir_path)
    print(f"Copied all files from {BACKUP_SCRIPTS_FOLDER} to {new_dir_path}")

    # Remove copied file with name of exception_file_name.
    # This is the script that was being mutated so it will be replaced with edited file.
    os.remove(new_dir_path + "/" + exception_file_name)


# Creates Scripts folder containing one mutation in one file and returns the folder path
# This folder can be copied to Unity project and then test set can be run to see if that mutation is caught
def create_new_mutation_folder(exception_file, line_number):
    # Set name of new folder
    new_dir_path = MUTATED_SCRIPTS_FOLDER
    # Copy all script files that are not being mutated into the new folder
    copy_non_mutated_scripts(MUTATED_SCRIPTS_FOLDER, exception_file)

    return new_dir_path


# Returns true if given line contains syntax matching to mutation operators
def line_is_mutable(line):
    # Return false if line is comment
    for syntax in C_SHARP_COMMENT_SYNTAX:
        if syntax in line:
            return False

    # Return true if any mutation operator syntax is in line
    for op in MUT_OPS:
        for syntax in op.syntax:
            if syntax in line:
                print(f"syntax: {syntax} | line: {line}")
                return True
    return False


# Calls appropriate function depending on mutation operator in the given line
def create_mutation(line, full_script_lines):
    op = get_mutation_operator(line)
    mutation = op.function(line, full_script_lines)

    return mutation


# Creates all mutations for given Unity script
def mutate_script(file_name):
    print(f"Starting script mutation of {BACKUP_SCRIPTS_FOLDER}/{file_name}")

    # Read all lines of the original script to an array
    script = open(BACKUP_SCRIPTS_FOLDER + "/" + file_name, 'r')
    script_lines = script.readlines()
    script.close()

    # Go through all instances of mutable lines in the file since last mutation
    for i in range(0, len(script_lines)):

        if line_is_mutable(script_lines[i]):
            # Save old_line so it can be used later when displaying results
            old_line = script_lines[i]
            # Create mutated line
            mutated_line = create_mutation(script_lines[i], script_lines)
            # If no mutation was created, skip to next line
            if mutated_line is None:
                continue
            print(f"Mutated line: {mutated_line} | Old line: {old_line}")

            # Create a list containing mutated script in lines which is copy of old script with one line mutated
            mutated_script_lines = list(script_lines)
            mutated_script_lines[i] = mutated_line

            # Create new folder for mutated file to go into and get path to this new folder
            # This folder will be a copy of the WHOLE original Scripts-folder except for ONE file that has ONE mutation
            mutated_folder_path = create_new_mutation_folder(file_name, i)
            print(f"Created new Scripts folder to {mutated_folder_path}")

            # Create new file to mutated_folder_path
            mutated_file_path = mutated_folder_path + "/" + file_name
            new_script = open(mutated_file_path, 'w+')
            # Write the mutated lines to new file
            new_script.writelines(mutated_script_lines)
            new_script.close()
            print(f"Created mutated file to new script folder: {mutated_file_path}")

            # Replace original Unity-project's Scripts folder with mutated Scripts-folder
            if path.exists(UNITY_SCRIPT_FOLDER):
                shutil.rmtree(UNITY_SCRIPT_FOLDER)
            shutil.move(mutated_folder_path, UNITY_SCRIPT_FOLDER)
            print(f"Replaced original Scripts-folder with mutated Scripts-folder in {UNITY_SCRIPT_FOLDER}")

            # Run tests now that Unity-project has the mutated file in its Scripts-folder

            run_unity_tests()
            print(f"Test run ready, moving results.xml to {MUTATION_RUN_RESULTS_FOLDER}")

            # Get results-file path and extension separately
            results_file_name = path.splitext(path.basename(TEMP_RESULTS_FILE_PATH))[0]
            results_file_ext = path.splitext(path.basename(TEMP_RESULTS_FILE_PATH))[1]
            # Name results-file as results_EnemyHandler_line_32.xml -format
            file_name_no_ext = path.splitext(file_name)[0]
            new_results_file_name = results_file_name + "_" + file_name_no_ext + "_line_" + str(i) + results_file_ext

            # Create subfolder for results of this mutation as mutation_EnemyHandler_line_32 -format
            mutation_results_path = f"{MUTATION_RUN_RESULTS_FOLDER}/mutation_{file_name_no_ext}_line_{i}"
            os.mkdir(mutation_results_path)
            # Move test results to subfolder
            shutil.move(TEMP_RESULTS_FILE_PATH, f"{mutation_results_path}/{new_results_file_name}")
            # Create data file to same subfolder
            f = open(f"{mutation_results_path}/mutation_data_line_{i}.xml", 'w')
            # Create xml-formatted lines by removing leading and trailing white space and escaping needed characters
            xml_old_line = ResultsParser.escape_xml(old_line).strip()
            xml_new_line = ResultsParser.escape_xml(mutated_line).strip()
            f.write(f"<mutation_data original=\"{xml_old_line}\" mutation=\"{xml_new_line}\""
                    f" line_number=\"{i+1}\" file_name=\"{file_name}\"> </mutation_data>")
            f.close()
            # Create a copy of the mutated script to same subfolder
            f = open(f"{mutation_results_path}/{file_name}", 'w')
            f.writelines(mutated_script_lines)
            f.close()

            print("--------------------------------------")

    print(f"All mutations generated for script: {UNITY_SCRIPT_FOLDER}/{file_name}")
    print("======================================")


# Systematically creates mutations for all files in given Scripts folder
# Every mutation is saved to new Scripts folder which also contains all the other script files
# This way Unity-project's Scripts folder can be replaced with new Scripts for every mutation
def mutate_unity_scripts():

    print(f"Starting mutation process of folder {UNITY_SCRIPT_FOLDER}")
    print("======================================")

    # Go through all .cs-files and systematically do all possible mutations to them
    # NOTE: Uses backup-scripts folder so original scripts must be copied to backup-folder before this
    # No mutations are done to backup-folder so it always has the original scripts
    unity_script_files = listdir(BACKUP_SCRIPTS_FOLDER)
    for file in unity_script_files:
        # Ignore files with wrong extension
        if not file.endswith(CS_FILE_TYPE):
            print(f"{file} is not a .cs file so not mutating it")
            print("======================================")
        # Mutate files with .cs-extension
        else:
            mutate_script(file)


# Runs tests in Unity-project and saves results to an xml-file
def run_unity_tests(unity_project_path=None):
    # TODO tää häsellys pois tästä
    if unity_project_path is None:
        unity_project_path = Path("F:/Unity/Projects/GRADU")

    process = subprocess.run(["C:/Program Files/Unity/Hub/Editor/2020.3.20f1/Editor/Unity.exe",
                              "-runTests", "-projectPath", unity_project_path.__str__(),
                              "-logFile",  TEMP_RESULTS_LOG_PATH,
                              "-testResults", TEMP_RESULTS_FILE_PATH,
                              "-testPlatform", "PlayMode"],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)


# Adds Unity-project's tags from given TagManager.asset path to global variable UNITY_PROJECT_TAGS
def init_unity_project_tags(tag_manager_path):
    tag_manager = open(tag_manager_path, 'r')
    tag_manager_lines = tag_manager.readlines()
    tag_manager.close()

    tags_section_started = False
    for line in tag_manager_lines:
        # List of tags start after "tags:" in TagManager.asset
        if "tags:" in line:
            tags_section_started = True
        # List of tags ends after "layers:" in TagManager.asset
        elif "layers:" in line:
            break
        # Tags start with TAG_MANAGER_LINE_START and only after tags_section_started is set to true
        elif line.startswith(TAG_MANAGER_LINE_START) and tags_section_started:
            # Tag is everything after TAG_MANAGER_LINE_START
            tag = line[len(TAG_MANAGER_LINE_START):].strip()
            UNITY_PROJECT_TAGS.append(tag)

    print(f"Got tags from Unity-project. {UNITY_PROJECT_TAGS}")


def main():

    start_time = time.time()

    print("This is Unity Mutator\n"
          "A program for creating mutated source code files from Unity game scripts\n"
          "======================================")
    # TODO PITÄSKÖ ALUSSA TYHJENTÄÄ FOLDEREITA, ESIM MUTATEDSCRIPTS AINAKIN
    # Get Unity-project's Scripts-folder from user
    # TODO don't use global variables like this, pass as parameter instead? Also don't hard code values like this
    global UNITY_SCRIPT_FOLDER
    global UNITY_TAG_MANAGER_ASSET
    # TODO kato mitä näistä käytetään
    # UNITY_SCRIPT_FOLDER = input("Give Unity-project's Scripts-folder location")
    UNITY_SCRIPT_FOLDER = "F:/Unity/Projects/Gradu/Assets/Scripts"
    # UNITY_SCRIPT_FOLDER = "E:/kurssit/GRADU/UnityMutator/FakeUnityProject/Assets/Scripts"
    UNITY_TAG_MANAGER_ASSET = "F:/Unity/Projects/Gradu/ProjectSettings/TagManager.asset"

    # Create MUTATION_RUN_RESULTS_FOLDER folder as a subfolder of RESULTS_FOLDER
    global MUTATION_RUN_RESULTS_FOLDER
    t = datetime.now()
    results_path = RESULTS_FOLDER/f"results_{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
    os.mkdir(results_path)
    # Update global  MUTATION_RUN_RESULTS_FOLDER variable with path to new results folder
    MUTATION_RUN_RESULTS_FOLDER = results_path

    global BACKUP_SCRIPTS_FOLDER
    # Create backup-copy of the original scripts folder
    backups_path = f"{BACKUP_SCRIPTS_FOLDER}/BACKUP_SCRIPTS_{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
    print(f"Copying backup of original scripts to {backups_path}")
    shutil.copytree(UNITY_SCRIPT_FOLDER, backups_path)
    # Update global BACKUP_SCRIPTS_FOLDER variable with path to new backup folder
    BACKUP_SCRIPTS_FOLDER = backups_path
    print(f"Back-up copied")

    # Start mutation process of Unity-project's Scripts-folder
    mutate_unity_scripts()
    print("Mutation process finished")

    # Replace Unity-project's Scripts folder with Backup-folder at the end again
    shutil.rmtree(UNITY_SCRIPT_FOLDER)
    shutil.move(backups_path, UNITY_SCRIPT_FOLDER)
    print("Restored Unity-project's Scripts folder")

    # Create .html-file from mutation results
    ResultsParser.parse_results_to_html(MUTATION_RUN_RESULTS_FOLDER)

    # Stop execution timer
    end_time = time.time()
    print(f"Execution took {end_time-start_time} seconds")


if __name__ == "__main__":
    main()
