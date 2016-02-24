# D2SI cra generator

Tool to generate a CRA from excel template.

## Installation

To run the tool, you will need the following dependencies :
 * openpyxl - The python library to read/write Excel files
 * pillow - The library for image manipulation
 * libjpeg - Same goal
I recomand to set up a virtualenv in order to run the tool.

### System packages

```
sudo apt-get install python3
sudo apt-get install python-virtualenv
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

### Virtualenv

```
virtualenv -p /usr/bin/python3.4 virtual_env
source virtual_env/bin/activate
```

### Python packages

```
pip install openpyxl
pip install pillow
```
