#!/bin/bash

# FIXME: python scripts should comunicate without writing intermediate files

# Get html for current month
# TODO
#python DownloadSyges.py data/credentials.json data/syges.html

# Extract data from html
python ExtractData.py data/syges.html data/syges_data.json

# Convert to data for XLS generation
python ConvertData.py data/syges_data.json data/personal_data.json data/xls_data.json

# Generate XLS
python XlsGenerator.py data/xls_data.json

# Send email
# TODO
