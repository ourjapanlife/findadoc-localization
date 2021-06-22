#!/usr/bin/env python3

import unittest

from translation_manager import *

class TestTranslationManager(unittest.TestCase):

    def test_copy_new_keys_to_locale(self):
        self.assertEqual('foo'.upper(), 'FOO')
        primaryDict = {
            "one": {
                "whatever": {"foo": "bar"},
                "okay": {"hoge": "hoge"}
            },
            "two": "top level",
            "three": {
                "rhubarb": { "eh": "eeeh"},
                "teeth": "yes"
            }
        }

        secondaryDict = {
            "one": {"okay": {"hoge": "ほげ"}},
            "three": {
                "teeth": "はい"
            }
        }

        copy_new_keys_to_locale(primaryDict, secondaryDict)

        expectedDict = {
            "one": {
                "whatever": {"foo": "bar"},
                "okay": {"hoge": "ほげ"}
            },
            "two": "top level",
            "three": {
                "rhubarb": { "eh": "eeeh"},
                "teeth": "はい"
            }
        }
        self.assertEqual(write_json(expectedDict), write_json(secondaryDict))

    # TODO: try a test with a key changing from string to object
    def test_copy_new_keys_to_locale_string_to_obj(self):
        self.assertEqual('foo'.upper(), 'FOO')
        primaryDict = {
            "one": {"hoge": "hoge"}
        }

        secondaryDict = {
            "one": "was a string"
        }

        copy_new_keys_to_locale(primaryDict, secondaryDict)

        expectedDict = {
            "one": {"hoge": "hoge"}
        }
        self.assertEqual(write_json(expectedDict), write_json(secondaryDict))

                         
if __name__ == '__main__':
    unittest.main()
