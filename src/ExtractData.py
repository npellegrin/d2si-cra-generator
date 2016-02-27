#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This script converts data from Syges html page to json
#
# It uses beautifulsoup, because WEBDEV produces non-standard malformed html
#

import bs4
import json
import sys

# Open file
sygesFile = open(sys.argv[1], encoding = "iso-8859-1")

# Parse data
sygesSoup = bs4.BeautifulSoup(sygesFile.read(), 'html.parser')

# Retrieve data block
divData = sygesSoup.find(id="ZRP_PAGPRI_1")

# Retrieve data row
rowData = divData.table.tbody.contents[3]

# Get data
data = rowData.find_all("input")

# Convert in json
extracted = {}
for tag in data:
	if "title" in tag.attrs and "value" in tag.attrs:
		extracted[tag["title"]] = tag["value"]

# Save data
json.dump(extracted, open(sys.argv[2], 'w'))
