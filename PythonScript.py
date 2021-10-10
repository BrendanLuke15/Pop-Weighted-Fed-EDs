# By: Brendan Luke
# Date: October 10, 2021
# Purpose: script to create population weighted electoral maps of Canada's federal electoral districts
from datetime import datetime
startTime = datetime.now()

# import modules
import math
import numpy as np
import matplotlib.pyplot as plt
import re
import codecs
import os

# relative filepaths sometimtes don't work
dirname = os.path.dirname(__file__)

# Get CSV file and parse out districts and population
EDpopData = np.genfromtxt(dirname + "/data/ED-Canada_2016.csv", delimiter=",", dtype=None)
ED_ID = EDpopData[2:len(EDpopData[:,1]),0]
ED_NameEn = EDpopData[2:len(EDpopData[:,1]),1]
ED_NameFr = EDpopData[2:len(EDpopData[:,1]),2]
ED_Pop = EDpopData[2:len(EDpopData[:,1]),3]

# Save KML file as .txt file and cut out unwanted junk
KMLData = codecs.open(dirname + '/data/FED_CA_2019_EN.kml','r',encoding='utf-8')
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
        x = []
        y = []
        z = []
        # write lat and lon to lists, cartesian coordinates
        for coord in tempCoords:
            if j%2 == 0: # even index (longitude)
                lon.append(float(coord))
                j += 1
            else: # odd index (latitude)
                lat.append(float(coord))
                j += 1
                x.append(math.cos(math.radians(lat[int(j/2-1)]))*math.cos(math.radians(lon[int(j/2-1)])))
                y.append(math.cos(math.radians(lat[int(j/2-1)]))*math.sin(math.radians(lon[int(j/2-1)])))
                z.append(math.sin(math.radians(lat[int(j/2-1)])))
        # get center coordinates
        cenLon.append(sum(lon)/len(lon))
        cenLat.append(sum(lat)/len(lat))
        # create plot and save image
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        #ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))  # aspect ratio is 1:1:1 in data space
        ax.plot3D(x,y,z)
        ax.set_xlim3d(-1,1)
        ax.set_ylim3d(-1,1)
        ax.set_zlim3d(0.65,1)
        ax.view_init(elev=62.4, azim=-96.466667) # set viww to middle of canada


        #plt.plot(lon,lat,'k-',linewidth=2)
        #plt.axis('equal')
        plt.axis('off')
        plt.savefig(dirname + "/images/"+name[len(name)-1]+".png",transparent=True,bbox_inches='tight',pad_inches=0)
        plt.close()
        i += 1
        print(i)

    # get outer boundary coords

    # see if inner boundary coords

    # handle multi-shaped districts



# Stop Clock & Show Plots
print('Done! Execution took ' + str(datetime.now() - startTime))
#plt.show()