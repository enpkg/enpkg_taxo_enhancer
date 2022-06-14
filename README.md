# taxo_enhancer
Retrieve taxonomy and Wikidata ID from sample's species

1. Clone this repository
2. Create (<code>conda env create -f environment.yml</code>) and activate environment (<code>conda activate taxo_enhancer</code>)
3. Adapt parameters in <code>/params/sirius_canopus_params.yml</code>, especially the path to the files you want to process (in the example below, it would be the path to "/data").<br>
4. Lauch the script: only 1 argument needed here, the path to your data directory.

```console
python .\src\taxo_info_fetcher.py -p path/to/your/data/directory/
```
