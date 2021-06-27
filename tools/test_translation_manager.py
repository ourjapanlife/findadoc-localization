#!/usr/bin/env python3

import unittest

from translation_manager import copy_new_keys_to_locale, write_json

class TestTranslationManager(unittest.TestCase):
    """Unit tests for translation manager"""
    def test_copy_new_keys_to_locale(self):
        """A larger test with varying structure"""
        primary_dict = {
            "one": {
                "whatever": {"foo": "bar"},
                "okay": {"hoge": "hoge"}
            },
            "two": "top level",
            "three": {
                "rhubarb": {"eh": "eeeh"},
                "teeth": "yes"
            }
        }

        secondary_dict = {
            "one": {"okay": {"hoge": "ほげ"}},
            "three": {
                "teeth": "はい"
            }
        }

        copy_new_keys_to_locale(primary_dict, secondary_dict)

        expected_dict = {
            "one": {
                "whatever": {"foo": "bar"},
                "okay": {"hoge": "ほげ"}
            },
            "two": "top level",
            "three": {
                "rhubarb": {"eh": "eeeh"},
                "teeth": "はい"
            }
        }
        self.assertEqual(write_json(expected_dict), write_json(secondary_dict))

    def test_copy_new_keys_to_locale_string_to_obj(self):
        """Tests changing a string into an object"""
        primary_dict = {
            "one": {"hoge": "hoge"}
        }

        secondary_dict = {
            "one": "was a string"
        }

        copy_new_keys_to_locale(primary_dict, secondary_dict)

        expected_dict = {
            "one": {"hoge": "hoge"}
        }
        self.assertEqual(write_json(expected_dict), write_json(secondary_dict))

    def test_copy_new_keys_to_locale_obj_to_string(self):
        """Tests changing an object to a string"""
        primary_dict = {
            "one": "is a string"
        }

        secondary_dict = {
            "one": {"hoge": "hoge"}
        }

        copy_new_keys_to_locale(primary_dict, secondary_dict)

        expected_dict = {
            "one": "is a string"
        }
        self.assertEqual(write_json(expected_dict), write_json(secondary_dict))

    def test_copy_new_keys_to_locale_expand_child(self):
        """Tests adding to child object"""
        primary_dict = {
            "one": {"hoge": "hoge",
                    "naruhodo": "naruhodo"}
        }

        secondary_dict = {
            "one": {"hoge": "ほげ"}
        }

        copy_new_keys_to_locale(primary_dict, secondary_dict)

        expected_dict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "naruhodo"}
        }
        self.assertEqual(write_json(expected_dict), write_json(secondary_dict))

    def test_copy_new_keys_to_locale_no_changes(self):
        """Tests running on no changes"""
        primary_dict = {
            "one": {"hoge": "hoge",
                    "naruhodo": "naruhodo"}
        }

        secondary_dict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "なるほど"}
        }

        copy_new_keys_to_locale(primary_dict, secondary_dict)

        expected_dict = {
            "one": {"hoge": "ほげ",
                    "naruhodo": "なるほど"}
        }
        self.assertEqual(write_json(expected_dict), write_json(secondary_dict))

if __name__ == '__main__':
    unittest.main()
