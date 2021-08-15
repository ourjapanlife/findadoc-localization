#!/usr/bin/env python3

import json
import copy
import glob

import fire


LOCALE_DIR = "../locales"
INDENT = 4


def open_locale_file(fname):
    """Opens a locale file"""
    with open(fname) as json_file:
        return json.load(json_file)


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
    
                    
def get_locale_files(path=LOCALE_DIR):
    """Returns a string array of all locale files"""
    return glob.glob(f'{path}/*.json')


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
        
if __name__ == '__main__':
    fire.Fire(TranslationManager)
