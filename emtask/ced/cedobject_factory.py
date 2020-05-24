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


def make_process(root, path):
    return Process(root, path, ET.ElementTree(new_process_etree()))


class Process(object):
    """It allows creating and editing a GTProcess object"""

    def __init__(self, root, path, etree):
        self.root = root
        self._etree = etree
        self.root_node = self._etree.getroot()
        self.path = path

    def add_field(self, field_type, name):
        process_def = self.root_node.find("ProcessDefinition")
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

    def get_field(self, name):
        for node in self.root_node.iter():
            if node.tag == "InstanceFields":
                instance_fields = node

        if instance_fields:
            for field in instance_fields.iter():
                if field.get("name") == name:
                    return field

        return None

    def get_imports(self):
        return []

    def realpath(self):
        relative_path = Path(self.path.replace(".", os.sep) + ".xml")
        realpath = self.root / relative_path

        return realpath

    def save(self):
        realpath = self.realpath()

        if not realpath.parent.exists():
            realpath.parent.mkdir(parents=True, exist_ok=True)

        realpath.write_text(str(self))

    def __eq__(self, other):
        if not isinstance(other, Process):
            return False

        return str(self) == str(other)

    def __str__(self):
        return ET.tostring(
            self._etree,
            pretty_print=True,
            doctype="<!DOCTYPE ProcessDefinition [] >",
            encoding="UTF-8",
            xml_declaration=True,
        ).decode("utf-8")


def parse(ced, path):
    etree = ET.parse(str(ced.get_realpath(path)))

    return Process(ced.root, path, etree)
