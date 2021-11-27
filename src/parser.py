import math
import inspect
import json


def interpolate(x1, y1, x2, y2, value):
	y = y1 + (y2-y1)/(x2-x1)*(value-x1)
	return y
    
def inside(x1, x2, value):
    if value <= x2 and value >= x1:
        return True
    elif (x1>x2):
        if value >= x2 and value <= x1:
            return True
    return False
    
class AirfoilFile():
    def __init__(self):
        self.c = {}

        self.c["alpha"] = []
        self.c["cl"] = []
        self.c["cd"] = []
        self.c["cm"] = []
        self.c["header"] = []
        #self.c["dataDict"] = {}
        self.c["liftPoints"] = []
        self.c["liftPointsText"] = ""
        
    def readFromFile(self, filename):
        self.c["header"] = []
        f = open(filename, "r")
        ln = f.readline()
        ln2 = f.readline()
        if ("I" in ln and "1110 Version" in ln2):
            # file seems to be right format
            self.c["header"].append(ln)
            self.c["header"].append(ln2)
            
        else:
            return
        
        for i in range(20):
            self.c["header"].append(f.readline())
            
        if "alpha cl cd cm:" in self.c["header"][21]:
            print("allt går bra hittils")
            
        while True:
            line = f.readline()
            if not line:
                break
            while line[0] == " ":
                line = line[1:]
            ar = line.split()
            
            angle = ar[0].replace('-', 'n')
            # self.c["dataDict"][ar[0]] = {}
            # self.c["dataDict"][ar[0]]["cl"] = ar[1]
            # self.c["dataDict"][ar[0]]["cd"] = ar[2]
            # self.c["dataDict"][ar[0]]["cm"] = ar[3]
            
            self.c["alpha"].append(float(ar[0]))
            self.c["cl"].append(float(ar[1]))
            self.c["cd"].append(float(ar[2]))
            self.c["cm"].append(float(ar[3]))
            
        #print(f.readline())
        #print(f.readline())
        #print(self.c["dataDict"])
        
    def saveFile(self, filename):
        f = open(filename, "w")
        for line in self.c["header"]:
            f.write(line)
        for i in range(len(self.c["alpha"])):
            out = "{:6.1f}{:9.5f}{:9.5f}{:9.5f}\n".format(self.c["alpha"][i], self.c["cl"][i], self.c["cd"][i], self.c["cm"][i])
            f.write(out)


    def saveConfigFile(self, filename):
        out = self.c
        for i in inspect.getmembers(self):
            if not inspect.ismethod(i[1]):
                if (i[0].startswith("s_")):
                    out[i[0]] = i[1]
                    
        with open(filename, "w") as outputfile:
            json.dump(out, outputfile, indent=4, sort_keys=True)
        
    def loadConfigFile(self, filename):
        
        with open(filename) as configfile:
            self.c = json.load(configfile)
            print("loaded config")
            print(self.c["u_liftSym"])
        
        
        
        
    def getIndexByAngle(self, infloat):
        for i in range(len(self.c["alpha"])):
            if infloat <= self.c["alpha"][i]:
                return i
                
    def createDrag(self, min, max):
        for i in range(len(self.c["alpha"])):
            self.c["cd"][i] = -math.cos(math.radians(self.c["alpha"][i]*2))/2*max + max/2 + min
            
    def createLiftFromPoints(self, text):
        points = self.createPointsFromText(text)
        self.plotPointsText = text
        self.plotPoints(self.c["cl"], points)
        
    def createPointsFromText(self, text):
        liftPoints = []
        rows = text.split("\n")
        for row in rows:
            pt = row.split()
            if (len(pt) == 2):
                pts = (float(pt[0]), float(pt[1]) )
                liftPoints.append(pts)
        
        # generera par
        pairs = []
        prev = 0
        for pt in liftPoints:
            if prev != 0:
                pair = (prev, pt )
                pairs.append(pair)
            prev = pt
            
        print("liftpoints", pairs)
        return pairs
        
    def interpolate(self):
        return 0
        
    def plotPoints(self, target, points):
        
        for pair in points:
            (x1, y1), (x2, y2) = pair
            print("plot", x1, y1, x2, y2)
            
            for i in range(len( self.c["alpha"]  )):
                alpha = self.c["alpha"][i]
                if (inside(x1, x2, alpha)):
                    target[i] = interpolate(x1, y1, x2, y2, alpha)
        
    def makeSymetric(self, target):
        for i in range(len( self.c["alpha"]  )):
            alpha = self.c["alpha"][i]
            if alpha <0:
                target[i] = float(target[self.getIndexByAngle(abs(alpha) )])*-1
                
                