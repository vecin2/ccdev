import lxml.etree as ET

from emtask.ced import cedobject_factory as of


class ProcessAssertor(object):
    def __init__(self, process):
        self.process = process
        self.rootelem = process.rootnode

    def assert_params(self, expected_fields):
        assert_equal_elems(expected_fields, self.process.get_parameters())

    def assert_results(self, expected_fields):
        assert_equal_elems(expected_fields, self.process.get_results())

    def assert_imports(self, expected_imports):
        assert_equal_elems(expected_imports, self.process.get_imports())

    def assert_process_in_graph(self, process_ref, node_name):
        childprocesses = self.process.process_def.findall("ChildProcess")

        for childprocess in childprocesses:
            process_ref_elem = childprocess.find("ProcessDefinitionReference")

            if (
                childprocess.get("name") == node_name
                and process_ref_elem.get("name") == process_ref
            ):
                assert True

                return
        assert False, (
            "Not found a process node in graph with named "
            + node_name
            + " referencing "
            + process_ref
        )


def assert_equal_elems(wrapper_params, process_params):
    assert len(wrapper_params) == len(process_params)

    for i in range(len(wrapper_params)):
        assert_equal_elem(process_params[i], wrapper_params[i])


def assert_equal_elem(expected, actual):
    assert ET.tostring(expected) == ET.tostring(actual)


def assert_dataflow(dataflow, fromnode=None, tonode=None, data_entries=None):
    assert fromnode == dataflow.find("FromNode").get("name")
    assert tonode == dataflow.find("ToNode").get("name")
    dataflowentries = dataflow.findall("DataFlowEntry")
    assert len(data_entries) == len(dataflowentries)
    param_assignment = dataflowentries[0].find("FromField").find("ParameterAssignment")
    assert param_assignment is not None
    fromfield = data_entries[0][0]
    assert fromfield == param_assignment.find("Verbatim").text
    field_ref = dataflowentries[0].find("ToField").find("FieldDefinitionReference")
    tofield = data_entries[0][1]
    assert tofield == field_ref.get("name")


def test_process_wrapper_when_process_has_object_params_imports_object(ced):
    process = ced.new_process("PRJContact.Implementation.Contact.Verbs.ViewContact")
    imported_process = ced.new_process(
        "PRJContact.Implementation.Contact.Processes.InlineView"
    )
    inlineview_import = of.make_import(imported_process.path)
    process.add_import(inlineview_import)
    inlineview_field = of.make_object_field("InlineView", "inlineView")
    process.add_field(inlineview_field)
    process.mark_as_parameter("inlineView")
    street_field = of.make_object_field("IContext", "context")
    process.add_field(street_field)
    process.mark_as_parameter("context")
    process.mark_as_result("context")
    output_field = of.make_field("Integer", "output")
    process.add_field(output_field)
    process.mark_as_result("output")
    wrapper_path = "PRJContact.Implementation.Contact.Verbs.ViewContactWrapper"
    wrapper_process = process.wrapper(wrapper_path)

    process.save()
    imported_process.save()
    wrapper_process.save()

    # check wrapper has field inlineView as parameter and imports the neccesary
    wrapper_assertor = ProcessAssertor(wrapper_process)
    wrapper_assertor.assert_params([inlineview_field, street_field])
    wrapper_assertor.assert_results([street_field, output_field])
    wrapper_assertor.assert_imports([inlineview_import])
    wrapper_assertor.assert_process_in_graph("ViewContact", "viewContact")

    transitions = wrapper_process.process_def.findall("Transition")
    assert 2 == len(transitions)
    assert transitions[0].find("StartNodeReference") is not None
    assert "viewContact" == transitions[0].find("ToNode").get("name")
    assert transitions[1].find("EndNodeReference") is not None
    assert "viewContact" == transitions[1].find("FromNode").get("name")
    fieldstores = wrapper_process.process_def.findall("ThisNode")
    assert 1 == len(fieldstores)
    assert "fieldStore0" == fieldstores[0].get("name")
    dataflows = wrapper_process.process_def.findall("DataFlow")
    assert 2 == len(dataflows)
    assert_dataflow(
        dataflows[0],
        fromnode="fieldStore0",
        tonode="viewContact",
        data_entries=[("inlineView", "inlineView"), ("address", "address")],
    )
    assert_dataflow(
        dataflows[1],
        fromnode="viewContact",
        tonode="fieldStore0",
        data_entries=[("context", "context"), ("output", "output")],
    )


def test_add_import(ced):
    mainprocess = ced.new_process("Test.MainProcess")
    childprocess = ced.new_process("Test.Processes.ChildProcess")

    mainprocess.add_import(of.make_import(childprocess.path))

    import_elem = mainprocess.rootnode.findall("ImportDeclaration")[0]
    packagename_elems = import_elem.find("PackageSpecifier").findall("PackageName")
    assert "ChildProcess" == import_elem.get("name")
    assert "Test" == packagename_elems[0].get("name")
    assert "Processes" == packagename_elems[1].get("name")
    package_entry_ref = import_elem.find("PackageEntryReference")
    assert "ChildProcess" == package_entry_ref.get("name")


def test_add_all_basic_types_fields(ced):
    process = ced.new_process("Test.TestProcess")
    process.add_field(of.make_field("String", "name1"))
    process.add_field(of.make_field("Number", "referenceNo"))
    process.add_field(of.make_field("Integer", "streetNumber"))
    process.add_field(of.make_field("Float", "partialAmount"))
    # defaults to precision 42 and scale 1
    process.add_field(of.make_field("Decimal", "totalAmount"))
    process.add_field(of.make_field("Character", "oneLetter"))
    process.add_field(of.make_field("Date", "dob"))
    assert process.get_field("name1") is not None
    assert process.get_field("referenceNo") is not None
    assert process.get_field("streetNumber") is not None
    assert process.get_field("partialAmount") is not None
    assert process.get_field("totalAmount") is not None
    assert process.get_field("oneLetter") is not None
    assert process.get_field("dob") is not None
    # todo type Form


def test_add_object_field(ced):
    childprocess = ced.new_process("Test.TestChildProcess")
    process = ced.new_process("Test.TestMainProcess")
    field = of.make_object_field("TestChildProcess", "childProcess")
    process.add_field(field)
    returned_field = process.get_field("childProcess")
    assert_equal_elem(returned_field, field)


def test_add_parameters(ced):
    process = ced.new_process("Test.TestProcessParameter")
    process.add_field(of.make_field("String", "street"))
    process.add_field(of.make_field("Number", "streetNumber"))
    process.mark_as_parameter("street")
    process.mark_as_parameter("streetNumber")
    assert process.get_field("street") is not None
    assert "street" == process.get_parameters()[0].get("name")
    assert process.get_field("streetNumber") is not None
    assert "streetNumber" == process.get_parameters()[1].get("name")


def test_add_result(ced):
    process = ced.new_process("Test.TestProcessResult")
    process.add_field(of.make_field("String", "street"))
    process.add_field(of.make_field("Number", "streetNumber"))

    process.mark_as_result("street")
    process.mark_as_result("streetNumber")

    assert process.get_field("street") is not None
    assert "street" == process.get_results()[0].get("name")
    assert process.get_field("streetNumber") is not None
    assert "streetNumber" == process.get_results()[1].get("name")


def test_add_as_param_and_result(ced):
    process = ced.new_process("Test.TestProcessParamAndResult")
    process.add_field(of.make_field("String", "street"))
    process.mark_as_parameter("street")
    process.mark_as_result("street")

    assert process.get_field("street") is not None
    assert "street" == process.get_parameters()[0].get("name")
    assert "street" == process.get_results()[0].get("name")


def test_add_procedure(ced):
    process = ced.new_process("Test.TestProcessResult")
    process.add_general_procedure("setUp")

    process.save()

    procedure = process.get_procedure("setUp")
    assert procedure is not None
    assert "Test.TestProcessResult.setUp" == procedure.path


def test_add_procedure2(ced):
    procedure = of.make_procedure(ced.root, "Test.TestBuildProcedure.procedure1")
    procedure.add_local_vars(age="Integer")
    # process.add_general_procedure(
    #    "setUp",
    #    parameter="Integer accountId",
    #    local_vars="Integer age, TestEmTaskProcess process",
    #    returns="Integer",
    #    contents="var i=0",
    # )
