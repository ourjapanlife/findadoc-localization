#!/usr/bin/env python3

from functools import reduce
import operator
import json
import copy
import glob
import os
import sys

import fire


LOCALE_DIR = "../locales"
INDENT = 4


class InvalidLanguageError(Exception):
    """Exception raised for invalid language inputs.

    Attributes
    ----------
    `language` : input language which caused the error
    """

    def __init__(self, language=""):
        self.language = language
        super().__init__(self.language)

    def __str__(self):
        if self.language:
            return f"Invalid language: {self.language}\nPlease check if it is an ISO 639-1 language flag!"
        else:
            return f"Invalid language!\nPlease check if it is an ISO 639-1 language flag!"


def open_locale_file(fname) -> dict:
    """Opens a locale file.
    
    Raises
    ------
    `InvalidLanguageError`
        If the input language flag is invalid.
    """
    try:
        with open(fname) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise InvalidLanguageError()


def write_json(data):
    """Writes JSON to a string"""
    return json.dumps(data, indent=INDENT, ensure_ascii=False, sort_keys=True)


def export(data, fname):
    """Writes data to the correct locale file"""
    with open(fname, 'w', encoding='utf-8') as json_file:
        json_file.write(write_json(data))


def is_expected(key, dest, exp_type):
    """Returns true if key in dest and is instance of exp_type, e.g. configured as expected"""
    return key in dest and isinstance(dest[key], exp_type)


def copy_new_keys_to_locale(source_dict, dest_dict):
    """Copy all the keys in source_dict missing from the destination JSON"""
    queue = [(source_dict, dest_dict)]
    while len(queue) > 0:
        (dict1, dict2) = queue.pop(0)
        for k, v in dict1.items():
            if isinstance(v, str):
                if not is_expected(k, dict2, str):
                    dict2[k] = copy.deepcopy(v)
            elif isinstance(v, dict):
                if is_expected(k, dict2, dict):
                    # add the subdict to the queue
                    queue.append((v, dict2[k]))
                else:
                    dict2[k] = copy.deepcopy(v)

                    
def delete_key_from_dict(key, dest_dict):
    """Removes a key from a dict. Key must be of the form 'a.b.c' using '.' separators to denote key hierarchy """
    parts = key.split('.')
    cur = dest_dict
    
    while len(parts) > 0:
        k = parts.pop(0)
        if not k in cur:
            return
        if len(parts) == 0:
            del cur[k]
        else:
            cur = cur[k]

def trim_dead_keys(primary_dict, dest_dict):
    """Remove all keys not in primary_dict from dest_dict"""
    queue = [(primary_dict, dest_dict)]
    trim_list = []
    while len(queue) > 0:
        (dict1, dict2) = queue.pop(0)
        for k, v in dict2.items():
            if k in dict1:
                if isinstance(v, dict):
                    queue.append((dict1[k], v))
            else:
                trim_list.append((dict2, k))

    while len(trim_list) > 0:
        (d, k) = trim_list.pop(0)
        del d[k]
                
                    
def get_locale_files(path=LOCALE_DIR):
    """Returns a string array of all locale files"""
    return glob.glob(f'{path}/*.json')


def recurse_dict(d: dict, keys=()):
    """Generator.
    
    Returns
    -------
    Iterable of the nested dictionary as (compound_keys, value):
        - compound_keys: cookie-trail
        - values: nested value after following the compound_keys
    """
    if type(d) == dict:
        for key in d:
            for value in recurse_dict(d[key], keys + (key, )):
                yield value
    else:
        yield (keys, d)

def nested_get(d: dict, *keys):
    """Returns value of nested dict for given compound_keys."""
    return reduce(operator.getitem, keys, d)

def nested_set(d: dict, value, *keys):
    """Sets value in nested dictionary for given keys path."""
    nested_get(d, *keys[:-1])[keys[-1]] = value


class TranslationManager(object):
    """Command line tool for managing i18n files"""
    def alphabetize(self):
        """Rewrites JSON files to be alphabetized"""
        for fname in get_locale_files():
            print(f"Updating {fname}...")
            data = open_locale_file(fname)
            export(data, fname)
        print("Done!🙌🏻")

    def copy_new_keys(self, locale="en"):
        """Moves all missing keys from the primary locale
        (default is English) to the other locale files"""
        primary_fname = f"{LOCALE_DIR}/{locale}.json"
        primary_dict = open_locale_file(primary_fname)

        for fname in get_locale_files():
            if fname != primary_fname:
                print(f"Updating {fname}...")
                dest_dict = open_locale_file(fname)
                copy_new_keys_to_locale(primary_dict, dest_dict)
                export(dest_dict, fname)

        print("Done!🙌🏻")


    def remove_key(self, key):
        """Deletes a key and child values from all locale files"""
        for fname in get_locale_files():
            print(f"Removing {key} from {fname}...")
            dest_dict = open_locale_file(fname)
            delete_key_from_dict(key, dest_dict)
            export(dest_dict, fname)
        print("Done!🙌")

        
    def trim_dead_keys(self, locale="en"):
        """Removes keys not in the primary locale file from 
        all other files"""
        primary_fname = f"{LOCALE_DIR}/{locale}.json"
        primary_dict = open_locale_file(primary_fname)

        for fname in get_locale_files():
            if fname != primary_fname:
                print(f"Trimming {fname}...")
                dest_dict = open_locale_file(fname)
                trim_dead_keys(primary_dict, dest_dict)
                export(dest_dict, fname)

    def translate_interactive(self, dest:str, source:str="en"):
        """Spawns interactive translating session.

        User is asked to submit (missing) key-translations for a given language.
        
        Parameters
        ----------
        `dest` : str
            The destination language flag [ISO 639-1].
        `source` : str, optional
            The source language flag [ISO 639-1]. Defaults to english language.
        """
        # Load locale
        source_fname = f"{LOCALE_DIR}/{source}.json"
        dest_fname   = f"{LOCALE_DIR}/{dest}.json"
        source_dict  = open_locale_file(source_fname)
        dest_dict    = open_locale_file(dest_fname)

        # Make sure target json has the same keys as the source one
        copy_new_keys_to_locale(source_dict, dest_dict)

        # Dict comparison generator
        dict_comparator = list(zip(recurse_dict(source_dict), recurse_dict(dest_dict)))
        n_keys = len(dict_comparator)

        # Start interactive translation session
        print(f"Translating from {source} -> {dest}")
        print("Enter a translation for the given key.")
        print("Leave the prompt empty if the current translation is good enough.")
        cols, _ = os.get_terminal_size()
        print("-"*cols)
        for i, [[_, source_value], [compound_key, dest_value]] in enumerate(dict_comparator):
            # Prompt user to input new translation
            counter = f"## {i} out of {n_keys} ##"
            key_trail = "## Key: " + '->'.join(compound_key) + " ##"
            string_source = f"{source}: {source_value}"
            string_dest   = f"{dest}: {dest_value}"
            prompt = ">>  "
            print(counter)
            print(key_trail)
            print(string_source)
            print(string_dest)
            string_translated = input(prompt)

            # Clear terminal
            cols, _ = os.get_terminal_size()
            for i in range(int(len(counter)/cols)
                            +int(len(key_trail)/cols)
                            +int(len(string_source)/cols)
                            +int(len(string_dest)/cols)
                            +int((len(prompt)+len(string_translated))/cols)
                            +5):
                sys.stdout.write("\033[F")  # back to previous line
                sys.stdout.write("\033[K")  # clear line
            
            # Save user input to dict
            if string_translated:
                nested_set(dest_dict, string_translated, *compound_key)

        # export modified dict and save
        export(dest_dict,dest_fname)
        print("Done! 🎉")

                
if __name__ == '__main__':
    try:
        fire.Fire(TranslationManager)
    except KeyboardInterrupt:
        print("\nAbort.")
