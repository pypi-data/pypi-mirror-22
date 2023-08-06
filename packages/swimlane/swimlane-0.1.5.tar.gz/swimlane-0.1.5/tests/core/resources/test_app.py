import mock
import unittest

from swimlane.core.resources import App


MOCK_APP = {
    'id': '123',
    'name': 'Mock App',
    'acronym': 'MA',
    'fields': [{
        'id': '456',
        'name': 'Mock Field'
    }]
}

patch_client = mock.patch('swimlane.core.resources.app.Client', autospec=True)


class AppTestCase(unittest.TestCase):
    def test_init(self):
        app = App(MOCK_APP)
        for key, value in MOCK_APP.items():
            self.assertEqual(getattr(app, key), value)

    def test_field_id(self):
        app = App(MOCK_APP)
        self.assertEqual(app.field_id('Mock Field'), '456')
        self.assertEqual(app.field_id('Not A Field'), None)

    @patch_client
    def test_find_all(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        apps = list(App.find_all())
        self.assertEqual(len(apps), 1)
        self.assertIsInstance(apps[0], App)

    @patch_client
    def test_find_by_id(self, mock_client):
        mock_client.get.return_value = MOCK_APP
        app = App.find(app_id='123')
        self.assertIsInstance(app, App)
        self.assertEqual(app.id, '123')

    @patch_client
    def test_find_by_name(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(name='Mock App')
        self.assertIsInstance(app, App)
        self.assertEqual(app.name, 'Mock App')

    @patch_client
    def test_find_by_acronym(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(acronym='MA')
        self.assertIsInstance(app, App)
        self.assertEqual(app.acronym, 'MA')

    @patch_client
    def test_find_by_name_does_not_exist(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(name='Some Other App')
        self.assertIsNone(app)

    @patch_client
    def test_find_by_acronym_does_not_exist(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(acronym='SOA')
        self.assertIsNone(app)

    @patch_client
    def test_find_with_missing_attributes(self, mock_client):
        """Tests that no exception is raised when returned App does not provide an acronym or name attribute"""
        mock_client.get.return_value = [{}]
        self.assertIsNone(App.find(name='Some App'))
        self.assertIsNone(App.find(acronym='SOA'))
