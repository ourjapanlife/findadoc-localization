#!/usr/bin/env python3

import fire
import json, copy, glob

#from typing import Dict


INDENT=4


def openLocaleFile(fname):
    """Opens a locale file"""
    with open(fname) as json_file: 
      return json.load(json_file) 

  
def write_json(data):
    return json.dumps(data, indent=INDENT, ensure_ascii=False, sort_keys=True) 


def export(data, fname):
    """Writes data to the correct locale file"""
    with open(fname, 'w', encoding='utf-8') as json_file: 
        json_file.write(write_json(data)) 

        
def is_expected(key, dest, expValue):
    return key in dest and isinstance(dest[key], expValue)

        
def copy_new_keys_to_locale(sourceDict, destDict):
    """Copy all the keys in sourceDict missing from the destination JSON"""
    queue = [(sourceDict, destDict)]
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

    
def get_locale_files(path='../locales'):

    return glob.glob(f'{path}/*.json')


class TranslationManager(object):

  def alphabetize(self):
      """Rewrites JSON files to be alphabetized"""
      for fname in get_locale_files():
          print(f"Updating {fname}...")
          data = openLocaleFile(fname)
          export(data, fname)
      print("Done!🙌🏻")
          
  
  def copy_new_keys(self, locale="en"):
    """Moves all missing keys from the primary locale (default is English) to the other locale files"""
    primaryFName = f"../locales/{locale}.json"
    primaryDict = openLocaleFile(primaryFName)

    for fname in get_locale_files():
        if fname != primaryFName:
            print(f"Updating {fname}...")
            destDict = openLocaleFile(destLocale)
            copy_new_keys_to_locale(primaryDict, destDict)
            export(destDict, destLocale)
            
    print("Done!🙌🏻")

    
if __name__ == '__main__':
  fire.Fire(TranslationManager)
