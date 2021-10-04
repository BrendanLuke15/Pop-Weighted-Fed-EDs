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
    "<Folder(.+?)>\\n","<name>FED_CA_2019_EN</name>\\n","0 "] # unwanted text to remove
for x in Regexs:
    KMLData = re.sub(x,"",KMLData,flags=re.DOTALL)

# write stripped data to file (<name> and <coordinates>)
with open("Stripped Data.txt", "w") as KML2TXT:
    KML2TXT.write(KMLData)

# Loop through each district and create plot of boundaries for each and save as image
splitData = KMLData.split("<name>")
splitData.pop(0) # remove newline first element
name = [""]
cenLat = []
cenLon = []
i = 0
for ED in splitData:
    tempName = ED[0:ED.find("</name>")]
    if tempName in name: # multi-shape district
        print("Uh-oh!")
        "do nothing" # defintely do something
    else: # stand alone district shape OR first instance of district shape
        name.append(tempName)
        tempCoords = ED[ED.find("<coordinates>\n")+len("<coordinates>\n"):ED.find("</coordinates>")]
        tempCoords = tempCoords.split(",")
        tempCoords.pop(len(tempCoords)-1) # remove newline last element
        j = 0
        lat = []
        lon = []
        # write lat and lon to lists
        for coord in tempCoords:
            if j%2 == 0: # even index (longitude)
                lon.append(float(coord))
                j += 1
            else: # odd index (latitude)
                lat.append(float(coord))
                j += 1
        # get center coordinates
        cenLon.append(sum(lon)/len(lon))
        cenLat.append(sum(lat)/len(lat))
        # create plot and save image
        plt.plot(lon,lat,'k-',linewidth=2)
        plt.axis('equal')
        plt.axis('off')
        plt.savefig("images/"+name[len(name)-1]+".png",transparent=True,bbox_inches='tight',pad_inches=0)
        plt.close()
        i += 1
        print(i)

    # get outer boundary coords

    # see if inner boundary coords

    # handle multi-shaped districts



# Stop Clock & Show Plots
print('Done! Execution took ' + str(datetime.now() - startTime))
#plt.show()