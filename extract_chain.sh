#!/bin/bash

# FIXME: python scripts should comunicate without writing intermediate files

# Get html for current month
# TODO
#python DownloadSyges.py data/credentials.json data/syges.html

# Extract data from html
python src/ExtractData.py src/data/syges.html src/data/syges_data.json

# Convert to data for XLS generation
python src/ConvertData.py src/data/syges_data.json src/data/personal_data.json src/data/xls_data.json

# Generate XLS
python src/XlsGenerator.py src/data/xls_data.json

# Send email
# TODO
