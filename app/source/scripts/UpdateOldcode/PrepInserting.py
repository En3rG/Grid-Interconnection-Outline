import copy
import math
import logging
import Common as CC
import PrepOutline as PREP
from lxml import etree
import myLog

####################################################################################################################
##
####################################################################################################################
class Prep_Inserting():
    @myLog.catch_wrapper
    def __init__(self,PARAMS,settings):
        ## PROPERTIES
        self.settings = settings
        self.PREP_OUTLINE = PREP.Prep_Outline(PARAMS,settings)

        ## METHODS
        self.prepInserting(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def prepInserting(self, PARAMS):
        print("...prepInserting")

        self.PREP_OUTLINE.setLRUInterconnections(PARAMS)
        self.PREP_OUTLINE.copyConnectionsFromSource(PARAMS)


        if self.settings["GridView"]["duplicateLRU"] == "True":
            self.PREP_OUTLINE.updateLRUConnectionsOver4(PARAMS)

        self.getPaths(PARAMS)

        print("...paths:")
        for path in PARAMS.pathList:
            print("paths:", path)

		## GET OTHER PATHS IF ANY
        unique_LRUs = self.PREP_OUTLINE.getOtherPaths(PARAMS)

        if self.settings["GridView"]["minimum_path_only"] == "True":
            self.PREP_OUTLINE.getMinimumPaths(PARAMS, unique_LRUs)

        self.countlruInstances(PARAMS)

        if self.settings["GridView"]["delete_path_list_loops_no_duplicate"] == "False":
            self.getPathLoops(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def countlruInstances(self, PARAMS):
        print("...count lru instances")

        for path in PARAMS.pathList:
            for lru in path:
                try:
                    PARAMS.lruInstances[lru] = PARAMS.lruInstances[lru] + 1
                except:
                    PARAMS.lruInstances[lru] = 1

        print(PARAMS.lruInstances)
		
    ####################################################################################################################
    ##
    ####################################################################################################################
    def setEndpointLoc(self, PARAMS):
        self.PREP_OUTLINE.setEndpointLoc(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getPaths(self, PARAMS):
        if PARAMS.lruToBeTraced == "ALL":
			## JUST PICK FIRST LRU
            for LRU in PARAMS.LRUInterconnectionList:
                temp_path_list = []
                temp_path_list.append(LRU.source_lru)
                PARAMS.lruToBeTraced = LRU.source_lru
                break
        else:
            temp_path_list = []
            temp_path_list.append(PARAMS.lruToBeTraced)

		## TRACE THE PATH BASE ON THE LRU TO BE TRACED
        #LRU = PARAMS.getLRUInterconnection(PARAMS.lruToBeTraced)
        for LRU in PARAMS.LRUInterconnectionList:
            if PARAMS.lruToBeTraced == LRU.source_lru:
                self.PREP_OUTLINE.getPaths(PARAMS, temp_path_list, LRU, LRU)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getPathLoops(self, PARAMS):
        print("...getting path loops")

        self.PREP_OUTLINE.getPathLoops(PARAMS)
        self.PREP_OUTLINE.getPathLoopsNoDuplicate(PARAMS)

        self.PREP_OUTLINE.getPathLoopsNoDuplicateDictList(PARAMS)

        self.PREP_OUTLINE.verifyPathListDicts(PARAMS)


