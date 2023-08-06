#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

##################################
# Standard library imports
##################################
import re
import zipfile
from io import BytesIO

##################################
# Third party imports
##################################
import pandas as pd
import requests

##################################
# Local imports
##################################

def downloadAndExtract(gdeltUrl):
    """Downloads and extracts GDELT zips without saving to disk"""

    response = requests.get(gdeltUrl, stream=True)
    zipdata = BytesIO()
    zipdata.write(response.content)
    gdelt_zipfile = zipfile.ZipFile(zipdata, 'r')
    name = re.search('(([\d]{4,}).*)',
                     gdelt_zipfile.namelist()[0]).group().replace('.zip', "")
    data = gdelt_zipfile.read(name)
    gdelt_zipfile.close()
    del zipdata, gdelt_zipfile, name, response
    return pd.read_csv(BytesIO(data), delimiter='\t', header=None)
