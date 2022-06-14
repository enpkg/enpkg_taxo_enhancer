# taxo_enhancer
Retrieve taxonomy and Wikidata ID from sample's species.  
NB: data have to be formatted according to https://github.com/mandelbrot-project/data_organization.


1. Clone this repository.
2. Create (<code>conda env create -f environment.yml</code>) and activate environment (<code>conda activate taxo_enhancer</code>).
3. Lauch the script: only 1 argument needed here, the path to your data directory.

```console
python .\src\taxo_info_fetcher.py -p path/to/your/data/directory/
```
