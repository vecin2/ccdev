from emtask.ced.nubia_commands.commands import override_verb
from sql_gen.commands import CreateSQLTaskCommand
from sql_gen.database import Connector

class FakeConnector(object):
    """docstring for FakeConnector"""
    def __init__(self,
                 server=None,
                 user=None,
                 password=None,
                 database=None,
                 port=None,
                 dbtype=None):
        self.server=server
        self.user =user
        self.password = password
        self.database = database
        self.port = port
        self.dbtype =dbtype
    def connect(self):
        return FakeConnection(self.server,
                                    self.user,
                                    self.password,
                                    self.database,
                                    port=self.port)
        
row ={
      "ENTITY_KEYNAME":"Contact",
      "NAME":"inlineView"
     }
class FakeConnection(object):
    def __init__(self,
                 server=None,
                 user=None,
                 password=None,
                 database=None,
                 port=None):
        self.server=server
        self.user =user
        self.password = password
        self.database = database
        self.port = port

    def cursor(self):
        return FakeCursor()

class FakeCursor(object):

    """Docstring for FakeCursor. """

    def __init__(self):
        """TODO: to be defined. """
        self.rows= None
        self.description=[]
    def execute(self,query):
        self.rows= [(row["ENTITY_KEYNAME"],row["NAME"])]
        for key in row.keys():
           self.description.append([key])

    def __iter__(self):
        return self.rows.__iter__()

    def __next__(self):
        return self.rows.__next__()
        


        
def testing_with_mock(mocker):
    """Test it computes entity_keyname and verb_name from current_path and it calls rewire_verb sql template with correct parameters"""
    mockCreateSQLCmd =mocker.patch('emtask.sql.tasks.CreateSQLTaskCommand',autospec=True)
    mockConnection =mocker.patch('emtask.sql.tasks.Connector',autospec=True)
    mockConnection.return_value=FakeConnector()

    override_verb(current_path='Contact.Verbs.InlineView',
                  new_path='PCContact.Verbs.InlineView')

    template_values={"entity_def_id":"Contact",
                     "new_pd_path":"PCContact.Verbs.InlineView",
                     "verb_name":"inlineView"}
    mockCreateSQLCmd.assert_called_once_with(template_name='rewire_verb.sql',template_values=template_values,run_once=True)
    mockConnection.assert_called_once_with('localhost',
                            'FP8_HFR2_DEV_AD',
                            'FP8_HFR2_DEV_AD',
                            'XEPDB1',
                            '1521',
                            'oracle')
