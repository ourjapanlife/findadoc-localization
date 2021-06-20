#!/usr/bin/env python3

import fire
import json, copy, glob

#from typing import Dict


INDENT=4


def openLocaleFile(fname):
    """Opens a locale file"""
    with open(fname) as json_file: 
      return json.load(json_file) 


def export(data, fname):
    """Writes data to the correct locale file"""
    with open(fname, 'w', encoding='utf-8') as json_file: 
        json_file.write(json.dumps(data, indent=INDENT, ensure_ascii=False, sort_keys=True)) 

        
def copyNewKeysToLocale(sourceDict, destLocale):
    """Copy all the keys in sourceDict missing from the destination JSON"""
    destDict = openLocaleFile(destLocale)

    queue = [(sourceDict, destDict)]
    while len(queue) > 0:
        (dict1, dict2) = queue.pop(0) 
        for k, v in dict1.items():
            if isinstance(v, str):
                if k not in dict2:
                    dict2[k] = copy.deepcopy(v)
            if isinstance(v, dict):
                if k in dict2:
                    # add the subdict to the queue
                    queue.append((v, dict2[k])) 
                else:
                    dict2[k] = copy.deepcopy(v)
                    
    export(destDict, destLocale)

    
def getLocaleFiles(path='locales'):

    return glob.glob(f'{path}/*.json')


class TranslationManager(object):

  def alphabetize(self):
      """Rewrites JSON files to be alphabetized"""
      for fname in getLocaleFiles():
          print(f"Updating {fname}...")
          data = openLocaleFile(fname)
          export(data, fname)
      print("Done!🙌🏻")
          
  
  def copyNewKeys(self, locale="en"):
    """Moves all missing keys from the primary locale (default is English) to the other locale files"""
    primaryFName = f"locales/{locale}.json"
    primaryDict = openLocaleFile(primaryFName)

    for fname in getLocaleFiles():
        if fname != primaryFName:
            print(f"Updating {fname}...")
            copyNewKeysToLocale(primaryDict, fname)

    print("Done!🙌🏻")

    
if __name__ == '__main__':
  fire.Fire(TranslationManager)
