import copy
import numpy
import logging
import Common as CC
import DrawOutline as DRAW
import myLog

####################################################################################################################
##
####################################################################################################################
class Draw_Tree():
    @myLog.catch_wrapper
    def __init__(self,PARAMS):
        ## PROPERTIES
        self.DRAW_OUTLINE = DRAW.Draw_Outline(PARAMS)
        self.nextRow = int(PARAMS.settings.attrib["next_row"])
        self.nextCol = int(PARAMS.settings.attrib["next_col"])

        ## METHODS
        maxrow = self.getLongestPath(PARAMS)
        PARAMS.positionMatrix = numpy.ndarray((maxrow, 1), dtype=object)

        self.drawTree(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getLongestPath(self, PARAMS):
        print("...getting longest path")

        max = 0

        for path in PARAMS.pathList:
            if len(path) > max:
                max = len(path)

        max = max * self.nextRow
        return max

    ####################################################################################################################
    ##
    ####################################################################################################################
    def drawTree(self, PARAMS):
        print("...draw_tree")

        ## PLACE LRUs IN THE MATRIX
        self.placeLRUinMatrix(PARAMS)

		## DELETE EMPTY ONES
        PARAMS.positionMatrix = DRAW.deleteUnusedRownCol(PARAMS.positionMatrix)

		## ASSIGN LRU POSITIONS
        self.updateALLLRUPositions(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def placeLRUinMatrix(self, PARAMS):
        print("...placing LRU in the positionMatrix")

        drawn_lru_list = []

        atColumn = 0
        for path in PARAMS.pathList:
            loops_at = ""

            if len(path) == len(set(path)):
                ## NO LOOPS
                doing = None
            else:
                ## HAS LOOP
                lru_count_dict = {}
                for lru in path:
                    try:
                        print(lru_count_dict[lru])
                        lru_count_dict[lru] = lru_count_dict[lru] + 1
						## 2ND TIME THIS LRU CAME UP, MUST BE THE LOOP
                        loops_at = lru
                    except:
						## KEY DOESNT EXIST YET
                        lru_count_dict[lru] = 1

                print("lru_count_dict", lru_count_dict)

            row = 0
            for lru in path:
                skip = False
                LRU = PARAMS.getLRUInterconnection(lru)
                if lru in drawn_lru_list:
                    doing = None
                    skip = True
                else:
                    PARAMS.positionMatrix[row][atColumn] = LRU

                drawn_lru_list.append(lru)

                row = row + self.nextRow

                if lru != "" and lru == loops_at and skip == False:
					## INSERT A COLUMN
                    maxrow, maxcol = PARAMS.positionMatrix.shape
                    for x in range(0,self.nextCol):
                        PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, maxcol, values=None, axis=1)
                    atColumn = atColumn + self.nextCol

			## INSERT A COLUMN
            maxrow,maxcol = PARAMS.positionMatrix.shape
            for x in range(0, self.nextCol):
                PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, maxcol, values=None, axis=1)
            atColumn = atColumn + self.nextCol


    ####################################################################################################################
    ##
    ####################################################################################################################
    def updateALLLRUPositions(self, PARAMS):
        print("...assigning LRU its positions base on the matrix")

        rows, cols = PARAMS.positionMatrix.shape

        for row in range(0, rows):
            for col in range(0, cols):
                LRU = PARAMS.positionMatrix[row][col]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    LRU.POSITION.row = row
                    LRU.POSITION.col = col