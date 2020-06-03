import os
from copy import deepcopy
from pathlib import Path

import lxml.etree as ET
from lxml.etree import CDATA


def make_import(childprocess_path):
    packagenames = childprocess_path.split(".")
    import_elem = ET.Element("ImportDeclaration", name=packagenames[-1])
    pkg_spec = ET.SubElement(import_elem, "PackageSpecifier", name="")

    for packagename in packagenames[:-1]:
        ET.SubElement(pkg_spec, "PackageName", name=packagename)
    ET.SubElement(import_elem, "PackageEntryReference", name=packagenames[-1])

    return import_elem


def make_field(field_type, field_name):
    field = ET.Element(
        field_type + "Field",
        designNodes="",
        isAttribute="false",
        length="0",
        name=field_name,
    )
    locale = ET.SubElement(field, field_type + "Field", locale="")
    ET.SubElement(locale, "Format")

    return field


def add_process_def_node(parent, name):
    attribs = {
        "appearsInHistory": "true",
        "cyclic": "false",
        "designNotes": "Undefined",
        "exceptionStrategy": "1",
        "icon": "",
        "isPrivate": "false",
        "logicalDatabaseConnection": "",
        "name": name,
        "nested": "false",
        "pointOfNoReturn": "false",
        "transactionBehaviour": "TX_NOT_SUPPORTED",
        "version": "10",
        "waitOnChildren": "false",
    }

    return ET.SubElement(parent, "ProcessDefinition", attribs)


def new_process_etree(name):
    root = ET.Element("PackageEntry")
    process_def = add_process_def_node(root, name)
    ET.SubElement(process_def, "StartNode", displayName="", name="", x="16", y="32")
    ET.SubElement(process_def, "EndNode", displayName="", name="", x="240", y="32")
    # transition = ET.SubElement(process_def, "Transition", isExceptionTransition="false")
    # ET.SubElement(transition, "StartNodeReference", name="")
    # ET.SubElement(transition, "EndNodeReference", name="")
    # graph_node_list = ET.SubElement(transition, "GraphNodeList", name="")
    # ET.SubElement(
    #    graph_node_list,
    #    "GraphNode",
    #    icon="",
    #    isLabelHolder="true",
    #    label="",
    #    name="",
    #    x="128",
    #    y="32",
    # )
    ET.SubElement(process_def, "BuilderInfo", name="")
    ET.SubElement(process_def, "TopicScope", defineTopicScope="false", name="")

    return root


def new_procedure_etree(name):
    procedure = ET.Element(
        "Procedure",
        designNotes="",
        isTPL="false",
        Language="EcmaScript",
        name=name,
        nested="false",
        version="10",
    )
    ET.SubElement(procedure, "ReferenceParameters")
    ET.SubElement(procedure, "ProcedureLocals")
    ET.SubElement(procedure, "Verbatim", fieldName="text")

    return procedure


def make_process(root, path):
    process_name = path.split(".")[-1]

    return Process(root, path, ET.ElementTree(new_process_etree(process_name)))


def make_childprocess(process_ref_name, coordinates):
    instance_name = process_ref_name[0].lower() + process_ref_name[1:]
    childprocess = ET.Element(
        "ChildProcess",
        displayName="",
        executeAsAsynchronous="false",
        name=instance_name,
        x=coordinates[0],
        y=coordinates[1],
    )
    ET.SubElement(
        childprocess,
        "ProcessDefinitionReference",
        name=process_ref_name,
        nested="false",
    )

    return childprocess


def make_start_transition(childprocess_name, coordinates):
    transition = ET.Element("Transition", isExceptionTransition="false")
    ET.SubElement(transition, "StartNodeReference", name="")
    ET.SubElement(transition, "ToNode", name=childprocess_name)
    graph_node_list = ET.SubElement(transition, "GraphNodeList", name="")
    ET.SubElement(
        graph_node_list,
        "GraphNode",
        icon="",
        isLabelHolder="true",
        label="",
        name="",
        x=coordinates[0],
        y=coordinates[1],
    )

    return transition


def make_end_transition(childprocess_name, coordinates):
    transition = ET.Element("Transition", isExceptionTransition="false")
    ET.SubElement(transition, "FromNode", name=childprocess_name)
    ET.SubElement(transition, "EndNodeReference", name="")
    graph_node_list = ET.SubElement(transition, "GraphNodeList", name="")
    ET.SubElement(
        graph_node_list,
        "GraphNode",
        icon="",
        isLabelHolder="true",
        label="",
        name="",
        x=coordinates[0],
        y=coordinates[1],
    )

    return transition


def make_fieldstore(name, coordinates):
    return ET.Element(
        "ThisNode", displayName="", name=name, x=coordinates[0], y=coordinates[1]
    )


def make_dataflow(fromnode, tonode, coordinates):
    dataflow = ET.Element("DataFlow")
    ET.SubElement(dataflow, "FromNode", name=fromnode)
    ET.SubElement(dataflow, "ToNode", name=tonode)
    graph_node_list = ET.SubElement(dataflow, "GraphNodeList", name="")
    ET.SubElement(
        graph_node_list,
        "GraphNode",
        icon="",
        isLabelHolder="true",
        label="",
        name="",
        x=coordinates[0],
        y=coordinates[1],
    )

    return dataflow


def make_dataflow_entry(dataflow, fromnode, tonode, from_data=None, to_data=None):
    dataflow_entry = ET.SubElement(dataflow, "DataFlowEntry")
    from_field = ET.SubElement(dataflow_entry, "FromField")
    param_assignment = ET.SubElement(
        from_field,
        "ParameterAssignment",
        exceptionStrategy="0",
        language="EcmaScript",
        name="",
        version="",
    )
    verbatim = ET.SubElement(param_assignment, "Verbatim", fieldName="text")
    verbatim.text = CDATA(from_data)
    to_field = ET.SubElement(dataflow_entry, "ToField")
    ET.SubElement(to_field, "FieldDefinitionReference", name=to_data)

    return dataflow


def make_procedure(root, path):
    procedure_name = path.rsplit(".", 1)[1]

    return Procedure(root, path, ET.ElementTree(new_procedure_etree(procedure_name)))


def parse(ced, path):
    etree = ET.parse(str(ced.get_realpath(path)))

    return Process(ced.root, path, etree)


class CEDResource(object):
    def __init__(self, root, path, etree):
        self.root = root
        self._etree = etree
        self.rootnode = self._etree.getroot()
        self.path = path

    def save(self):
        realpath = self.realpath()

        if not realpath.parent.exists():
            realpath.parent.mkdir(parents=True, exist_ok=True)

        realpath.write_text(str(self))

    def realpath(self):
        relative_path = Path(self.path.replace(".", os.sep) + ".xml")
        realpath = self.root / relative_path

        return realpath

    def __str__(self):
        return ET.tostring(
            self._etree,
            pretty_print=True,
            doctype="<!DOCTYPE " + self._get_doctype() + " [] >",
            encoding="UTF-8",
            xml_declaration=True,
        ).decode("utf-8")


class Procedure(CEDResource):
    """docstring for Procedure"""

    def __init__(self, root, path, etree):
        super().__init__(root, path, etree)

    def name(self):
        return self.rootnode.get("name")

    def _get_doctype(self):
        return "Procedure"

    # <ProcedureLocals>
    #  <IntegerField
    #      name="age" />
    # </ProcedureLocals>
    def add_local_vars(self, **kwargs):
        for key, value in kwargs.items():
            local_vars = ET.SubElement(self.rootnode, "ProcedureLocals")
            ET.SubElement(local_vars, "IntegerField", name=key)

    def local_vars(self):
        self.rootnode


class Process(CEDResource):
    """It allows creating and editing a GTProcess object"""

    def __init__(self, root, path, etree):
        super().__init__(root, path, etree)
        self.procedures = []

    @property
    def instance_fields(self):
        return self.process_def.find("InstanceFields")

    @property
    def process_def(self):
        return self.rootnode.find("ProcessDefinition")

    def add_import(self, import_elem):
        self.rootnode.append(import_elem)

    def get_imports(self):
        return self.rootnode.findall("ImportDeclaration")

    def add_fields(self, fields):
        for field in fields:
            self.add_field(field)

    def add_field(self, field_node):
        process_def = self.rootnode.find("ProcessDefinition")
        instance_fields = process_def.find("InstanceFields")

        if not instance_fields:
            instance_fields = ET.SubElement(process_def, "InstanceFields")
        instance_fields.append(field_node)

    def add_parameters(self, parameters):
        self.add_fields(parameters)
        self._mark_as_params_or_results(parameters, "Parameter")

    def _mark_as_params_or_results(self, parameters, tagname):
        for param in parameters:
            self._mark_field(param.get("name"), tagname)

    def add_results(self, results):
        self.add_fields(results)
        self._mark_as_params_or_results(results, "Result")

    def mark_as_parameter(self, field_name):
        self._mark_field(field_name, "Parameter")

    def mark_as_result(self, field_name):
        self._mark_field(field_name, "Result")

    def _mark_field(self, field_name, tagname):
        process_def = self.rootnode.find("ProcessDefinition")
        attrib = {"from": "", "name": field_name, "to": ""}
        ET.SubElement(process_def, tagname, attrib)

    def get_parameters(self):
        return self._get_params_or_results("Parameter")

    def get_results(self):
        return self._get_params_or_results("Result")

    def _get_params_or_results(self, tagname):
        return [
            field
            for field in self.instance_fields.find(".")
            if field.get("name") in self._get_process_def_child_names(tagname)
        ]

    def _get_process_def_child_names(self, tagname):
        return [elem.get("name") for elem in self.process_def.findall(tagname)]

    def get_field(self, name):
        for node in self.rootnode.iter():
            if node.tag == "InstanceFields":
                instance_fields = node

        if instance_fields:
            for field in instance_fields.iter():
                if field.get("name") == name:
                    return field

        return None

    def add_general_procedure(self, procedure_name):
        process_def = self.rootnode.find("ProcessDefinition")
        instance_procedures = process_def.find("InstanceProcedures")

        if not instance_procedures:
            instance_procedures = ET.SubElement(
                process_def, "InstanceProcedures", name=""
            )

        ET.SubElement(
            instance_procedures, "Procedure", name=procedure_name, nested="true"
        )
        self.procedures.append(
            make_procedure(self.root, self.path + "." + procedure_name)
        )

    def get_procedure(self, procedure_name):
        for procedure in self.procedures:
            if procedure.name() == procedure_name:
                return procedure

        return None

    # <ChildProcess
    #    displayName=""
    #    executeAsAsynchronous="false"
    #    name="viewContact"
    #    waitOnParent="false"
    #    x="154"
    #    y="32">
    #  <ProcessDefinitionReference
    #      name="ViewContact"
    #      nested="false" />
    # </ChildProcess>
    def name(self):
        return self.process_def.get("name")

    def instance_name(self):
        name = self.name()

        return name[0].lower() + name[1:]

    def wrapper(self, path):
        wrapper = make_process(self.root, path)
        wrapper.add_imports(deepcopy(self.get_object_imports()))
        wrapper.add_fields(deepcopy(self.get_params_and_results()))

        for field in self.get_parameters():
            wrapper.mark_as_parameter(field.get("name"))

        for field in self.get_results():
            wrapper.mark_as_result(field.get("name"))

        childprocess = make_childprocess(self.name(), ("142", "32"))
        wrapper.process_def.append(childprocess)
        wrapper.process_def.append(
            make_start_transition(childprocess.get("name"), ("70", "32"))
        )
        wrapper.process_def.append(
            make_end_transition(childprocess.get("name"), ("202", "32"))
        )
        wrapper.process_def.append(make_fieldstore("fieldStore0", ("142", "176")))
        dataflow = make_dataflow("fieldStore0", self.instance_name(), ("48", "144"))
        parameters = wrapper.get_parameters()
        tonode = self.instance_name()
        fromnode = "fieldStore0"

        for param in parameters:
            make_dataflow_entry(
                dataflow,
                fromnode,
                tonode,
                from_data=param.get("name"),
                to_data=param.get("name"),
            )
        wrapper.process_def.append(dataflow)

        dataflow = make_dataflow(self.instance_name(), "fieldStore0", ("240", "144"))

        for result in wrapper.get_results():
            make_dataflow_entry(
                dataflow,
                self.instance_name(),
                "fieldStore0",
                from_data=result.get("name"),
                to_data=result.get("name"),
            )
        wrapper.process_def.append(dataflow)

        return wrapper

    def get_params_and_results(self):
        wrapper_fields = list(self.get_parameters())
        wrapper_fields.extend(
            field for field in self.get_results() if field not in wrapper_fields
        )

        return wrapper_fields

    def get_object_imports(self):
        data_flow = self.get_parameters()
        data_flow.extend(self.get_results())
        dataflow_objectfields = [
            field for field in data_flow if field.tag == "ObjectField"
        ]

        imports = [
            self.get_object_import(object_field)
            for object_field in dataflow_objectfields
        ]

        return imports

    def add_imports(self, imports):
        for import_elem in imports:
            self.add_import(import_elem)

    def get_object_import(self, object_field):
        object_ref = object_field.find("TypeDefinitionReference").get("name")

        for import_elem in self.get_imports():
            if object_ref == import_elem.get("name"):
                return import_elem

        return None

    def save(self):
        super().save()

        for procedure in self.procedures:
            procedure.save()

    def _get_doctype(self):
        return "ProcessDefinition"

    def __eq__(self, other):
        if not isinstance(other, Process):
            return False

        return str(self) == str(other)
