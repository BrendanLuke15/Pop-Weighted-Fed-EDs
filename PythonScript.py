# By: Brendan Luke
# Date: October 1, 2021
# Purpose: script to create population weighted electoral maps of Canada's federal electoral districts
from datetime import datetime
startTime = datetime.now()

# import modules
import math
import numpy as np
import matplotlib.pyplot as plt
import re
import codecs

# Get CSV file and parse out districts and population
EDpopData = np.genfromtxt("data/ED-Canada_2016.csv", delimiter=",", dtype=None)
ED_ID = EDpopData[2:len(EDpopData[:,1]),0]
ED_NameEn = EDpopData[2:len(EDpopData[:,1]),1]
ED_NameFr = EDpopData[2:len(EDpopData[:,1]),2]
ED_Pop = EDpopData[2:len(EDpopData[:,1]),3]

# Save KML file as .txt file and cut out unwanted junk
KMLData = codecs.open('data/FED_CA_2019_EN.kml','r',encoding='utf-8')
KMLData = KMLData.read()
Regexs = ["<description>(.+?)</description>\\n","<styleUrl>(.+?)</styleUrl>\\n",
    "<Snippet(.+?)</Snippet>\\n","<Style(.+?)</Style>\\n","<\?xml(.+?)?>\\n","<kml(.+?)>\\n",
    "<Document(.+?)>\\n","<MultiGeometry>\\n","<Polygon>\\n",#"<outerBoundaryIs>\\n",
    "<LinearRing>\\n",
    "</LinearRing>\\n",#"</outerBoundaryIs>\\n",
    "</Polygon>\\n","</MultiGeometry>\\n","</Placemark>\\n",
    "<Placemark(.+?)>\\n","\\t",#\\t\\t\\t\\t",
    "</Folder>\\n","</Document>\\n","</kml>\\n","<name>FED_CA_2019_EN</name>\\n",
    "<Folder(.+?)>\\n","<name>FED_CA_2019_EN</name>\\n",",0"] # unwanted text to remove
for x in Regexs:
    KMLData = re.sub(x,"",KMLData,flags=re.DOTALL)

# write stripped data to file (<name> and <coordinates>)
with open("Stripped Data.txt", "w") as KML2TXT:
    KML2TXT.write(KMLData)

# Loop through each district shape and parse out data (name & lat-lon coordinates)
splitData = KMLData.split("<name>")
splitData.pop(0) # remove newline first element
name = []
coords = []
i = 0
for ED in splitData:
    name.append(ED[0:ED.find("</name>")])
    coords.append(ED[ED.find("<coordinates>")+len("<coordinates>"):ED.find("</coordinates>")])
    coords[i] = re.sub("\\n","",coords[i],flags=re.DOTALL)
    coords[i] = coords[i][0:len(coords[i])-1]
    i += 1

# Stop Clock
print('Done! Execution took ' + str(datetime.now() - startTime))