#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This script converts syges extract to xls data, adding personnal data in input file
#

import copy
import datetime
import json
import locale
import sys

# Load params
with open(sys.argv[1]) as data_file:
	sygesData = json.load(data_file)
with open(sys.argv[2]) as data_file:
	personalData = json.load(data_file)

# French locale dates
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

# Build basic result
merged = copy.deepcopy(personalData)
merged["year"] = datetime.datetime.now().strftime("%Y")
merged["month"] = datetime.datetime.now().strftime("%m")
merged["day"] = datetime.datetime.now().strftime("%d")
merged["worked_days"] = {}

# Convert data
worked_days_am = 0
worked_days_pm = 0
for day in sygesData:
	date = datetime.datetime.strptime(day, "%A %d/%m/%y")
	amount = float(sygesData[day])
	if amount == 1.0:
		merged["worked_days"]["{d.day}".format(d=date)] = {"AM":True, "PM":True}
		worked_days_am = worked_days_am + amount
		worked_days_pm = worked_days_pm + amount
	elif amount == 0.0:
		merged["worked_days"]["{d.day}".format(d=date)] = {"AM":False, "PM":False}
	elif amount == 0.5:
		print("WARNING: unable to identify AM or PM, AM is set")
		merged["worked_days"]["{d.day}".format(d=date)] = {"AM":True, "PM":False}
		worked_days_am = worked_days_am + amount
	else:
		print("ERROR: unable to parse " + sygesData[day])

# Add sums
merged["worked_days"]["sum"] = {"AM":worked_days_am, "PM":worked_days_pm}

# Save result
json.dump(merged, open(sys.argv[3], 'w'))
