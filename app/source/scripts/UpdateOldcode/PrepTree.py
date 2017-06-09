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
class Prep_Tree():
    @myLog.catch_wrapper
    def __init__(self,PARAMS):
        ## PROPERTIES
        self.PREP_OUTLINE = PREP.Prep_Outline(PARAMS)

        ## METHODS
        self.prepTree(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def prepTree(self, PARAMS):
        print("...prep_tree")

        self.PREP_OUTLINE.setLRUInterconnections(PARAMS)
        self.PREP_OUTLINE.copyConnectionsFromSource(PARAMS)
        self.getPaths(PARAMS)

        print("...paths:")
        for path in PARAMS.pathList:
            print("paths:", path)

		## GET OTHER PATHS IF ANY
        unique_LRUs = self.PREP_OUTLINE.getOtherPaths(PARAMS)

        if PARAMS.settings.attrib["minimum_path_only"] == "true":
            self.PREP_OUTLINE.getMinimumPaths(PARAMS, unique_LRUs)


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
        for LRU in PARAMS.LRUInterconnectionList:
            if PARAMS.lruToBeTraced == LRU.source_lru:
                self.PREP_OUTLINE.getPaths(PARAMS, temp_path_list, LRU, LRU)