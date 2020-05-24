import os
from pathlib import Path

import pytest

from emtask import project
from emtask.ced import cedobject_factory
from emtask.ced.nubia_commands.commands import rewire_verb
from emtask.ced.tool import CED
from emtask.project import EMProject
from emtasktest.testutils import sample_project


class FakeConnector(object):
    """docstring for FakeConnector"""

    def __init__(
        self,
        server=None,
        user=None,
        password=None,
        database=None,
        port=None,
        dbtype=None,
        mock_connection=None,
    ):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.dbtype = dbtype
        self._valid_connection = {}
        self.mock_connection = mock_connection
        self._connection = None
        self._rows_to_return = None

    def with_connection_details(self, **kwargs):
        self._valid_connection = dict(**kwargs)

        return self

    def fetch_returns(self, rows):
        self._rows_to_return = rows

    def connect(self):
        if self._assert_valid_connection():
            self._connection = FakeConnection(
                self.server, self.user, self.password, self.database, port=self.port
            )
        self._connection.set_cursor(FakeCursor(self._rows_to_return))

        return self._connection

    def _assert_valid_connection(self):
        self.mock_connection.assert_called_once_with(
            self._valid_connection["database_host"],
            self._valid_connection["database_user"],
            self._valid_connection["database_pass"],
            self._valid_connection["database_name"],
            self._valid_connection["database_port"],
            self._valid_connection["database_type"],
        )

        return True

        return self.server == self._valid_connection["server"]


class FakeConnection(object):
    def __init__(self, server=None, user=None, password=None, database=None, port=None):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self._cursor = None

    def cursor(self):
        return self._cursor

    def set_cursor(self, cursor):
        self._cursor = cursor


class FakeCursor(object):

    """Docstring for FakeCursor. """

    def __init__(self, rows):
        """TODO: to be defined. """
        self.column_names_to_return = rows[0]
        self.rows_to_return = rows[1:]
        self.description = []
        self.rows = None

    def execute(self, query):
        self.row = self.rows_to_return[0]
        self.rows = self.rows_to_return

        for column_name in self.column_names_to_return:
            self.description.append([column_name])

    def __iter__(self):
        return self.rows.__iter__()

    def __next__(self):
        return self.rows.__next__()


@pytest.fixture
def fake_connector(mocker):
    """Returns an instance of FakeConnector when invoked within the module specified.
    FakeConnector uses the mock to assert that connection details match
    with those expected
    """
    mock = mocker.patch("emtask.database.Connector", autospec=True)
    fake_connector = FakeConnector(mock_connection=mock)
    mock.return_value = fake_connector
    yield fake_connector


@pytest.fixture
def createsql_cmd(mocker):
    createsql_cmd = mocker.patch("emtask.sql.tasks.CreateSQLTaskCommand")
    createsql_cmd.return_value = createsql_cmd
    yield createsql_cmd


# if testfilesystem.exists():
#    shutil.rmtree(testfilesystem)


def testing_with_mock(fake_connector, createsql_cmd, autospec=True):
    """Test it computes entity_keyname and verb_name from current_path
       and it calls rewire_verb sql template with correct parameters"""
    rows = [
        ("ENTITY_KEYNAME", "NAME", "REPOSITORY_PATH"),
        ("Contact", "inlineView", "Contact.verbs.InlineView"),
    ]
    fake_connector.fetch_returns(rows)
    sample_project(db_connector=fake_connector)

    rewire_verb(
        current_path="Contact.Verbs.InlineView", new_path="PCContact.Verbs.InlineView"
    )

    template_values = {
        "entity_def_id": "Contact",
        "new_pd_path": "PCContact.Verbs.InlineView",
        "verb_name": "inlineView",
    }
    createsql_cmd.assert_called_once_with(
        template_name="rewire_verb.sql", template_values=template_values, run_once=True
    )
    createsql_cmd.run.assert_called_once()


# gtProcess.add_field('String','form')
#    gtProcess.add_import('PRJCustomer.API.EIPRJCustomer','EIPRJCustomer')\
#             .add_parameter("EIPRJCustomer","customer")
#             .add_field("EIPRJCustomer","customer")
#             .add_result("EIPRJContact","entity")
#             .add_procedure("setup")
#


@pytest.fixture
def ced():
    ced = CED(sample_project().get_repo())
    yield ced


def test_when_creating_new_process_save_and_reopen_they_match(ced):
    process_path = "PRJContact.Implementation.Contact.InlineContact"
    process = ced.new_process(process_path)
    process.save()

    assert ced.get_realpath(process_path).exists()
    assert_file_matches_process(ced, process_path, process)

    # <InstanceFields>
    #  <StringField
    #      designNotes=""
    #      isAttribute="false"
    #      length="0"
    #      name="name">
    #    <StringField_loc
    #        locale="">
    #      <Format />
    #    </StringField_loc>
    #  </StringField>
    # </InstanceFields>


def test_add_all_basic_types_fields(ced):
    process = ced.new_process("Test.TestProcess")
    process.add_field("String", "name1")
    process.add_field("Number", "referenceNo")
    process.add_field("Integer", "streetNumber")
    process.add_field("Float", "partialAmount")
    process.add_field("Decimal", "totalAmount")  # defaults to precision 42 and scale 1
    process.add_field("Character", "oneLetter")
    process.add_field("Date", "dob")
    assert process.get_field("name1") is not None
    assert process.get_field("referenceNo") is not None
    assert process.get_field("streetNumber") is not None
    assert process.get_field("partialAmount") is not None
    assert process.get_field("totalAmount") is not None
    assert process.get_field("oneLetter") is not None
    assert process.get_field("dob") is not None
    # todo type Form


@pytest.mark.skip
def test_add_procedure(ced):
    process = ced.new_process("Test.TestProcess")
    process.save()
    process2 = ced.new_process("Test.TestProcess2")
    process2.save()


def assert_file_matches_process(ced, process_path, process):
    loaded_process = ced.open(process_path)
    assert process.get_imports() == loaded_process.get_imports()
    assert str(loaded_process) == str(process)
