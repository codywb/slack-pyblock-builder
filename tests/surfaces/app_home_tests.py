import unittest
from pyblock_builder.surfaces import AppHome
from pyblock_builder.blocks import Section, Divider

class TestAppHomeSurface(unittest.TestCase):
    """Tests for the AppHome surface class"""

    def test_default_attributes(self):
        test_app_home = AppHome()

        expected_type = "home"
        expected_callback_id = ""
        expected_private_metadata = ""
        expected_external_id = ""
        expected_blocks = []
        expected_view = {
            "type": "home",
            "callback_id": "",
            "blocks": []
        }

        actual_type = test_app_home._type
        actual_callback_id = test_app_home._callback_id
        actual_private_metadata = test_app_home._private_metadata
        actual_external_id = test_app_home._external_id
        actual_blocks = test_app_home.blocks
        actual_view = test_app_home.view

        self.assertEqual(expected_type, actual_type)
        self.assertEqual(expected_callback_id, actual_callback_id)
        self.assertEqual(expected_private_metadata, actual_private_metadata)
        self.assertEqual(expected_external_id, actual_external_id)
        self.assertEqual(expected_blocks, actual_blocks)
        self.assertEqual(expected_view, actual_view)

    def test_set_callback_id(self):
        test_app_home = AppHome()
        test_app_home.set_callback_id("test callback id")

        expected = "test callback id"
        actual = test_app_home._callback_id

        self.assertEqual(expected, actual)

    def test_set_private_metadata(self):
        test_app_home = AppHome()
        test_app_home.set_private_metadata("test metadata")

        expected = "test metadata"
        actual = test_app_home._private_metadata

        self.assertEqual(expected, actual)

    def test_set_external_id(self):
        test_app_home = AppHome()
        test_app_home.set_external_id("test id")

        expected = "test id"
        actual = test_app_home._external_id

        self.assertEqual(expected, actual)

    def test_add_blocks(self):
        test_app_home = AppHome()
        test_app_home.add_blocks(
            Section()
            .set_text("This is a test section."),
            Divider()
        )

        expected = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'This is a test section.'
                }
            },
            {
                'type': 'divider'
            }
        ]
        actual = test_app_home.blocks

        self.assertEqual(expected, actual)

    def test_view(self):
        expected_callback_id = "test callback id"
        expected_private_metadata = "test metadata"
        expected_external_id = "test id"
        expected_blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'This is a test section.'
                }
            },
            {
                'type': 'divider'
            }
        ]
        test_app_home = (AppHome()
                         .set_callback_id(expected_callback_id)
                         .set_private_metadata(expected_private_metadata)
                         .set_external_id(expected_external_id)
                         .add_blocks(
                            Section()
                             .set_text("This is a test section."),
                             Divider()
                         )
                        )

        expected = {
            "type": "home",
            "callback_id": expected_callback_id,
            "private_metadata": expected_private_metadata,
            "external_id": expected_external_id,
            "blocks": expected_blocks
        }