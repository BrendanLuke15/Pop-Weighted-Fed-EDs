# By: Brendan Luke
# Date: September 30, 2021
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
EDpopData = np.genfromtxt("ED-Canada_2016.csv", delimiter=",", dtype=None)
ED_ID = EDpopData[2:len(EDpopData[:,1]),0]
ED_NameEn = EDpopData[2:len(EDpopData[:,1]),1]
ED_NameFr = EDpopData[2:len(EDpopData[:,1]),2]
ED_Pop = EDpopData[2:len(EDpopData[:,1]),3]

# Save KML file as .txt file and cut out unwanted junk
KMLData = codecs.open('FED_CA_2019_EN.kml','r',encoding='utf-8')
KMLData = KMLData.read()
Regexs = ["<description>(.+?)</description>\\n","<styleUrl>(.+?)</styleUrl>\\n",
    "<Snippet(.+?)</Snippet>\\n","<Style(.+?)</Style>\\n","<\?xml(.+?)?>\\n","<kml(.+?)>\\n",
    "<Document(.+?)>\\n","<MultiGeometry>\\n","<Polygon>\\n","<outerBoundaryIs>\\n","<LinearRing>\\n",
    "</LinearRing>\\n","</outerBoundaryIs>\\n","</Polygon>\\n","</MultiGeometry>\\n","</Placemark>\\n",
    "<Placemark(.+?)>\\n","\\t","</Folder>\\n","</Document>\\n","</kml>\\n","<name>FED_CA_2019_EN</name>\\n",
    "<Folder(.+?)>\\n","<name>FED_CA_2019_EN</name>\\n",",0"] # unwanted text to remove
for x in Regexs:
    KMLData = re.sub(x,"",KMLData,flags=re.DOTALL)

# write stripped data to file (<name> and <coordinates>)
with open("Stripped Data.txt", "w") as KML2TXT:
    KML2TXT.write(KMLData)

# Get KML file and parse out lat-lon coordinates of district outlines
#test = KMLData.split("<Placemark")

#for x in test:
    #name = re.search('<name>(.+?)</name>',x)
    #name = re.search('<description>(.+?)</description>',x,flags=re.DOTALL)
    #print(name.group(1))
    #print(name.groups)
#print(len(test))

# Stop Clock
print('Done! Execution took ' + str(datetime.now() - startTime))