#!bin/bash/python3
# import warnings as warn
import os
import csv
import json
import glob
import time
import warnings as warn
# import sys
# gis
import utm
# math
import numpy as np
import numpy.linalg as la
# plot
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d


class Path(object):
    """docstring for Path"""
    def __init__(self, cords, typ="UTM", keyPoints = None):
        self.keyPoints = keyPoints
        self.GPScords = [] # cords in GPS
        self.UTMcords = [] # cords in UTM
        if typ== "UTM":
            self.setUTM(cords)
        elif typ=="GPS":
            self.setGPS(cords)
        else:
            raise RuntimeError("invalid type of coordinates")

    def setUTM(self, cords):
        self.UTMcords = cords

    def setGPS(self, cords):
        self.UTMcord = cords

    def UTM2GPS(self, zone):
        # converts all the UTM cords to GPS
        self.GPScords = [utm.to_latlon(*cord, *zone) for cord in self.UTMcords]

    def GPS2UTM(self):
        # converts all the GPS cords to UTM
        self.UTMcords = [utm.from_latlon(*cord) for cord in self.GPScords]

    def setKeypoints(self, keyPoints):
        self.keyPoints = keyPoints

    def __len__(self):
        # number of waypoints in path
        return len(self.UTMcords)

    def __repr__(self):
        #print the cords
        return print(self.UTMcords)
        

    def parseFile(self):
        pathFiles = glob.glob(os.path.join(self.pathDir, "routes/*"))
        for file in pathFiles:
            self.cords = dict()
            # print(file)
            with open(file) as csvfile:
                for line in csv.reader(csvfile, delimiter=','):
                    if line[2] != '50':
                        continue
                    cords = (line[0], line[1])
                    if cords in self.keyPoints:
                        continue
                    try:
                        self.cords[cords] += 1
                    except KeyError as e:
                        self.cords[cords] = 1
                try:
                    routeEff = self.calcEff()
                    print(file, ": ", routeEff)
                    self.writeEff(file, routeEff)
                except ZeroDivisionError as e:
                    print("invalid file: {:s}".format(file))

    def calcEff(self):
        nPts = 0
        nPaths = 0
        for keys in self.cords:
            nPaths += self.cords[keys]
            nPts += 1
        return nPts/nPaths

    def writeEff(self, routeFile, routeEff):
        infoFile = os.path.join(self.pathDir, "info.txt")
        if os.path.exists(infoFile):
            writeMode = 'a'
        else:
            writeMode = 'w'
        with open(infoFile, writeMode) as f:
            routeName = routeFile.split('/')[-1]
            f.write("\n{:s}: {:2.4f}".format(
                    routeName,
                    routeEff))

    def plot(self, ax, color='b'):
        # path
        cords = np.array(self.UTMcords)
        ax.plot(cords[:-1, 0], cords[:-1, 1])

    def write(self, filename, alt=50, spd=5):
        # writes the trajectory as a txt file
        # Lat,Long,Alt,Speed,Picture,ElevationMap,WP,CameraTilt,UavYaw,DistanceFrom
        with open(filename, "w+") as f:
            # take off
            # add hut-lz as takeoff point
            # f.write("%s,%s,%s,%s,FALSE,,1\n" % (lat, lng, alt, spd))
            # routes
            for lat, lng in self.GPScords:
                f.write(f"{lat} , {lng}, {alt}, {spd},FALSE,,1\n")
            # end route
            # get higher above last point
            lat, lng = self.GPScords[-1]
            f.write(f"{lat} , {lng}, 70, {spd},FALSE,,1\n")





def main(pathDir):
    # get path files
    pathFiles = glob.glob(os.path.join(pathDir, "*/*/"))

    # read json
    # jsonFile = mission + ".json"
    for pathDir in pathFiles:
        Path(pathDir)


if __name__ == '__main__':
    pathDir = "../out"
    main(pathDir)