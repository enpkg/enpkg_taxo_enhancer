import pandas as pd 
import numpy as np
from pandas import json_normalize
import requests
import os
from taxo_resolver import *
from pathlib import Path
import argparse
import textwrap

p = Path(__file__).parents[2]
os.chdir(p)

""" Argument parser """
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
         This script creates a <sample>_taxo_metadata.tsv file with the WD ID of the samples species and its OTT taxonomy
         --------------------------------
            You should just enter the path to the directory where samples folders are located
        '''))
parser.add_argument('-p', '--sample_dir_path', required=True,
                    help='The path to the directory where samples folders to process are located')
parser.add_argument('-f', '--force_research', default=False, action="store_true",
                    help='Reanalyze samples for which a result folder is already present')
args = parser.parse_args()
sample_dir_path = args.sample_dir_path
force_res = args.force_research

""" Functions """
url = 'https://query.wikidata.org/sparql'

def wd_taxo_fetcher_from_ott(url, ott_id):
  
    query = '''
  PREFIX wdt: <http://www.wikidata.org/prop/direct/>
  SELECT ?ott ?wd ?img
  WHERE{{
      ?wd wdt:P9157 ?ott
      OPTIONAL{{ ?wd wdt:P18 ?img }}
      VALUES ?ott {{'{}'}}
  }}
  '''.format(ott_id)
  
    r = requests.get(url, params={'format': 'json', 'query': query})

    data = r.json()
    results = pd.DataFrame.from_dict(data).results.bindings
    df = json_normalize(results)
    if len(df) == 0:
      df = pd.DataFrame(data = {'ott.type' : [np.NaN], 'ott.value': [np.NaN], 'wd.type': [np.NaN], 'wd.value': [np.NaN]})
    return df 

 
""" Process """ 

path = os.path.normpath(sample_dir_path)
samples_dir = [directory for directory in os.listdir(path)]
df_list = []

no_match = []
for directory in samples_dir:
    metadata_path = os.path.join(path, directory, directory + '_metadata.tsv')
    try:
        metadata = pd.read_csv(metadata_path, sep='\t')
    except FileNotFoundError:
        continue
    except NotADirectoryError:
      continue
      
    if pd.isna(metadata['organism_species'][0]) == False :
      path_to_results_folders = os.path.join(path, directory, 'taxo_output/')
      if (os.path.isdir(path_to_results_folders)) & (force_res is False):
        print(f'sample {directory} alredy processed')
        continue
      if not os.path.isdir(path_to_results_folders):
        os.makedirs(path_to_results_folders)
      print(f'processing sample {directory}')
      taxo_df = taxa_lineage_appender(metadata, 'organism_species', True, path_to_results_folders, directory)
      if taxo_df['matched_name'][0] == 'None':
        print(f'No matched species for sample {directory}')
        no_match.append(directory)
        continue
      wd_df = wd_taxo_fetcher_from_ott(url,taxo_df['ott_id'][0])
      path_taxo_df = os.path.join(path_to_results_folders, directory + '_taxo_metadata.tsv')
      taxo_df.join(wd_df).to_csv(path_taxo_df, sep='\t')
    else:
      continue

print(f'Done, no match for samples: {no_match}')    