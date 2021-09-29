# By: Brendan Luke
# Date: September 29, 2021
# Purpose: script to create population weighted electoral maps of Canada's federal electoral districts
from datetime import datetime
startTime = datetime.now()

# import modules
import math
import numpy as np
import matplotlib.pyplot as plt
#import xml as xml
import xml.etree.ElementTree as ET

# Get CSV file and parse out districts and population
EDpopData = np.genfromtxt("ED-Canada_2016.csv", delimiter=",", dtype=None)
ED_ID = EDpopData[2:len(EDpopData[:,1]),0]
ED_NameEn = EDpopData[2:len(EDpopData[:,1]),1]
ED_NameFr = EDpopData[2:len(EDpopData[:,1]),2]
ED_Pop = EDpopData[2:len(EDpopData[:,1]),3]

# Get KML file and parse out lat-lon coordinates of district outlines
KMLData = ET.parse('FED_CA_2019_EN.xml')



# Stop Clock
print('Done! Execution took ' + str(datetime.now() - startTime))