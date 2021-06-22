#!/usr/bin/env python3

from translation_manager import copy_new_keys_to_locale, write_json
import unittest

class TestTranslationManager(unittest.TestCase):

    def test_copy_new_keys_to_locale(self):
        """A larger test with varying structure"""
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

        
    def test_copy_new_keys_to_locale_string_to_obj(self):
        """Tests changing a string into an object"""
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


    def test_copy_new_keys_to_locale_obj_to_string(self):
        """Tests changing an object to a string"""
        primaryDict = {
            "one": "is a string"
        }

        secondaryDict = {
            "one": {"hoge": "hoge"}
        }

        copy_new_keys_to_locale(primaryDict, secondaryDict)

        expectedDict = {
            "one": "is a string"
        }
        self.assertEqual(write_json(expectedDict), write_json(secondaryDict))

        
    def test_copy_new_keys_to_locale_expand_child(self):
        """Tests adding to child object"""
        primaryDict = {
            "one": {"hoge": "hoge",
                    "naruhodo": "naruhodo"}
        }

        secondaryDict = {
            "one": {"hoge": "ほげ"}
        }

        copy_new_keys_to_locale(primaryDict, secondaryDict)

        expectedDict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "naruhodo"}
        }
        self.assertEqual(write_json(expectedDict), write_json(secondaryDict))


    def test_copy_new_keys_to_locale_no_changes(self):
        """Tests running on no changes"""
        primaryDict = {
            "one": {"hoge": "hoge",
                    "naruhodo": "naruhodo"}
        }

        secondaryDict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "なるほど"}
        }

        copy_new_keys_to_locale(primaryDict, secondaryDict)

        expectedDict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "なるほど"}
        }
        self.assertEqual(write_json(expectedDict), write_json(secondaryDict))

                         
if __name__ == '__main__':
    unittest.main()
