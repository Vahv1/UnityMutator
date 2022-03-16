from unittest import TestCase
from pathlib import Path
import shutil
import UnityMutator
import ResultsParser

script_with_only_start = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Enemy_with_start_and_both_updates.cs"
script_with_only_awake = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Projectile_with_only_awake.cs"
script_with_start_and_awake = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Enemy_with_awake_and_start.cs"
script_with_only_update = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Enemy_with_only_update.cs"
script_with_only_fixedupdate = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Enemy_with_only_fixedupdate.cs"
script_with_both_updates = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Enemy_with_start_and_both_updates.cs"
filler_script = "E:/kurssit/GRADU/UnityMutator/UnitTestData/Projectile_with_only_awake.cs"
test_tag_manager = "E:/kurssit/GRADU/UnityMutator/UnitTestData/TagManager.asset"
fake_unity_script = "E:/kurssit/GRADU/UnityMutator/FakeUnityProject/Assets/Scripts/GameManager.cs"
TEMP_RESULTS_FILE_PATH = Path("E:/kurssit/GRADU/UnityMutator/unity_test_results.xml")


class Test(TestCase):

    def setUp(self):
        UnityMutator.init_mutation_operators()

    # =========== BASE FUNCTIONS ===========

    def test_multi_param_replace(self):
        mutated_line = UnityMutator.replace_single_parameter(
            "Missile clone = Instantiate(projectile, transform.position, transform.rotation);",
            "Instantiate", mutated_parameter="gameObject", multiple_parameters=True)
        self.assertEqual("Missile clone = Instantiate(gameObject, transform.position, transform.rotation);", mutated_line)

    def test_single_param_replace_multiple_brackets(self):
        mutated_line = UnityMutator.replace_single_parameter("Destroy(GetComponent<BoxCollider>());", "Destroy")
        self.assertEqual("Destroy(null);", mutated_line)

    def test_single_param_replace_no_brackets(self):
        mutated_line = UnityMutator.replace_single_parameter("Destroy(MyObject);", "Destroy")
        self.assertEqual("Destroy(null);", mutated_line)

    def test_tag_getter(self):
        UnityMutator.UNITY_PROJECT_TAGS = []
        UnityMutator.init_unity_project_tags(test_tag_manager)
        self.assertEqual(len(UnityMutator.UNITY_PROJECT_TAGS), 9)

    def test_get_parameter(self):
        parameter = UnityMutator.get_parameters("enemy.SetActive(GameIsStarted());", "SetActive")
        self.assertEqual("GameIsStarted()", parameter)

    # =========== MUTATION FUNCTIONS ===========

    # ===== LIFECYCLE METHODS =====
    """
    def test_mutate_start_with_awake(self):
        script = open(script_with_start_and_awake, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Start ()", script_lines)
        self.assertEqual(None, mutated_line)

    def test_mutate_start_no_awake(self):
        script = open(script_with_only_start, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Start ()", script_lines)
        self.assertEqual("void Awake ()", mutated_line)

    def test_mutate_awake_with_start(self):
        script = open(script_with_start_and_awake, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Awake()", script_lines)
        self.assertEqual(None, mutated_line)

    def test_mutate_awake_no_start(self):
        script = open(script_with_only_awake, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Awake()", script_lines)
        self.assertEqual("void Start()", mutated_line)

    def test_mutate_update_with_fixedupdate(self):
        script = open(script_with_both_updates, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Update ()", script_lines)
        self.assertEqual(None, mutated_line)

    def test_mutate_update_no_fixedupdate(self):
        script = open(script_with_only_update, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void Update ()", script_lines)
        self.assertEqual("void FixedUpdate ()", mutated_line)

    def test_mutate_fixedupdate_with_update(self):
        script = open(script_with_both_updates, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void FixedUpdate()", script_lines)
        self.assertEqual(None, mutated_line)

    def test_mutate_fixedupdate_no_start(self):
        script = open(script_with_only_fixedupdate, 'r')
        script_lines = script.readlines()
        script.close()

        mutated_line = UnityMutator.create_mutation("void FixedUpdate()", script_lines)
        self.assertEqual("void Update()", mutated_line)

    def test_mutate_deltatime(self):
        mutated_line = UnityMutator.create_mutation(
            "transform.Rotate(0, 0, degreesPerSecond * Time.deltaTime);", filler_script)
        self.assertEqual("transform.Rotate(0, 0, degreesPerSecond * Time.fixedDeltaTime);", mutated_line)

    def test_mutate_fixed_deltatime(self):
        mutated_line = UnityMutator.create_mutation(
            "transform.Rotate(0, 0, degreesPerSecond * Time.fixedDeltaTime);", filler_script)
        self.assertEqual("transform.Rotate(0, 0, degreesPerSecond * Time.deltaTime);", mutated_line)
    """

    # ===== STUFF =====

    def test_mutate_destroy(self):
        mutated_line = UnityMutator.create_mutation("  Destroy(GetComponent<BoxCollider>());", filler_script)
        self.assertEqual("  Destroy(null);", mutated_line)

    def test_mutate_instantiate(self):
        mutated_line = UnityMutator.create_mutation(
            "Missile clone = Instantiate(projectile, transform.position, transform.rotation);", filler_script)
        self.assertEqual("Missile clone = Instantiate(gameObject, transform.position, transform.rotation);", mutated_line)

    def test_mutate_gameobject_find(self):
        mutated_line = UnityMutator.create_mutation(
            "hand = GameObject.Find(\"Monster/Arm/Hand\");", filler_script)
        self.assertEqual("hand = GameObject.Find(\"InvalidObjectName\");", mutated_line)

    def test_mutate_get_child(self):
        mutated_line = UnityMutator.create_mutation("child = this.gameObject.transform.GetChild(0);", filler_script)
        self.assertEqual("child = this.gameObject.transform.GetChild(1);", mutated_line)

    def test_mutate_compare_tag(self):
        UnityMutator.UNITY_PROJECT_TAGS = []
        UnityMutator.init_unity_project_tags(test_tag_manager)

        mutated_line = UnityMutator.create_mutation("if (other.gameObject.CompareTag(\"Player\"))", filler_script)
        self.assertEqual("if (other.gameObject.CompareTag(\"Enemy\"))", mutated_line)

    def test_mutate_find_objects_with_tag(self):
        UnityMutator.UNITY_PROJECT_TAGS = []
        UnityMutator.init_unity_project_tags(test_tag_manager)

        mutated_line = UnityMutator.create_mutation(
            "respawns = GameObject.FindGameObjectsWithTag(\"Respawn\");", filler_script)
        self.assertEqual("respawns = GameObject.FindGameObjectsWithTag(\"Player\");", mutated_line)

    def test_mutate_find_with_tag(self):
        UnityMutator.UNITY_PROJECT_TAGS = []
        UnityMutator.init_unity_project_tags(test_tag_manager)

        mutated_line = UnityMutator.create_mutation("player = GameObject.FindWithTag(\"Player\");", filler_script)
        self.assertEqual("player = GameObject.FindWithTag(\"Enemy\");", mutated_line)

    def test_mutate_set_active(self):
        mutated_line = UnityMutator.create_mutation("enemy.SetActive(GameIsStarted());", filler_script)
        self.assertEqual("enemy.SetActive(!(GameIsStarted()));", mutated_line)

    def test_mutate_scene_load(self):
        mutated_line = UnityMutator.create_mutation(
            "SceneManager.LoadScene(nextSceneName, LoadSceneMode.Additive);", filler_script)
        self.assertEqual("SceneManager.LoadScene(\"InvalidSceneName\", LoadSceneMode.Additive);", mutated_line)

    def test_mutate_invoke(self):
        mutated_line = UnityMutator.create_mutation("  Invoke(\"Explode\", 1);", filler_script)
        self.assertEqual("  Invoke(\"InvalidMethodName\", 1);", mutated_line)

    def test_mutate_invoke_repeating(self):
        mutated_line = UnityMutator.create_mutation("  InvokeRepeating(\"Shoot\", 1, 0.5f);", filler_script)
        self.assertEqual("  InvokeRepeating(\"InvalidMethodName\", 1, 0.5f);", mutated_line)

    def test_mutate_onclick_add_listener(self):
        mutated_line = UnityMutator.create_mutation("homeButton.onClick.AddListener(OpenHomeMenu);", filler_script)
        self.assertEqual("homeButton.onClick.AddListener(delegate {});", mutated_line)

    def test_mutate_event_add_listener(self):
        mutated_line = UnityMutator.create_mutation("winEvent.AddListener(LaunchConfetti);", filler_script)
        self.assertEqual("winEvent.AddListener(delegate {});", mutated_line)

    def test_mutate_coroutine(self):
        mutated_line = UnityMutator.create_mutation("yield return StartCoroutine(WaitAndPrint(2.0f));", filler_script)
        self.assertEqual("yield return StartCoroutine(CoroutineMockUp.EmptyCoroutine());", mutated_line)

    def test_mutate_active_self(self):
        mutated_line = UnityMutator.create_mutation("if (myObj.activeSelf && gameStarted == true)", filler_script)
        self.assertEqual("if (myObj.activeInHierarchy && gameStarted == true)", mutated_line)

    def test_mutate_active_in_hierarchy(self):
        mutated_line = UnityMutator.create_mutation("activityState = obj1.activeInHierarchy && obj2.activeInHierarchy", filler_script)
        self.assertEqual("activityState = obj1.activeSelf && obj2.activeSelf", mutated_line)

    # =====  VECTOR3 DIRECTIONS =====

    def test_mutate_vector3_forward(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.forward * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.back * 10.0f;", mutated_line)

    def test_mutate_vector3_back(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.back * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.forward * 10.0f;", mutated_line)

    def test_mutate_vector3_up(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.up * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.down * 10.0f;", mutated_line)

    def test_mutate_vector3_down(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.down * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.up * 10.0f;", mutated_line)

    def test_mutate_vector3_right(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.right * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.left * 10.0f;", mutated_line)

    def test_mutate_vector3_left(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.left * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.right * 10.0f;", mutated_line)

    def test_mutate_vector3_zero(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.zero * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.one * 10.0f;", mutated_line)

    def test_mutate_vector3_one(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector3.one * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector3.zero * 10.0f;", mutated_line)

    # =====  VECTOR2 DIRECTIONS =====

    def test_mutate_vector2_up(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.up * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.down * 10.0f;", mutated_line)

    def test_mutate_vector2_down(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.down * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.up * 10.0f;", mutated_line)

    def test_mutate_vector2_right(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.right * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.left * 10.0f;", mutated_line)

    def test_mutate_vector2_left(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.left * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.right * 10.0f;", mutated_line)

    def test_mutate_vector2_zero(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.zero * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.one * 10.0f;", mutated_line)

    def test_mutate_vector2_one(self):
        mutated_line = UnityMutator.create_mutation("child.position += Vector2.one * 10.0f;", filler_script)
        self.assertEqual("child.position += Vector2.zero * 10.0f;", mutated_line)

    # ===== OTHER VECTORS =====

    def test_mutate_vector_axis_x(self):
        mutated_line = UnityMutator.create_mutation("m_NewPosition.x = m_XValue;", filler_script)
        self.assertEqual("m_NewPosition.y = m_XValue;", mutated_line)

    def test_mutate_vector_axis_y(self):
        mutated_line = UnityMutator.create_mutation("m_NewPosition.y = m_XValue;", filler_script)
        self.assertEqual("m_NewPosition.x = m_XValue;", mutated_line)

    def test_mutate_vector_axis_z(self):
        mutated_line = UnityMutator.create_mutation("m_NewPosition.z = m_XValue;", filler_script)
        self.assertEqual("m_NewPosition.x = m_XValue;", mutated_line)

    def test_mutate_magnitude(self):
        mutated_line = UnityMutator.create_mutation("if (offset.magnitude > maxDistance)", filler_script)
        self.assertEqual("if (offset.sqrMagnitude > maxDistance)", mutated_line)

    def test_mutate_sqr_magnitude(self):
        mutated_line = UnityMutator.create_mutation("float sqrLen = offset.sqrMagnitude;", filler_script)
        self.assertEqual("float sqrLen = offset.magnitude;", mutated_line)

    # ===== TRANSFORM DIRECTION =====

    def test_mutate_transform_forward(self):
        mutated_line = UnityMutator.create_mutation("rb.velocity = transform.forward * speed;", filler_script)
        self.assertEqual("rb.velocity = transform.up * speed;", mutated_line)

    def test_mutate_transform_up(self):
        mutated_line = UnityMutator.create_mutation("rb.velocity = transform.up * speed;", filler_script)
        self.assertEqual("rb.velocity = transform.right * speed;", mutated_line)

    def test_mutate_transform_right(self):
        mutated_line = UnityMutator.create_mutation("rb.velocity = transform.right * speed;", filler_script)
        self.assertEqual("rb.velocity = transform.forward * speed;", mutated_line)

    def test_mutate_transform_parent(self):
        mutated_line = UnityMutator.create_mutation("enemy.transform.parent = enemyParentObject;", filler_script)
        self.assertEqual("enemy.transform.parent = null;", mutated_line)

    def test_mutate_set_parent(self):
        mutated_line = UnityMutator.create_mutation("child.transform.SetParent(newParent, false);", filler_script)
        self.assertEqual("child.transform.SetParent(null, false);", mutated_line)

    def test_mutate_set_parent_old_is_null(self):
        mutated_line = UnityMutator.create_mutation("child.transform.SetParent(null);", filler_script)
        self.assertEqual(None, mutated_line)

    # ===== GENERAL FUNCTIONS =====
    def test_create_unity_test_result_file_name(self):
        result_file_name = UnityMutator.create_unity_test_result_file_name("PlayerController", 32)
        self.assertEqual("unity_test_results_PlayerController_line_32.xml", result_file_name)

    """def test_create_single_mutation_results_folder(self):
        UnityMutator.MUTATION_RUN_RESULTS_FOLDER = Path("E:/kurssit/GRADU/UnityMutator/UnitTestData/"
                                                        "TestDataMutationResults_00_00_00_00_00_00")
        # Read mock up script to array
        script = open(fake_unity_script, 'r')
        script_lines = script.readlines()
        script.close()
        # Assign other variables that will be given as arguments
        file_name = "GameManager.cs"
        mutation_line_number = 14
        old_line = "StartCoroutine(FakeCoroutine());"
        new_line = "StartCoroutine(CoroutineMockUp.EmptyCoroutine());"

        UnityMutator.create_single_mutation_results_folder(file_name, mutation_line_number, script_lines, old_line, new_line)

        # Copy original unity_test_results.xml back to UnityMutator-folder where it was
        # TODO
        shutil.copyfile(source, TEMP_RESULTS_FILE_PATH)"""

    # ===== RESULTSPARSER =====
    def test_xml_escape(self):
        original_string = "RaycastHit2D hit = Physics2D.Raycast(rb.positiondir, 3, 1 << LayerMask.NameToLayer(\"NPC\"))"
        new_string = ResultsParser.escape_xml(original_string)
        self.assertEqual(
            "RaycastHit2D hit = Physics2D.Raycast(rb.positiondir, 3, 1 &lt;&lt; LayerMask.NameToLayer(&quot;NPC&quot;))",
            new_string)

        original_string = "if (letter1 == 'A' && letter2 == 'B' && letterAmount > 26) weHaveAlphabet = true"
        new_string = ResultsParser.escape_xml(original_string)
        self.assertEqual(
            "if (letter1 == &apos;A&apos; &amp;&amp; letter2 == &apos;B&apos; &amp;&amp; letterAmount &gt; 26) weHaveAlphabet = true",
            new_string)


    # ===== CREAMUNITYTESTRUNNER =====


