#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This script generates the CRA from Xls template and data provided in json format
#

import calendar
import datetime
import locale
import json
import openpyxl
import sys

# Debug mode
debug = False

# Load params
with open(sys.argv[1]) as data_file:
	params = json.load(data_file)

# Harcoded params
# FIXME
month_weekday_template_key = "month.weekday"
month_day_template_key = "month.day"
short_day_template_key = "short_date"
long_day_template_key = "long_date"

# French locale dates
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

########################################################################
# Functions
########################################################################
def extract_template_key( key ):
	"Extract template key from value with '{{' '}}'"
	if key.startswith("{{") and key.endswith("}}"):
		return key[2:len(key) - 2]
	else:
		return key

def extract_data(dictionary, key):
	current = dictionary
	for split_value in key.split("."):
		if isinstance(current, dict):
			current = current.get(split_value)
		else:
			return None
		if current is None:
			return None
	if current != dictionary:
		return current
	else:
		return None

########################################################################
# Main
########################################################################

# Compute some dates
current_year = datetime.date.today().year
current_month = datetime.date.today().month

# Load workbook
wb = openpyxl.load_workbook(filename = params.get("template"))

# Grab the CRA worksheet
ws = wb.get_sheet_by_name("CRA")

# Navigate cells
for row in ws.iter_rows(): 
	for cell in row:
		# Cell has a value
		if cell.value is not None:
			cell_value = extract_template_key(str(cell.value).strip())
			data_value = extract_data(params, cell_value)

			# If value is a placeholder, default value = ""
			if not debug and str(cell.value).startswith("{{") and str(cell.value).endswith("}}"):
				cell.value = ""

			# Cell is a param from data file
			if data_value is not None and not isinstance(data_value, dict):
				if str(data_value).lower().endswith(".png"):
					# Data is an image
					cell.value = ""
					img = openpyxl.drawing.image.Image(data_value)
					img.anchor(cell = cell, anchortype = "oneCell")
					ws.add_image(img)
				elif isinstance(data_value, bool):
					if data_value is True:
						# Data is a checkbox (true)
						cell.value = "X"
					else:
						# Data is a checkbox (false)
						cell.value = ""
				else:
					# Data is a value
					cell.value = data_value

			# Cell is current month indication
			if cell_value == short_day_template_key:
				cell.value = datetime.date.today().strftime("%B %Y")

			# Cell is current day indication
			if cell_value == long_day_template_key:
				cell.value = datetime.date.today().strftime("%d/%m/%Y")

			# Cell is a weekday
			if cell_value.startswith(month_weekday_template_key):
				day = int(cell_value[len(month_weekday_template_key) + 1:])
				if day <= calendar.monthrange(current_year, current_month)[1]:
					date = datetime.date(current_year, current_month, day)
					cell.value = date.strftime("%a").upper()
				else:
					cell.value = ""

			# Cell is a day
			if cell_value.startswith(month_day_template_key):
				day = int(cell_value[len(month_day_template_key) + 1:])
				if day <= calendar.monthrange(current_year, current_month)[1]:
					cell.value = day
				else:
					cell.value = ""


# Save the file
wb.save(params.get("output"))
