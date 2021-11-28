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
        self.c["dataHeader"] = []
        #self.c["dataDict"] = {}
        self.c["liftPoints"] = []
        self.c["liftPointsText"] = ""
        
        self.c["h_mach"] = 0.0
        
        
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
        
        self.readFile(filename)
        
    def readFile(self, filename):
        self.rawfile = []
        f = open(filename, "r")
        while True:
            line = f.readline()
            if not line:
                break
            self.rawfile.append(line)
            
        #extract header
        self.c["h_mach"] = self.rawfile[4]
        
        self.rawDataHeader = self.rawfile[20].split()
        if len(self.rawDataHeader) == 25:
            print("Data header ok")
            self.c["dh_aMin"] = self.rawDataHeader[3]
            self.c["dh_aMax"] = self.rawDataHeader[4]
            self.c["dataHeader"] = self.rawDataHeader
        else:
            print("Data header ERROR",len(self.rawDataHeader) )
        
    def createHeader(self):
        out = ""
# I
# 1110 Version
# 1234 device type code
# 0.040000
# 0.970000
# -0.25000  0.00000  #5
# -0.22000  0.20000  
# -0.15000  0.40000
#  0.00000  0.50000
#  0.20000  0.50000
#  0.75000  0.00000
#  0.75000  0.00000
#  0.75000  0.00000
#  0.75000  0.00000
#  0.20000 -0.50000
#  0.00000 -0.50000
# -0.15000 -0.40000
# -0.22000 -0.20000
# -0.25000 -0.00000  #18
# 2
        if ("h_mach" in self.c):
            mach = f"{self.c['h_mach']:.6f}\n"
        else:
            mach = "0.970\n"
        out += self.c["header"][0]
        out += self.c["header"][1]
        out += self.c["header"][2]
        out += self.c["header"][3] #profile thickness
        out += mach # self.c["h_mach"] # mach number
        out += self.c["header"][5] #5-18 unknown data
        out += self.c["header"][6]
        out += self.c["header"][7]
        out += self.c["header"][8]
        out += self.c["header"][9]
        out += self.c["header"][10]
        out += self.c["header"][11]
        out += self.c["header"][12]
        out += self.c["header"][13]
        out += self.c["header"][14]
        out += self.c["header"][15]
        out += self.c["header"][16]
        out += self.c["header"][17]
        out += self.c["header"][18]
        out += "1\n" # number of tabs with datapoints, only 1 supported at the moment
        return out
    def createDataHeader(self):
# 9.10000 0.10200 0.00000 -18.00000 18.00000 17.00000 1.10000 3.00000 0.00000 0.00000 0.01000 0.00800 0.00000 0.02900 2.60000 0.30000 0.00000 0.00200 2.00000 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000
# 0       1       2       3         4        5        6       7       8       9       10      11      12      13      14      15      16      17      18      19      29      21      22      23      24
# alpha cl cd cm:

# 0 Re number
# 1 slope 

# 3 alpha min
# 4 alpha max
# 5 linear range
        self.c["dataHeader"][3] = f"{self.c['dh_aMin']:.6f}" 
        self.c["dataHeader"][4] = f"{self.c['dh_aMax']:.6f}" # self.c["dh_aMax"]
        out = ""
        for d in self.c["dataHeader"]:
            out += d +" "
        out = out[:-1]
        out+= "\n"
        out+= "alpha cl cd cm:\n"
        
        print("dataheader", out)
        return out
        
        
    def saveFile(self, filename):
        print("exporting file ", filename)
        f = open(filename, "w")
        f.write(self.createHeader())
        # for line in self.c["header"]:
        #     f.write(line)
        f.write(self.createDataHeader())
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
            
        if ("dataHeader" not in self.c):
            
            self.c["dataHeader"] = "9.10000 0.10200 0.00000 -18.00000 18.00000 17.00000 1.10000 3.00000 0.00000 0.00000 0.01000 0.00800 0.00000 0.02900 2.60000 0.30000 0.00000 0.00200 2.00000 0.00000 0.00000 0.00000 0.00000 0.00000 0.00000".split()
            
        
        
        
    def getIndexByAngle(self, infloat):
        for i in range(len(self.c["alpha"])):
            if infloat <= self.c["alpha"][i]:
                return i
                
    def createDrag(self, min, max):
        for i in range(len(self.c["alpha"])):
            self.c["cd"][i] = -math.cos(math.radians(self.c["alpha"][i]*2))/2*max + max/2 + min
            
    def createLiftFromPoints(self, text):
        points = self.createPointsFromText(text)
        #self.plotPointsText = text
        self.plotPoints(self.c["cl"], points)

    def createDataFromPoints(self,target, text, multi=1.0):
        points = self.createPointsFromText(text)
        #self.plotPointsText = text
        self.plotPoints(target, points, multi=multi)
        
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
        
    def plotPoints(self, target, points, multi=1.0):
        
        for pair in points:
            (x1, y1), (x2, y2) = pair
            print("plot", x1, y1, x2, y2)
            
            for i in range(len( self.c["alpha"]  )):
                alpha = self.c["alpha"][i]
                if (inside(x1, x2, alpha)):
                    target[i] = interpolate(x1, y1, x2, y2, alpha)*multi
        
    def makeSymetric(self, target):
        for i in range(len( self.c["alpha"]  )):
            alpha = self.c["alpha"][i]
            if alpha <0:
                target[i] = float(target[self.getIndexByAngle(abs(alpha) )])*-1
    def makeSymetricAbs(self, target):
        for i in range(len( self.c["alpha"]  )):
            alpha = self.c["alpha"][i]
            if alpha <0:
                target[i] = float(target[self.getIndexByAngle(abs(alpha) )])
                
                