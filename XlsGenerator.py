#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
import calendar
import datetime
import openpyxl

#
# Params
#
d2si_text_params = {
	"d2si.consultant.name":"",
	"d2si.administrative.name":"",
	"d2si.contract":"",
	"client.name":""
}
d2si_image_params = {
	"d2si.logo":"d2si.png",
	"d2si.consultant.signature":"signature.png"
}
template = "BNP_template.xlsx"

# Harcoded params
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

########################################################################
# Main
########################################################################

# Compute some dates
current_year = datetime.date.today().year
current_month = datetime.date.today().month

# Load workbook
wb = openpyxl.load_workbook(filename = template)

# Grab the CRA worksheet
ws = wb.get_sheet_by_name("CRA")

# Navigate cells
for row in ws.iter_rows(): 
	for cell in row:
		# Cell has a value
		if cell.value is not None:
			cell_value = extract_template_key(str(cell.value).strip())

			# Cell is a d2si param
			if cell_value in d2si_text_params.keys():
				cell.value = d2si_text_params.get(cell_value)

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

			# Cell is an image
			if cell_value in d2si_image_params.keys():
				cell.value = ""
				img = openpyxl.drawing.image.Image(d2si_image_params.get(cell_value))
				img.anchor(cell = cell, anchortype = "oneCell")
				ws.add_image(img)


# Save the file
wb.save("BNP CRA PELLEGRIN Nicolas " + datetime.date.today().strftime("%B %Y") + ".xlsx")
