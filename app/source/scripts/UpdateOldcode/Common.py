import numpy
import csv
from lxml import etree
import logging
import myLog

####################################################################################################################
##
####################################################################################################################
class Params():
    @myLog.catch_wrapper
    def __init__(self, settings=None):
        ## PROPERTIES
        ## VERSION INFO
        self.major = 0
        self.minor = 4
        self.build = 0
        
		## ROOT DIRECTORY OF FILES
        self.rootFiles = "../files/data/"

        ## FROM SETTINGS
        self.settingsCSS = None
        self.settings = settings

		## USING NUMPY TO GENERATE ARRAYS
        # self.csvMatrix = numpy.zeros((5,5))
        # self.csvMatrix = numpy.array(['a', 'b', 'c'], dtype=object)

        self.maxrow = 10
        self.maxcol = 10

        self.positionMatrix = numpy.ndarray((self.maxrow, self.maxcol), dtype=object)

        #self.csvMatrix = numpy.ndarray((self.maxrow, self.maxcol), dtype=object)

		## ROW NUM IS FIRST, THEN COL
        self.csv_row = 0
        self.csv_col = 0
        self.position_row = 0
        self.position_col = 0
        # self.csvMatrix[1][2] = "test"
		
		## DICTIONARY OF COLUMNS, BASE ON KEY OF THE LRU
        ## ONLY ADDS THE LRU IF ITS NOT IN found_LRU YET
        self.csv_col_dict = {}
        #self.csv = open('./OUTPUT/Connections.csv', 'w', newline='\n', encoding='utf-8')
        #self.csvfile = csv.writer(self.csv)

		## FOR GATHERING PIN INFORMATION
        self.pinInterconnectionList = []
        self.connectionList = []
        self.LRUInterconnectionList = []

		## FOR GENERATING PATHS
        self.LRUSTARTINGCONNECTION = Lru_Interconnection()
        self.pathList = []
        self.pathSkippedList = []
        self.pathLoopsList = []
        self.pathLoopsNoDuplicateList = []
        self.pathLoopsNoDuplicateDictList = []
        self.pathLoopsRemovedList = []
        self.startingLruPickedList = []
        self.Loop1EndDictList = []

        ## FOR DRAWING OUTLINE
        #self.directionDict = {"up": "up", "right": "right", "down": "down", "left": "left","upleft": "upleft","upright": "upright","downleft": "downleft","downright": "downright"}
        self.directionDict = {"up": "up", "right": "right", "down": "down", "left": "left"}
        self.directionDict2 = {"upleft": "upleft","upright": "upright", "downleft": "downleft", "downright": "downright"}
        self.statusDict = {"set": "set", "temp": "temp"}
        self.signalTypeDict = {"input": "input", "output": "output", "control": "control", "same":"same"}
        self.lruTypeDict = {"LRU":"LRU", "CABLE":"CABLE", "input":"input", "output":"output", "control":"control", "":"unknown","COMPONENT":"COMPONENT", "CONTROL":"CONTROL"}

        ## PARAMS.LoopsDict:  {'DSP': [{'Loops_C': [], 'Paths': ['DSP', '1W3', 'ECM', '1W2', 'VCDM', '1W1', 'DSP'], 'Loops_D': [], ...
        self.LoopsDict = {}
        ## renameDict {'DSP': {'DSP2': '1W5', 'DSP1': '1W1', 'DSP0': '1W3', 'DSP3': '1W7'}, 'ECM': {'ECM3': '1W6', 'ECM1': '1W2', 'ECM0': '1W3', 'ECM2': '1W4'}}
        self.renameDict = {}
        ## PARAMS.multipleloopsCornerLRUDict {'DSP': ['DSP', 'ECM']}
        self.multipleloopsCornerLRUDict = {}

        self.lrusExpandedList = []

        self.multipleLoopsKey = []

        self.delimeterDuplicatingLRU = "____"

        self.lruToBeTraced = None

        self.totalDelay = 0

        self.lruInstances = {}

    ####################################################################################################################
    ##
    ####################################################################################################################
    def updateSizeOfPositionMatrix(self, size):
        print("...Updating size of positionMatrix to", size)
        self.maxrow = size
        self.maxcol = size
        self.positionMatrix = numpy.ndarray((size, size), dtype=object)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def updateSizeOfCsvMatrix(self, size):
        print("...Updating size of csvMatrix to", size)
        self.maxrow = size
        self.maxcol = size
        self.csvMatrix = numpy.ndarray((size, size), dtype=object)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getLRUInterconnection(self,lru):
        for LRU in self.LRUInterconnectionList:
            if lru == LRU.source_lru:
                return LRU

####################################################################################################################
## EACH CONNECTION/PINS ON EACH LRU/CABLE
####################################################################################################################
class Pin():
    @myLog.catch_wrapper
    def __init__(self):
        self.lru = None
        self.lru_label = None
        self.conn = None
        self.pin = None
        self.connectedpin = None
        self.lruType = None

        self.description = ""
        self.components = "'"
        self.type = ""
        self.control = ""

    def setConnectedPin(self,xmlData):
        ## FIND PIN FROM THE XML DATA

        newPin = None
        for elem in xmlData:
            if self.lru == elem.attrib["name"]:
                for connectors in elem:
                    if self.conn == connectors.tag:
                        for pins in connectors:
                            if self.pin == pins.tag:
                                ## FOUND PIN
                                try:
                                    newPin = pins.attrib["connectedPin"]
                                except:
                                    newPin = self.pin
                                break

        if newPin == None:
            print("Error: Pin Not Found",self.lru,self.conn,self.pin)
            logging.error("Error: Pin Not Found %s %s %s",self.lru,self.conn,self.pin)

        self.connectedpin = newPin

        return self.connectedpin

    def getString(self):
        if self.lru != None:
            stringval = self.lru + "_" + self.conn + "_"+ self.pin
            return stringval
        else:
            stringval = ""
            return stringval

    def getStringLeft(self):
        if self.lru != None:
            stringval = self.pin + "_" + self.conn + "_" + self.lru
            return stringval
        else:
            stringval = ""
            return stringval

    def printdata(self):
        print("             -----printdata (Connection)----")
        print("             lru: ", self.lru)
        print("             lru_label:", self.lru_label)
        print("             conn:", self.conn)
        print("             pin:", self.pin)
        print("             lruType: ", self.lruType)
        print("             description: ", self.description)
        print("             components: ", self.components)
        print("             type: ", self.type)
        print("             control: ", self.control)
		
		
####################################################################################################################
## A PAIR OF CONNECTIONS (SOURCE & DESTINATION)
####################################################################################################################
class Pin_Interconnection():
    @myLog.catch_wrapper
    def __init__(self):
        self.SOURCE = Pin()
        self.DEST = Pin()
        self.internal_list = []

        self.source_loc = None
        self.dest_loc = None

    def setSource(self, src):
        self.SOURCE = src

    def setDest(self, dst):
        self.DEST = dst

    def setInternalList(self, internal_dest_conn_list):
        self.internal_list = internal_dest_conn_list

    def printdata(self,isConnection=False, isInternal=False):
        print("     -----printdata (Pin_Interconnection)----")
        if isConnection == True:
            print("     SOURCE::::: ")
            self.SOURCE.printdata()
        else:
            print("     SOURCE::::: ")
            print("     ", self.SOURCE.lru)
        if isConnection == True:
            print("     DEST::::: ")
            self.DEST.printdata()
        else:
            print("     DEST::::: ")
            print("     ", self.DEST.lru)
        if isInternal == True:
            print("     internal_list:::::::: ")
            for item in  self.internal_list:
                print("     lru:", item.lru, " conn:", item.conn,  " pin: ", item.pin)
        else:
            print("     internal_list:::::::: ")
            print("     internal_list:", self.internal_list)
        print("     source_loc: ", self.source_loc)
        print("     dest_loc: ", self.dest_loc)

####################################################################################################################
## OBJECT IN AN OBJECT ARE TIED TOGETHER, CHANGING THE PARENT WILL CHANGE THE CHILD
####################################################################################################################
class Lru_Interconnection():
    @myLog.catch_wrapper
    def __init__(self):
        self.source_lru = ""
		## LIST OF pin_interconnection CLASS
        self.pin_interconnections_list = []
		## LIST OF UNIQUE LRU DEST (STRINGS)
        self.dest_lru_list = []
        self.POSITION = Position()
		## UP, DOWN, LEFT, RIGHT
        self.direction = None
		## SET, TEMP
        self.status = None

        self.isTop_empty = True
        self.isRight_empty = True
        self.isBottom_empty = True
        self.isLeft_empty = True

        self.isEmptyDict = {"up": True, "down": True, "right": True, "left": True}
        self.isEmptyDict2 = {"upleft": True, "upright": True, "downright": True, "downleft": True}

    def setSourceLru(self, src):
        self.source_lru = src

    def addPinInterconnectionsList(self, pin_interconnection):
        self.pin_interconnections_list.append(pin_interconnection)

    def addDestLruList(self, dest):
        self.dest_lru_list.append(dest)

    def setRow(self, row):
        self.POSITION.row = row

    def setCol(self, col):
        self.POSITION.col = col

    def getOppositeDirection(self, direction):
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        else:
            doing = None

    def getToTheRightDirection(self, direction):
        if direction == 'up':
            return 'right'
        elif direction == 'down':
            return 'left'
        elif direction == 'left':
            return 'up'
        elif direction == 'right':
            return 'down'
        else:
            doing = None

    def printdata(self,isPin=False,isConnection=False, isInternal=False):
        print("-----printdata (Lru_Interconnection)----")
        print("source_lru: ", self.source_lru)
        if isPin == True:
            print("pin_interconnections_list:::::::::")
            for item in self.pin_interconnections_list:
                item.printdata(isConnection,isInternal)
        else:
            print("pin_interconnections_list:::::::::")
            for item in self.pin_interconnections_list:
                print(item)
        print("dest_lru_list:", self.dest_lru_list)
        print("POSITION:", " row: ", self.POSITION.row, " col: ", self.POSITION.col)
        print("direction:", self.direction)
        print("status:", self.status)
        print("isTop_empty:", self.isTop_empty)
        print("right_empty:", self.isRight_empty)
        print("bottom_empty:", self.isBottom_empty)
        print("left_empty: ", self.isLeft_empty)

####################################################################################################################
## POSITION IN MATRIX (ROW AND COLUMN)
####################################################################################################################
class Position():
    @myLog.catch_wrapper
    def __init__(self):
        self.row = None
        self.col = None

####################################################################################################################
##
####################################################################################################################
class Pathbranch():
    @myLog.catch_wrapper
    def __init__(self):
        self.prefix = None
        self.paths_list = []
        self.branch_tree = Pathtree()

####################################################################################################################
##
####################################################################################################################
class Pathtree():
    @myLog.catch_wrapper
    def __init__(self):
        ## LIST OF PATHBRANCH
        self.branches_list = []




