# Anticipe
Anticipe download, process and perform all the step to compute the green growth index.

# Getting started

```
git clone https://github.com/simonzabrocki/Anticipe.git
```

# How to 

Because each indicator has specific requirements, each indicator is defined by a folder in data/indicator.

The architecture is as follow for a given indicator (eg. AB1)

data/indicator/AB1/ contains:
- raw: The raw data used in the indicator (can be multiple files from different sources)
- preprocessed: The preprocessed data (formatted)
- processed: The processed data (filtered, imputed)
- computed: The computed data (for the case of composite indicators)


Additionnaly, the folder contains:

- download_config.json: a file containing the API parameters to download the indicator
- process.py: If the indicator is composite, this file is used to define the computation
- preprocess.py: If the file is added manually, this script contains a function to parse the data in raw/

Once the files above are specificed, it is possible the run the pipeline in Pipeline.ipynb. This pipeline will:

- Download
- Preprocess/process indicators
- Compute the index
- Produce reports on the index (missing values, imputation etc ...)


To check that th e pipeline does not contains obvious mistake (duplicates, empty tables etc), run pytest tests/

# Roadmap

- Update config.json with metadata about the indicator (Full name, remarks, details about computation and sources)
- Remove redundant process.py
- Put the pipeline into a CLI tools rather than a jupyter notebook 
- Improve the tests


# Contact

simon.zabrocki@gggi.org