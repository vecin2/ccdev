import os
from pathlib import Path

import lxml.etree as ET


def add_process_def_node(parent):
    attribs = {
        "appearsInHistory": "true",
        "cyclic": "false",
        "designNotes": "Undefined",
        "exceptionStrategy": "1",
        "icon": "",
        "isPrivate": "false",
        "logicalDatabaseConnection": "",
        "name": "EmptyProcess",
        "nested": "false",
        "pointOfNoReturn": "false",
        "transactionBehaviour": "TX_NOT_SUPPORTED",
        "version": "10",
        "waitOnChildren": "false",
    }

    return ET.SubElement(parent, "ProcessDefinition", attribs)


def new_process_etree():
    root = ET.Element("PackageEntry")
    process_def = add_process_def_node(root)
    ET.SubElement(process_def, "StartNode", displayName="", name="", x="16", y="32")
    ET.SubElement(process_def, "EndNode", displayName="", name="", x="240", y="32")
    transition = ET.SubElement(process_def, "Transition", isExceptionTransition="false")
    ET.SubElement(transition, "StartNodeReference", name="")
    ET.SubElement(transition, "EndNodeReference", name="")
    graph_node_list = ET.SubElement(transition, "GraphNodeList", name="")
    ET.SubElement(
        graph_node_list,
        "GraphNode",
        icon="",
        isLabelHolder="true",
        label="",
        name="",
        x="128",
        y="32",
    )
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
    return Process(root, path, ET.ElementTree(new_process_etree()))


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

    def add_field(self, field_type, name):
        process_def = self.rootnode.find("ProcessDefinition")
        instance_fields = process_def.find("InstanceFields")

        if not instance_fields:
            instance_fields = ET.SubElement(process_def, "InstanceFields")
        string_field = ET.SubElement(
            instance_fields,
            field_type + "Field",
            designNodes="",
            isAttribute="false",
            length="0",
            name=name,
        )
        locale = ET.SubElement(string_field, "StringField_loc", locale="")

        ET.SubElement(locale, "Format")

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
        process_def = self.rootnode.find("ProcessDefinition")

        return process_def.findall(tagname)

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

    def wrapper(self, path):
        process = make_process(self.root, path)

        for param in self.get_parameters():
            process.add_field("String", param.get("name"))
            process.mark_as_parameter(param.get("name"))

        return process

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
