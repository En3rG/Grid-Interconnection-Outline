import copy
import numpy
import logging
import Common as CC
import DrawOutline as DRAW
import random
import myLog


####################################################################################################################
##
####################################################################################################################
class Draw_Inserting():
    @myLog.catch_wrapper
    def __init__(self,PARAMS,settings):

        ## PROPERTIES
        self.DRAW_OUTLINE = DRAW.Draw_Outline(PARAMS)

        self.drawnLru_list = []
        self.loopAt_list = []
        self.lruStarting = None
        self.LRUstarting = None
        self.settings = settings

        ## METHODS
        maxrow = 1
        maxcol = 1
        ## INITIALIZE ARRAY
        PARAMS.positionMatrix = numpy.ndarray((maxrow, maxcol), dtype=object)

        self.drawInserting(PARAMS)
        self.deleteBlocks(PARAMS)

        if self.settings["GridView"]["duplicateLRUasNeeded"] == "True":
            self.duplicateLRUasNeeded(PARAMS)

        self.forPrintingMatrix(PARAMS)
        #self.forPrintingData(PARAMS)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def drawInserting(self, PARAMS):
        print("...drawInserting")

        ## PLACE LRUs IN THE MATRIX
        self.positionEachLRU(PARAMS)

        ## DELETE EMPTY ONES
        PARAMS.positionMatrix = DRAW.deleteUnusedRownCol(PARAMS.positionMatrix)


    ####################################################################################################################
    ##
    ####################################################################################################################
    def positionEachLRU(self, PARAMS):
        print("...placing LRU in the positionMatrix")

        for keys in PARAMS.LoopsDict.keys():
            self.loopAt_list.append(keys)

		## GET STARTING LRU
        path = PARAMS.pathList[0]
        self.lruStarting = path[0]
        lru = path[0]
        self.LRUstarting = PARAMS.getLRUInterconnection(lru)

        if self.settings["GridView"]["reorder_paths"] == "False":
            for path in PARAMS.pathList:
				## EACH START OF PATH, PREVIOUS PATH IS SET TO NONE
                previousLRU = None

                for lru in path:
                    LRU = PARAMS.getLRUInterconnection(lru)
                    print("...at lru:", lru)

                    if lru in self.drawnLru_list:
                        print("...already drawn")
                    elif lru in self.loopAt_list:
                        self.drawingLoops(PARAMS, previousLRU, LRU)

                    else:
                        inserting = False

                        if lru == self.lruStarting:
                            print("...starting LRU, placing LRU at row[0]col[0]")
                            self.drawFirstLRU(PARAMS, LRU)

                        elif previousLRU == None:
                            print("...other path found?")
                            self.drawLRUfromOtherPath(PARAMS, LRU)

                        else:
                            direction = self.drawLRUnGetDirection(PARAMS, previousLRU, LRU)

                        self.drawnLru_list.append(lru)

                    previousLRU = LRU

        else:
            pathSkipped_list = []

            for path in PARAMS.pathList:
                previousLRU = None
                pathSkipped = []
                skipping = False

                for lru in path:
                    if skipping == True:
                        pathSkipped.append(lru)
                    else:
                        LRU = PARAMS.getLRUInterconnection(lru)
                        print("at lru:", lru)

                        if lru in self.drawnLru_list:
                            print("...already drawn")
                            doing = None
                        elif lru in self.loopAt_list:
                            self.drawingLoops(PARAMS,previousLRU,LRU)
                        elif PARAMS.lruInstances[lru] == 1:
                            pathSkipped.append(previousLRU)
                            pathSkipped.append(lru)
                            skipping = True
                        else:
                            inserting = False

                            if lru == self.lruStarting:
                                print("...starting LRU, placing LRU at row[0]col[0]")
                                self.drawFirstLRU(PARAMS, LRU)

                            elif previousLRU == None:
                                print("...other path found?")
                                self.drawLRUfromOtherPath(PARAMS, LRU)

                            else:
                                direction = self.drawLRUnGetDirection(PARAMS, previousLRU, LRU)

                            self.drawnLru_list.append(lru)

                        previousLRU = LRU

                if pathSkipped != []:
                    pathSkipped_list.append(pathSkipped)

            pathSkipped_list = self.reorganizePathsByLength(pathSkipped_list)

			## GO THROUGH PATHS THAT WERE SKIPPED
            for path in pathSkipped_list:
                previousLRU = path[0]
                path.pop(0)

                for lru in path:
                    LRU = PARAMS.getLRUInterconnection(lru)
                    print("at lru:", lru)

                    if lru in self.drawnLru_list:
                        print("...already drawn")
                        doing = None
                    elif lru in self.loopAt_list:
                        self.drawingLoops(PARAMS, previousLRU, LRU)

                    else:
                        inserting = False

                        if lru == self.lruStarting:
                            print("...starting LRU, placing LRU at row[0]col[0]")
                            self.drawFirstLRU(PARAMS, LRU)

                        elif previousLRU == None:
                            print("...other path found?")
                            self.drawLRUfromOtherPath(PARAMS, LRU)

                        else:
                            direction = self.drawLRUnGetDirection(PARAMS, previousLRU, LRU)

                        self.drawnLru_list.append(lru)

                    previousLRU = LRU

    ####################################################################################################################
    ##
    ####################################################################################################################
    def duplicateLRUasNeeded(self, PARAMS):
        print("...duplicate LRUasNeeded")

        for LRU in PARAMS.LRUInterconnectionList:

            # ####SKIPPING ADAPTER??
            if LRU.pin_interconnections_list[0].SOURCE.lruType == "ADAPTER":
                continue

            for dest in LRU.dest_lru_list:
                print(LRU.source_lru, dest)
                previousLRU = PARAMS.getLRUInterconnection(dest)
                self.duplicateLRU(PARAMS, LRU, previousLRU)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def duplicateLRU(self, PARAMS,LRU,previousLRU):
        print("...duplicate LRU if needed")

        if LRU.POSITION.row == previousLRU.POSITION.row:
            LruInBetween = self.checkIfLruInBetween(PARAMS,LRU, previousLRU, same="row")
            if LruInBetween == True:
                self.sameColOrRow_insertPath(PARAMS, LRU, previousLRU,same="row")
        elif LRU.POSITION.col == previousLRU.POSITION.col:
            LruInBetween = self.checkIfLruInBetween(PARAMS,LRU,previousLRU,same="col")
            if LruInBetween == True:
                self.sameColOrRow_insertPath(PARAMS, LRU, previousLRU,same="col")
        else:
            self.diagonal_insertPath(PARAMS, LRU, previousLRU)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def checkIfLruInBetween(self, PARAMS,LRU,previousLRU,same="not_given"):
        status = False

        if same == "row":
            samenum = LRU.POSITION.row
            if LRU.POSITION.col > previousLRU.POSITION.col:
                max = LRU.POSITION.col
                min = previousLRU.POSITION.col
            else:
                max = previousLRU.POSITION.col
                min = LRU.POSITION.col
            status = self.getIfLruInBetween(PARAMS, min, max, same,samenum)

        elif same == "col":
            samenum = LRU.POSITION.col
            if LRU.POSITION.row > previousLRU.POSITION.row:
                max = LRU.POSITION.row
                min = previousLRU.POSITION.row
            else:
                max = previousLRU.POSITION.row
                min = LRU.POSITION.row
            status = self.getIfLruInBetween(PARAMS, min, max, same, samenum)

        else:
            doing = None

        return status

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getIfLruInBetween(self, PARAMS, min,max,same,samenum):
        status = False

        if same == "row":
            for x in range(min+1,max):
                LRU = PARAMS.positionMatrix[samenum][x]
                if type(LRU) == type(CC.Lru_Interconnection()) and LRU.source_lru != "!!BLOCKED!!":
                    status = True
                    break

        elif same == "col":
            for x in range(min + 1, max):
                LRU = PARAMS.positionMatrix[x][samenum]
                if type(LRU) == type(CC.Lru_Interconnection()) and LRU.source_lru != "!!BLOCKED!!":
                    status = True
                    break

        else:
            doing = None

        return status

    ####################################################################################################################
    ##
    ####################################################################################################################
    def sameColOrRow_insertPath(self, PARAMS, LRU, previousLRU,same="not_given"):
        print("...sameColOrRow_insertPath")
        print(LRU.source_lru,",",previousLRU.source_lru)

        if same == "row":
            print("...LRU and previousLRU at same row")
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, LRU.POSITION.row, values=None, axis=0)
            LRUnew, previousLRUnew = self.createLRUconnection(PARAMS, LRU, previousLRU)
            PARAMS.positionMatrix[LRU.POSITION.row][LRU.POSITION.col] = LRUnew
            PARAMS.positionMatrix[LRU.POSITION.row][previousLRU.POSITION.col] = previousLRUnew
            self.updateALLLRUsPositions(PARAMS)
            self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
            self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)
        elif same == "col":
            print("...LRU and previousLRU at same col")
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, LRU.POSITION.col, values=None, axis=1)
            LRUnew, previousLRUnew = self.createLRUconnection(PARAMS, LRU, previousLRU)
            PARAMS.positionMatrix[LRU.POSITION.row][LRU.POSITION.col] = LRUnew
            PARAMS.positionMatrix[previousLRU.POSITION.row][LRU.POSITION.col] = previousLRUnew
            self.updateALLLRUsPositions(PARAMS)
            self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
            self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)
        else:
            doing = None

    ####################################################################################################################
    ##
    ####################################################################################################################
    def diagonal_insertPath(self, PARAMS, LRU, previousLRU):
        print("...diagonally")

        if abs(LRU.POSITION.row - previousLRU.POSITION.row) == 1:
            print("...insert a row")
            if LRU.POSITION.row > previousLRU.POSITION.row:
                insertRow = LRU.POSITION.row
            else:
                insertRow = previousLRU.POSITION.row
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertRow, values=None, axis=0)
            LRUnew, previousLRUnew = self.createLRUconnection(PARAMS, LRU, previousLRU)
            PARAMS.positionMatrix[insertRow][LRU.POSITION.col] = LRUnew
            PARAMS.positionMatrix[insertRow][previousLRU.POSITION.col] = previousLRUnew
            self.updateALLLRUsPositions(PARAMS)
            self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
            self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)
        elif abs(LRU.POSITION.col - previousLRU.POSITION.col) == 1:
            print("...insert a col")
            if LRU.POSITION.col > previousLRU.POSITION.col:
                insertCol = LRU.POSITION.col
            else:
                insertCol = previousLRU.POSITION.col
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertCol, values=None, axis=1)
            LRUnew, previousLRUnew = self.createLRUconnection(PARAMS, LRU, previousLRU)
            PARAMS.positionMatrix[LRU.POSITION.row][insertCol] = LRUnew
            PARAMS.positionMatrix[previousLRU.POSITION.row][insertCol] = previousLRUnew
            self.updateALLLRUsPositions(PARAMS)
            self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
            self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)
        else:
            print("...far away, insert row and col")
            if LRU.POSITION.row > previousLRU.POSITION.row:
                insertRow = LRU.POSITION.row
                if LRU.POSITION.col > previousLRU.POSITION.col:
                    insertCol = previousLRU.POSITION.col + 1
                else:
                    insertCol = previousLRU.POSITION.col
                PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertCol, values=None, axis=1)
                PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertRow, values=None, axis=0)
                self.updateALLLRUsPositions(PARAMS)
                LRUnew, LRUmid, previousLRUnew = self.createLRUconnection2(PARAMS, LRU, LRU, previousLRU)
                PARAMS.positionMatrix[insertRow][insertCol] = LRUmid
                PARAMS.positionMatrix[insertRow][LRU.POSITION.col] = LRUnew
                PARAMS.positionMatrix[previousLRU.POSITION.row][insertCol] = previousLRUnew
                self.updateALLLRUsPositions(PARAMS)
                self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
                self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)
            else:
                insertRow = previousLRU.POSITION.row
                if LRU.POSITION.col > previousLRU.POSITION.col:
                    insertCol = LRU.POSITION.col
                else:
                    insertCol = LRU.POSITION.col + 1
                PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertCol, values=None, axis=1)
                PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, insertRow, values=None, axis=0)
                self.updateALLLRUsPositions(PARAMS)
                LRUnew, LRUmid, previousLRUnew = self.createLRUconnection2(PARAMS, LRU, previousLRU, previousLRU)
                PARAMS.positionMatrix[LRU.POSITION.row][insertCol] = LRUnew
                PARAMS.positionMatrix[insertRow][insertCol] = LRUmid
                PARAMS.positionMatrix[insertRow][previousLRU.POSITION.col] = previousLRUnew
                self.updateALLLRUsPositions(PARAMS)
                self.checkLRUforOverlapConnection(PARAMS, LRU, LRUnew)
                self.checkLRUforOverlapConnection(PARAMS, previousLRU, previousLRUnew)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def createLRUconnection2(self, PARAMS, LRU, LRUmid, previousLRU):
        print("...createLRUconnection2")
        print(LRU.source_lru,LRUmid.source_lru,previousLRU.source_lru)

		## APPEND THIS FOR FUTURE USE
        _LRU = copy.deepcopy(LRU)
        _previousLRU = copy.deepcopy(previousLRU)
        PARAMS.lrusExpandedList.append(_LRU)
        PARAMS.lrusExpandedList.append(_previousLRU)

        LRUnew = copy.deepcopy(LRU)
        LRUcopy = copy.deepcopy(LRU)
        LRUmidnew = copy.deepcopy(LRUmid)
        LRUmidnewcopy = copy.deepcopy(LRUmid)
        previousLRUnew = copy.deepcopy(previousLRU)
        previousLRUcopy = copy.deepcopy(previousLRU)

		## UPDATE source_lru OF NEW LRUs
        LRUnew.source_lru = LRU.source_lru + PARAMS.delimeterDuplicatingLRU + previousLRU.source_lru
        LRUmidnew.source_lru = LRUmid.source_lru + PARAMS.delimeterDuplicatingLRU + previousLRU.source_lru + "2"
        previousLRUnew.source_lru = previousLRU.source_lru + PARAMS.delimeterDuplicatingLRU + LRU.source_lru

        if LRU.source_lru == LRUmid.source_lru:
            midConnectionLRU = copy.deepcopy(previousLRUnew)
            midConnectionLRUbefore = copy.deepcopy(previousLRU)
            sameConnectionLRU = copy.deepcopy(LRUnew)
        else:
            midConnectionLRU = copy.deepcopy(LRUnew)
            midConnectionLRUbefore = copy.deepcopy(LRU)
            sameConnectionLRU = copy.deepcopy(previousLRUnew)

        print(LRUnew.source_lru,LRUmidnew.source_lru,previousLRUnew.source_lru )

		## DELETE pin_interconnections_list OF NEW LRUs
        LRUnew.pin_interconnections_list = []
        LRUmidnew.pin_interconnections_list = []
        previousLRUnew.pin_interconnections_list = []

		## DELETE dest_lru_list OF NEW LRUs
        LRUnew.dest_lru_list = []
        LRUmidnew.dest_lru_list = []
        previousLRUnew.dest_lru_list = []

		## UPDATE lruType OF ORIGINAL LRU
        for pin in LRU.pin_interconnections_list:
            if pin.SOURCE.lruType.endswith('SAME'):
                doing = None
            else:
                pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"

		## UDPATE lruType OF ORIGINAL previousLRU
        for pin in previousLRU.pin_interconnections_list:
            if pin.SOURCE.lruType.endswith('SAME'):
                doing = None
            else:
                pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"

		## SET NEW pin_interconnections_list AND dest_lru_list FOR Lrunew
        for pin in LRUcopy.pin_interconnections_list:
            if pin.DEST.lru == previousLRU.source_lru:
                TEMP_PIN = self.getTempPin(pin,LRUnew,LRU,sameLruType=True)
                LRUnew.pin_interconnections_list.append(TEMP_PIN)
                LRUnew.dest_lru_list.append(LRU.source_lru)
                break

		## SET NEW pin_interconnections_list AND dest_lru_list FOR previousLRUnew
        for pin in previousLRUcopy.pin_interconnections_list:
            if pin.DEST.lru == LRU.source_lru:
                TEMP_PIN = self.getTempPin(pin, previousLRUnew, previousLRU,sameLruType=True)
                previousLRUnew.pin_interconnections_list.append(TEMP_PIN)
                previousLRUnew.dest_lru_list.append(previousLRU.source_lru)
                break

        for pin in LRUmidnewcopy.pin_interconnections_list:
            if pin.DEST.lru == midConnectionLRUbefore.source_lru:
                pin.SOURCE.lru = LRUmidnew.source_lru
                # pin.SOURCE.type = type_text
                if pin.SOURCE.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"
                pin.DEST.lru = midConnectionLRU.source_lru
                # pin.DEST.type = type_text
                if pin.DEST.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.DEST.lruType = pin.DEST.lruType + "SAME"
                LRUmidnew.pin_interconnections_list.append(pin)
                LRUmidnew.dest_lru_list.append(midConnectionLRU.source_lru)

                TEMP_PIN = self.getTempPin(pin, LRUmidnew, sameConnectionLRU,sameLruType=True)
                LRUmidnew.pin_interconnections_list.append(TEMP_PIN)
                LRUmidnew.dest_lru_list.append(sameConnectionLRU.source_lru)
                break

		## REMOVE OLD pin_interconnections_list
        pin_temp = None
        for pin in LRU.pin_interconnections_list:
            if pin.DEST.lru == previousLRU.source_lru:
                pin_temp = pin
				## REMOVE OLD PIN
                LRU.pin_interconnections_list.remove(pin)
		## ADD UPDATED PIN
        TEMP_PIN = self.getTempPin(pin, LRU, LRUnew)
        LRU.pin_interconnections_list.append(TEMP_PIN)
        LRU.dest_lru_list.append(LRUnew.source_lru)

		## REMOVE OLD pin_interconnections_list
        pin_temp = None
        for pin in previousLRU.pin_interconnections_list:
            if pin.DEST.lru == LRU.source_lru:
                pin_temp = pin
				## REMOVE OLD PIN
                previousLRU.pin_interconnections_list.remove(pin)
		## ADD UPDATED PIN
        TEMP_PIN = self.getTempPin(pin, previousLRU, previousLRUnew)
        previousLRU.pin_interconnections_list.append(TEMP_PIN)
        previousLRU.dest_lru_list.append(previousLRUnew.source_lru)

		## REMOVE OLD dest_lru_list
        for lru in LRU.dest_lru_list:
            if lru == previousLRU.source_lru:
                LRU.dest_lru_list.remove(lru)

        ## REMOVE OLD dest_lru_list
        for lru in previousLRU.dest_lru_list:
            if lru == LRU.source_lru:
                previousLRU.dest_lru_list.remove(lru)

		## APPEND NEW LRU INTO LRUInterconnectionList
        PARAMS.LRUInterconnectionList.append(LRUnew)
        print("...appending to PARAMS.LRUInterconnectionList:", LRUnew.source_lru)
        PARAMS.LRUInterconnectionList.append(LRUmidnew)
        print("...appending to PARAMS.LRUInterconnectionList:", LRUmidnew.source_lru)
        PARAMS.LRUInterconnectionList.append(previousLRUnew)
        print("...appending to PARAMS.LRUInterconnectionList:", previousLRUnew.source_lru)


        return LRUnew, LRUmidnew, previousLRUnew

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getTempPin(self, pin, LRUnew, LRU,sameLruType=False):
        conn_text = ""
        pin_text = ""
        type_text = "same"

        print(LRUnew.source_lru,LRU.source_lru)

        TEMP_PIN = CC.Pin_Interconnection()
        TEMP_PIN.SOURCE.lru = LRUnew.source_lru
        TEMP_PIN.SOURCE.lru_label = pin.SOURCE.lru_label
        TEMP_PIN.SOURCE.conn = conn_text
        TEMP_PIN.SOURCE.pin = pin_text
        TEMP_PIN.SOURCE.type = type_text

        if sameLruType == True:
            if pin.SOURCE.lruType.endswith('SAME'):
                TEMP_PIN.SOURCE.lruType = pin.SOURCE.lruType
            else:
                TEMP_PIN.SOURCE.lruType = pin.SOURCE.lruType + "SAME"
        else:
            TEMP_PIN.SOURCE.lruType = pin.SOURCE.lruType

        TEMP_PIN.DEST.lru = LRU.source_lru
        TEMP_PIN.DEST.conn = conn_text
        TEMP_PIN.DEST.pin = pin_text
        TEMP_PIN.DEST.type = type_text
        TEMP_PIN.DEST.lruType = pin.DEST.lruType

        return TEMP_PIN

    ####################################################################################################################
    ##
    ####################################################################################################################
    def createLRUconnection(self, PARAMS, LRU, previousLRU):
        print("...createLRUconnection")
        print(LRU.source_lru,",",previousLRU.source_lru)

		## APPEND THIS FOR FUTURE USE
        _LRU = copy.deepcopy(LRU)
        _previousLRU = copy.deepcopy(previousLRU)
        PARAMS.lrusExpandedList.append(_LRU)
        PARAMS.lrusExpandedList.append(_previousLRU)

        conn_text = ""
        pin_text = ""
        type_text = "same"

        LRUnew = copy.deepcopy(LRU)
        LRUcopy = copy.deepcopy(LRU)
        previousLRUnew = copy.deepcopy(previousLRU)
        previousLRUcopy = copy.deepcopy(previousLRU)

		## UPDATE source_lru OF NEW LRUs
        LRUnew.source_lru = LRU.source_lru + PARAMS.delimeterDuplicatingLRU + previousLRU.source_lru
        previousLRUnew.source_lru = previousLRU.source_lru + PARAMS.delimeterDuplicatingLRU + LRU.source_lru

		## DELETE pin_interconnections_list OF NEW LRUs
        LRUnew.pin_interconnections_list = []
        previousLRUnew.pin_interconnections_list = []

		## DELETE dest_lru_list OF NEW LRUS
        LRUnew.dest_lru_list = []
        previousLRUnew.dest_lru_list = []

		## UDPATE lruType OF ORIGINAL LRU
        for pin in LRU.pin_interconnections_list:
            if pin.SOURCE.lruType.endswith('SAME'):
                doing = None
            else:
                pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"

		## UDPATE lruType OF ORIGINAL previousLRU
        for pin in previousLRU.pin_interconnections_list:
            if pin.SOURCE.lruType.endswith('SAME'):
                doing = None
            else:
                pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"

		## SET NEW pin_interconnections_list AND dest_lru_list FOR LRUnew
        print("LRU pin interconnection dest list")
        for pin in LRUcopy.pin_interconnections_list:
            print(pin.DEST.lru)
        pin_temp = None
        for pin in LRUcopy.pin_interconnections_list:
            if pin.DEST.lru == previousLRU.source_lru:
                pin_temp = pin
                pin.SOURCE.lru = LRUnew.source_lru
                #pin.SOURCE.type = type_text
                if pin.SOURCE.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"
                pin.DEST.lru = previousLRUnew.source_lru
                #pin.DEST.type = type_text
                if pin.DEST.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.DEST.lruType = pin.DEST.lruType + "SAME"
                LRUnew.pin_interconnections_list.append(pin)
                LRUnew.dest_lru_list.append(previousLRUnew.source_lru)

        TEMP_PIN = self.getTempPin(pin_temp, LRUnew, LRU)
        LRUnew.pin_interconnections_list.append(TEMP_PIN)
        print("...appending", LRU.source_lru,"in dest_lru_list of", LRUnew.source_lru)
        LRUnew.dest_lru_list.append(LRU.source_lru)

		## REMOVE DUPLICATES
        LRUnew.dest_lru_list = list(set(LRUnew.dest_lru_list))

		## SET NEW pin_interconnections_list AND dest_lru_list FOR previousLRUnew
        print("previousLRU pin interconnection dest list")
        for pin in previousLRUcopy.pin_interconnections_list:
            print(pin.DEST.lru)
        pin_temp = None
        for pin in previousLRUcopy.pin_interconnections_list:
            if pin.DEST.lru == LRU.source_lru:
                pin_temp = pin
                pin.SOURCE.lru = previousLRUnew.source_lru
                #pin.SOURCE.type = type_text
                if pin.SOURCE.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.SOURCE.lruType = pin.SOURCE.lruType + "SAME"
                pin.DEST.lru = LRUnew.source_lru
                #pin.DEST.type = type_text
                if pin.DEST.lruType.endswith('SAME'):
                    doing = None
                else:
                    pin.DEST.lruType = pin.DEST.lruType + "SAME"
                previousLRUnew.pin_interconnections_list.append(pin)
                previousLRUnew.dest_lru_list.append(LRUnew.source_lru)

        TEMP_PIN = self.getTempPin(pin_temp, previousLRUnew, previousLRU)
        previousLRUnew.pin_interconnections_list.append(TEMP_PIN)
        print("...appending", previousLRU.source_lru, "in dest_lru_list of", previousLRUnew.source_lru)
        previousLRUnew.dest_lru_list.append(previousLRU.source_lru)

        previousLRUnew.dest_lru_list = list(set(previousLRUnew.dest_lru_list))

        print("LRUnew:", LRUnew.source_lru, LRUnew.dest_lru_list)
        print("previousLRUnew:", previousLRUnew.source_lru, previousLRUnew.dest_lru_list)

		## REMOVE OLD pin_interconnections_list
        print("LRU:",LRU.source_lru,LRU.dest_lru_list)
        pin_temp = None
        for pin in LRU.pin_interconnections_list:
            if pin.DEST.lru == previousLRU.source_lru:
                pin_temp = pin
				## REMOVE OLD PIN
                LRU.pin_interconnections_list.remove(pin)
		## ADD UPDATED PIN
        TEMP_PIN = self.getTempPin(pin_temp, LRU, LRUnew)
        LRU.pin_interconnections_list.append(TEMP_PIN)
        LRU.dest_lru_list.append(LRUnew.source_lru)

		## REMOVE OLD pin_interconnections_list
        print("previousLRU:",previousLRU.source_lru, previousLRU.dest_lru_list)
        pin_temp = None
        for pin in previousLRU.pin_interconnections_list:
            if pin.DEST.lru == LRU.source_lru:
                pin_temp = pin
				## REMOVE OLD PIN
                previousLRU.pin_interconnections_list.remove(pin)
		## ADD UPDATED PIN
        TEMP_PIN = self.getTempPin(pin_temp, previousLRU, previousLRUnew)
        previousLRU.pin_interconnections_list.append(TEMP_PIN)
        previousLRU.dest_lru_list.append(previousLRUnew.source_lru)

		## REMOVE OLD dest_lru_list
        for lru in LRU.dest_lru_list:
            if lru == previousLRU.source_lru:
                LRU.dest_lru_list.remove(lru)
        print("test", LRU.dest_lru_list)

		## REMOVE OLD dest_lru_list
        for lru in previousLRU.dest_lru_list:
            if lru == LRU.source_lru:
                previousLRU.dest_lru_list.remove(lru)
        print("test", previousLRU.dest_lru_list)

		## APPEND NEW LRU INTO LRUInterconnectionList
        PARAMS.LRUInterconnectionList.append(LRUnew)
        print("...appending to PARAMS.LRUInterconnectionList:", LRUnew.source_lru)
        PARAMS.LRUInterconnectionList.append(previousLRUnew)
        print("...appending to PARAMS.LRUInterconnectionList:", previousLRUnew.source_lru)

        return LRUnew, previousLRUnew

    ####################################################################################################################
    ##
    ####################################################################################################################
    def checkLRUforOverlapConnection(self, PARAMS, LRU, LRUnew):
        print("...checkOrigLRUConnectionForOverlap")
        if LRU.POSITION.row == LRUnew.POSITION.row:
            same = "row"
        else:
            same = "col"

        print(same)

        for dest in LRU.dest_lru_list:
            print(dest)
            LRU2 = PARAMS.getLRUInterconnection(dest)

            if same == "row":
                if LRU.POSITION.row == LRU2.POSITION.row:
                    print(LRU2.source_lru, "is same row")
                    if abs(LRU.POSITION.col - LRU2.POSITION.col) > abs(LRUnew.POSITION.col - LRU2.POSITION.col):
                        self.movePINfromLRUtoLRUnew(PARAMS, LRU, LRUnew, LRU2)
            else:
                if LRU.POSITION.col == LRU2.POSITION.col:
                    print(LRU2.source_lru, "is same col")
                    if abs(LRU.POSITION.row - LRU2.POSITION.row) > abs(LRUnew.POSITION.row - LRU2.POSITION.row):
                        self.movePINfromLRUtoLRUnew(PARAMS, LRU, LRUnew, LRU2)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def movePINfromLRUtoLRUnew(self, PARAMS, LRU, LRUnew, LRU2):
        print("...movePINfromLRUtoLRUnew")
        if LRUnew.source_lru == LRU2.source_lru:
            doing = None
        else:
            print(LRU.source_lru,",",LRUnew.source_lru,",",LRU2.source_lru)
            print(LRU.dest_lru_list)
            if len(LRU.dest_lru_list) == 1 or (len(LRU.dest_lru_list) == 2 and (LRUnew.source_lru in LRU.dest_lru_list)):
                print("...will delete", LRUnew.source_lru, ". Keeping", LRU.source_lru , "instead, but place it in ", LRUnew.source_lru, "position")

                copiedPIN = None
                
				## REMOVE ODL pin_interconnections_list
                for pin in LRU.pin_interconnections_list:
                    if pin.DEST.lru == LRU2.source_lru:
                        copiedPIN = copy.deepcopy(pin)
                        copiedPIN.SOURCE.lru = LRUnew.source_lru
                        LRUnew.pin_interconnections_list.append(copiedPIN)
                        LRUnew.dest_lru_list.append(LRU2.source_lru)
						## REMOVE OLD PIN
                        LRU.pin_interconnections_list.remove(pin)
                LRUnew.dest_lru_list = list(set(LRUnew.dest_lru_list))

				## REMOVE OLD pin_interconnections_list
                for pin in LRU2.pin_interconnections_list:
                    if pin.DEST.lru == LRU.source_lru:
                        copiedPIN = copy.deepcopy(pin)
                        copiedPIN.SOURCE.lru = LRU2.source_lru
                        LRU2.pin_interconnections_list.append(copiedPIN)
                        LRU2.dest_lru_list.append(LRUnew.source_lru)
						## REMOVE OLD PIN
                        LRU2.pin_interconnections_list.remove(pin)
                LRU2.dest_lru_list = list(set(LRU2.dest_lru_list))

				## REMOVE OLD dest_lru_list
                for lru in LRU.dest_lru_list:
                    if lru == LRU2.source_lru:
                        LRU.dest_lru_list.remove(lru)

                ## REMOVE OLD dest_lru_list
                for lru in LRU2.dest_lru_list:
                    if lru == LRU.source_lru:
                        LRU2.dest_lru_list.remove(lru)

				## REMOVE OLD pin_interconnections_list
                for pin in LRUnew.pin_interconnections_list:
                    if pin.DEST.lru == LRU.source_lru:
                        LRUnew.pin_interconnections_list.remove(pin)

				## REMOVE OLD dest_lru_list
                for lru in LRUnew.dest_lru_list:
                    if lru == LRU.source_lru:
                        LRUnew.dest_lru_list.remove(lru)

                ## remove LRU that no longer have any connections
                PARAMS.positionMatrix[LRU.POSITION.row][LRU.POSITION.col] = None
                for LRU_ in PARAMS.LRUInterconnectionList:
                    if LRU_.source_lru == LRU.source_lru:
                        PARAMS.LRUInterconnectionList.remove(LRU_)

                ## update LRUnew lruType to no longer have 'SAME'
                for pin in LRUnew.pin_interconnections_list:
                    if pin.SOURCE.lruType.endswith('SAME'):
                        pin.SOURCE.lruType = pin.SOURCE.lruType[:-4]


            else:
                copiedPIN = None

                ## remove old pin_interconnections_list
                for pin in LRU.pin_interconnections_list:
                    if pin.DEST.lru == LRU2.source_lru:
                        copiedPIN = copy.deepcopy(pin)
                        copiedPIN.SOURCE.lru = LRUnew.source_lru
                        LRUnew.pin_interconnections_list.append(copiedPIN)
                        LRUnew.dest_lru_list.append(LRU2.source_lru)
                        ## remove old pin
                        LRU.pin_interconnections_list.remove(pin)
                LRUnew.dest_lru_list = list(set(LRUnew.dest_lru_list))

                ## remove old pin_interconnections_list
                for pin in LRU2.pin_interconnections_list:
                    if pin.DEST.lru == LRU.source_lru:
                        copiedPIN = copy.deepcopy(pin)
                        copiedPIN.SOURCE.lru = LRU2.source_lru
                        LRU2.pin_interconnections_list.append(copiedPIN)
                        LRU2.dest_lru_list.append(LRUnew.source_lru)
                        ## remove old pin
                        LRU2.pin_interconnections_list.remove(pin)
                LRU2.dest_lru_list = list(set(LRU2.dest_lru_list))


                ## remove old dest_lru_list
                for lru in LRU.dest_lru_list:
                    if lru == LRU2.source_lru:
                        LRU.dest_lru_list.remove(lru)

                ## remove old dest_lru_list
                for lru in LRU2.dest_lru_list:
                    if lru == LRU.source_lru:
                        LRU2.dest_lru_list.remove(lru)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def reorganizePathsByLength(self, PATH_list):
        print("...reorganizing paths by length")

        temp_dict = {}

        for paths in PATH_list:

            length = len(paths)
            print(paths, length)
            try:
                ## dictionary for it already exist (key of length exist)
                temp_list = temp_dict[length]
                temp_list.append(paths)
                temp_dict[length] = temp_list
            except:
                temp_list = []
                temp_list.append(paths)
                temp_dict[length] = temp_list

        new_path_list = []
        for key in sorted(temp_dict):
            print(key, temp_dict[key])
            for path in temp_dict[key]:
                new_path_list.append(path)

        reversed_path_list = []
        for path in reversed(new_path_list):
            reversed_path_list.append(path)

        return reversed_path_list


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getEmptyDirection(self, PARAMS, previousLRU):
        print("...finding empty location")
        inserting = False

        if self.settings["GridView"]["more_random"] == "True":
            dict_list = self.getRandomDict_list(previousLRU.isEmptyDict)
            dict_list2 = self.getRandomDict_list(previousLRU.isEmptyDict2)
        else:
            dict_list = previousLRU.isEmptyDict.keys()
            dict_list2 = previousLRU.isEmptyDict2.keys()

        #for key, value in previousLRU.isEmptyDict.items():
        for direction in dict_list:
            value = previousLRU.isEmptyDict[direction]
            if value == True:
                status = self.getAvailability(PARAMS,direction,previousLRU)

                if status == False or status == "OutOfBounds":
                    print("...direction", direction, "status is", status)
                else:
                    return direction, inserting

        print("...will have to insert in OutOfBounds if possible")
        ## will get here if all status is bad, will need to insert
        #for key, value in previousLRU.isEmptyDict.items():
        for direction in dict_list:
            value = previousLRU.isEmptyDict[direction]
            if value == True:
                status = self.getAvailability(PARAMS, direction, previousLRU)

                if status == "OutOfBounds":
                    inserting = True
                    return direction, inserting

        print("...will have to insert")
        ## will get here if all status is bad, will need to insert
        #for key, value in previousLRU.isEmptyDict.items():
        for direction in dict_list:
            value = previousLRU.isEmptyDict[direction]
            if value == True:
                inserting = True
                return direction, inserting

        print("...up down left right all not available")
        print(previousLRU.source_lru)
        ## will get here if all status is bad, cannot insert in up, down, left, right
        for direction in dict_list2:
            value = previousLRU.isEmptyDict2[direction]
            if value == True:
                inserting = True
                return direction, inserting

        print("...up down left right upleft upright downleft downright all not available")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def isInserting(self, PARAMS, previousLRU, emptyDirection):
        status = self.getAvailability(PARAMS, emptyDirection, previousLRU)

        if status == False or status == "OutOfBounds":
            isInserting = True
            return isInserting
        else:
            isInserting = False
            return isInserting

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getBestDirection(self, PARAMS, LRU,direction1, direction2):
        print("...at getBestDirection")
        status1 = self.getAvailability(PARAMS,direction1,LRU)
        status2 = self.getAvailability(PARAMS, direction2, LRU)

        if status1 == True:
            return direction1
        elif status2 == True:
            return direction2
        elif status1 == False and status2 == "OutOfBounds":
            return direction2
        elif status2 == False and status1 == "OutOfBounds":
            return direction1
        else:
            return direction1

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getAvailability(self, PARAMS, emptyDirection, previousLRU):
        print("...at getAvailability")

        maxrow, maxcol = PARAMS.positionMatrix.shape

        if emptyDirection == PARAMS.directionDict["left"]:
            atRow = previousLRU.POSITION.row
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict["right"]:
            atRow = previousLRU.POSITION.row
            atCol = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict["up"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict["down"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict2["upleft"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["upright"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict2["downleft"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["downright"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col + 1
        else:
            doing = None

        print("atRow:", atRow, "atCol", atCol)

        if atRow < 0 or atRow > maxrow - 1 or atCol < 0 or atCol > maxcol - 1:
            print("...out of bounds")
            status = "OutOfBounds"
        elif PARAMS.positionMatrix[atRow][atCol] == None:
            status = True
        else:
            status = False

        return status

    ####################################################################################################################
    ##
    ####################################################################################################################
    def placeLRUInMatrix(self, PARAMS, emptyDirection, previousLRU, LRU):
        print("...at placeLRUInMatrix")
        if emptyDirection == PARAMS.directionDict["left"]:
            atRow = previousLRU.POSITION.row
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict["right"]:
            atRow = previousLRU.POSITION.row
            atCol = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict["up"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict["down"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict2["upleft"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["upright"]:
            atRow = previousLRU.POSITION.row - 1
            atCol = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict2["downleft"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["downright"]:
            atRow = previousLRU.POSITION.row + 1
            atCol = previousLRU.POSITION.col + 1
        else:
            doing = None

        print("...placing ", LRU.source_lru, "at row[",atRow,"] col[",atCol,"]")
        PARAMS.positionMatrix[atRow][atCol] = LRU
        print("...placed")

        self.forPrintingMatrix(PARAMS)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def updateLRUsIsEmptyDict(self, PARAMS,emptyDirection,previousLRU, LRU):
        print("...at updateLRUsIsEmptyDict with emptyDirection", emptyDirection)
        print(previousLRU.source_lru,"at",previousLRU.POSITION.row,previousLRU.POSITION.col, LRU.source_lru,"at",LRU.POSITION.row,LRU.POSITION.col)
        if emptyDirection == PARAMS.directionDict["left"]:
            previousLRU.isEmptyDict[emptyDirection] = False
            LRU.isEmptyDict[PARAMS.directionDict["right"]] = False
        elif emptyDirection == PARAMS.directionDict["right"]:
            previousLRU.isEmptyDict[emptyDirection] = False
            LRU.isEmptyDict[PARAMS.directionDict["left"]] = False
        elif emptyDirection == PARAMS.directionDict["up"]:
            previousLRU.isEmptyDict[emptyDirection] = False
            LRU.isEmptyDict[PARAMS.directionDict["down"]] = False
        elif emptyDirection == PARAMS.directionDict["down"]:
            previousLRU.isEmptyDict[emptyDirection] = False
            LRU.isEmptyDict[PARAMS.directionDict["up"]] = False
        # elif emptyDirection == PARAMS.directionDict2["upleft"]:
        #     previousLRU.isEmptyDict2[emptyDirection] = False
        #     LRU.isEmptyDict2[PARAMS.directionDict2["downright"]] = False
        # elif emptyDirection == PARAMS.directionDict2["upright"]:
        #     previousLRU.isEmptyDict2[emptyDirection] = False
        #     LRU.isEmptyDict2[PARAMS.directionDict2["downleft"]] = False
        # elif emptyDirection == PARAMS.directionDict2["downleft"]:
        #     previousLRU.isEmptyDict2[emptyDirection] = False
        #     LRU.isEmptyDict2[PARAMS.directionDict2["upright"]] = False
        # elif emptyDirection == PARAMS.directionDict2["downright"]:
        #     previousLRU.isEmptyDict2[emptyDirection] = False
        #     LRU.isEmptyDict2[PARAMS.directionDict2["upleft"]] = False
        else:
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def insertRowCol(self, PARAMS, emptyDirection, previousLRU):
        print("...at insertRowCol with emptyDirection", emptyDirection, "row:",previousLRU.POSITION.row,"col:",previousLRU.POSITION.col)

        maxrow, maxcol = PARAMS.positionMatrix.shape
        print("maxrow: ", maxrow, "maxcol:", maxcol)
        self.forPrintingMatrix(PARAMS)

        if emptyDirection == PARAMS.directionDict["left"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.col, values=None, axis=1)
            self.blockOnInserted(PARAMS,emptyDirection,previousLRU.POSITION.col + 1, previousLRU.POSITION.col)
        elif emptyDirection == PARAMS.directionDict["right"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.col + 1, values=None, axis=1)
            self.blockOnInserted(PARAMS, emptyDirection, previousLRU.POSITION.col, previousLRU.POSITION.col + 1)
        elif emptyDirection == PARAMS.directionDict["up"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.row, values=None, axis=0)
            self.blockOnInserted(PARAMS, emptyDirection, previousLRU.POSITION.row + 1, previousLRU.POSITION.row)
        elif emptyDirection == PARAMS.directionDict["down"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.row+1, values=None, axis=0)
            self.blockOnInserted(PARAMS, emptyDirection, previousLRU.POSITION.row,previousLRU.POSITION.row+1)
        elif emptyDirection == PARAMS.directionDict2["upleft"] or emptyDirection == PARAMS.directionDict2["downleft"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.col, values=None, axis=1)
            self.blockOnInserted(PARAMS, emptyDirection, previousLRU.POSITION.col + 1, previousLRU.POSITION.col)
        elif emptyDirection == PARAMS.directionDict2["upright"] or emptyDirection == PARAMS.directionDict2["downright"]:
            PARAMS.positionMatrix = numpy.insert(PARAMS.positionMatrix, previousLRU.POSITION.col + 1, values=None,axis=1)
            self.blockOnInserted(PARAMS, emptyDirection, previousLRU.POSITION.col, previousLRU.POSITION.col + 1)
        else:
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setLRUsPosition(self, PARAMS,emptyDirection, previousLRU, LRU):
        if emptyDirection == PARAMS.directionDict["left"]:
            LRU.POSITION.row = previousLRU.POSITION.row
            LRU.POSITION.col = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict["right"]:
            LRU.POSITION.row = previousLRU.POSITION.row
            LRU.POSITION.col = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict["up"]:
            LRU.POSITION.row = previousLRU.POSITION.row - 1
            LRU.POSITION.col = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict["down"]:
            LRU.POSITION.row = previousLRU.POSITION.row + 1
            LRU.POSITION.col = previousLRU.POSITION.col
        elif emptyDirection == PARAMS.directionDict2["upleft"]:
            LRU.POSITION.row = previousLRU.POSITION.row - 1
            LRU.POSITION.col = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["upright"]:
            LRU.POSITION.row = previousLRU.POSITION.row - 1
            LRU.POSITION.col = previousLRU.POSITION.col + 1
        elif emptyDirection == PARAMS.directionDict2["downleft"]:
            LRU.POSITION.row = previousLRU.POSITION.row + 1
            LRU.POSITION.col = previousLRU.POSITION.col - 1
        elif emptyDirection == PARAMS.directionDict2["downright"]:
            LRU.POSITION.row = previousLRU.POSITION.row + 1
            LRU.POSITION.col = previousLRU.POSITION.col + 1
        else:
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def updateALLLRUsPositions(self, PARAMS):
        print("...assigning/updating LRU its positions base on the matrix")

        rows, cols = PARAMS.positionMatrix.shape

        for row in range(0, rows):
            for col in range(0, cols):
                LRU = PARAMS.positionMatrix[row][col]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    LRU.POSITION.row = row
                    LRU.POSITION.col = col

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def deleteBlocks(self, PARAMS):
        print("...deleting blocks")

        rows, cols = PARAMS.positionMatrix.shape

        for row in range(0, rows):
            for col in range(0, cols):
                LRU = PARAMS.positionMatrix[row][col]
                if type(LRU) == type(CC.Lru_Interconnection()) and LRU.source_lru == "!!BLOCKED!!":
                    PARAMS.positionMatrix[row][col] = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawingLoops(self, PARAMS, previousLRU, _LRU):
        print("...drawing loop")
        for key, value in PARAMS.LoopsDict.items():
            if _LRU.source_lru == key:
                LRU = PARAMS.getLRUInterconnection(key)

                print("loop's Paths:", value[0]["Paths"])
                print("loop's Loop1:", value[0]["Loop1"])
                print("loop's Loop1 End:", value[0]["Loop1_End"])
                print("loop's LoopCorner:", value[0]["LoopCorner"])

                ## drawing loops at on the loop path
                if previousLRU == None:
                    if self.drawnLru_list == []:
                        print("...first to be drawn")
                        self.drawFirstLRU(PARAMS, LRU)

                        for directionvalue in PARAMS.directionDict.values():
                            ## picking first direction, will change per run
                            direction = directionvalue
                            break
                    else:
                        print("...not connected from previous paths")
                        self.drawLRUfromOtherPath(PARAMS, LRU)
                        for directionvalue in PARAMS.directionDict.values():
                            ## picking first direction, will change per run
                            direction = directionvalue
                            break
                else:
                    direction = self.drawLRUnGetDirection(PARAMS, previousLRU, LRU)

                self.drawnLru_list.append(key)

                previousLRU = LRU
                print("...Direction is", direction)
                direction1 = direction

                if direction1 == PARAMS.directionDict["left"]:
                    directionCorner = self.getBestDirection(PARAMS,LRU,PARAMS.directionDict["up"],PARAMS.directionDict["down"])
                elif direction1 == PARAMS.directionDict["right"]:
                    directionCorner = self.getBestDirection(PARAMS,LRU, PARAMS.directionDict["down"], PARAMS.directionDict["up"])
                elif direction1 == PARAMS.directionDict["up"]:
                    directionCorner = self.getBestDirection(PARAMS,LRU, PARAMS.directionDict["right"], PARAMS.directionDict["left"])
                elif direction1 == PARAMS.directionDict["down"]:
                    directionCorner = self.getBestDirection(PARAMS,LRU, PARAMS.directionDict["left"], PARAMS.directionDict["right"])
                elif direction1 == PARAMS.directionDict2["upleft"]:
                    directionCorner = self.getBestDirection(PARAMS, LRU, PARAMS.directionDict["down"],PARAMS.directionDict["right"])
                elif direction1 == PARAMS.directionDict2["upright"]:
                    directionCorner = self.getBestDirection(PARAMS, LRU, PARAMS.directionDict["down"],PARAMS.directionDict["left"])
                elif direction1 == PARAMS.directionDict2["downleft"]:
                    directionCorner = self.getBestDirection(PARAMS, LRU, PARAMS.directionDict["up"],PARAMS.directionDict["right"])
                elif direction1 == PARAMS.directionDict2["downright"]:
                    directionCorner = self.getBestDirection(PARAMS, LRU, PARAMS.directionDict["up"],PARAMS.directionDict["left"])
                else:
                    doing = None

                ## go through Loop1
                for x in range(0, len(value[0]["Loop1"])):
                    if x == 0:
                        doing = None
                    else:
                        print("...at loop1 lru:", value[0]["Loop1"][x])
                        LRU = PARAMS.getLRUInterconnection(value[0]["Loop1"][x])
                        print("direction = ", direction)
                        self.drawLRUwithDirection(PARAMS, previousLRU, LRU, direction1)
                        self.drawnLru_list.append(LRU.source_lru)
                        previousLRU = LRU

                ## go through Loop1_Corner (2nd)
                LRU = PARAMS.getLRUInterconnection(value[0]["LoopCorner"][1])
                print("...at LoopCorner lru:", value[0]["LoopCorner"][1])
                previousLRU = PARAMS.getLRUInterconnection(value[0]["Loops_at"])
                Corner2 = LRU
                self.drawLRUwithDirection(PARAMS, previousLRU, LRU, directionCorner)
                self.drawnLru_list.append(LRU.source_lru)

                ## go through Loop1_Corner (1st)
                LRU = PARAMS.getLRUInterconnection(value[0]["LoopCorner"][0])
                print("...at LoopCorner lru:", value[0]["LoopCorner"][0])
                previousLRU = PARAMS.getLRUInterconnection(value[0]["Loop1_End"])
                Corner1 = LRU
                self.drawLRUwithDirection(PARAMS, previousLRU, LRU, directionCorner)
                self.drawnLru_list.append(LRU.source_lru)

                ## update empty dict and block corners
                self.updateLRUsIsEmptyDict(PARAMS,direction1,Corner2,Corner1)
                self.blockBetweenCorners(PARAMS,Corner1,Corner2)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def blockOnInserted(self, PARAMS, direction, previousNum, insertedNum):
        print("...block on inserted: direction:", direction,"previousNum:",previousNum, "insertedNum:",insertedNum)

        maxrow, maxcol = PARAMS.positionMatrix.shape
        print("maxrow: ", maxrow, "maxcol:", maxcol)
        self.forPrintingMatrix(PARAMS)

        if direction == "up":
            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.dest_lru_list = ["!!BLOCKED!!","!!BLOCKED!!"]
            LRUblock.isEmptyDict["up"] = False
            LRUblock.isEmptyDict["down"] = False

            for x in range(0,maxcol):
                LRU = PARAMS.positionMatrix[previousNum][x]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    if LRU.isEmptyDict["up"] == False:
                        print(LRU.source_lru)
                        byItselfLRUpushed, LRUpushed, byItselfpreviousLRU = self.isLRUbyItself(PARAMS,insertedNum-1,x,LRU)
                        if byItselfLRUpushed == True:
                            PARAMS.positionMatrix[insertedNum][x] = LRUpushed
                            PARAMS.positionMatrix[insertedNum-1][x] = None
                        elif byItselfpreviousLRU == True:
                            PARAMS.positionMatrix[insertedNum][x] = LRU
                            PARAMS.positionMatrix[insertedNum + 1][x] = None
                        else:
                            PARAMS.positionMatrix[insertedNum][x] = LRUblock

        elif direction == "down":
            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.dest_lru_list = ["!!BLOCKED!!", "!!BLOCKED!!"]
            LRUblock.isEmptyDict["up"] = False
            LRUblock.isEmptyDict["down"] = False

            for x in range(0, maxcol):
                LRU = PARAMS.positionMatrix[previousNum][x]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    if LRU.isEmptyDict["down"] == False:
                        byItselfLRUpushed, LRUpushed, byItselfpreviousLRU = self.isLRUbyItself(PARAMS, insertedNum + 1, x,LRU)
                        if byItselfLRUpushed == True:
                            PARAMS.positionMatrix[insertedNum][x] = LRUpushed
                            PARAMS.positionMatrix[insertedNum+1][x] = None
                        elif byItselfpreviousLRU == True:
                            PARAMS.positionMatrix[insertedNum][x] = LRU
                            PARAMS.positionMatrix[insertedNum - 1][x] = None
                        else:
                            PARAMS.positionMatrix[insertedNum][x] = LRUblock


        elif direction == "right":
            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.dest_lru_list = ["!!BLOCKED!!", "!!BLOCKED!!"]
            LRUblock.isEmptyDict["left"] = False
            LRUblock.isEmptyDict["right"] = False

            for x in range(0, maxrow):
                LRU = PARAMS.positionMatrix[x][previousNum]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    print(LRU.isEmptyDict)
                    if LRU.isEmptyDict["right"] == False:
                        byItselfLRUpushed, LRUpushed, byItselfpreviousLRU = self.isLRUbyItself(PARAMS, x, insertedNum+1,LRU)
                        if byItselfLRUpushed == True:
                            PARAMS.positionMatrix[x][insertedNum] = LRUpushed
                            PARAMS.positionMatrix[x][insertedNum+1] = None
                        elif byItselfpreviousLRU == True:
                            PARAMS.positionMatrix[x][insertedNum] = LRU
                            PARAMS.positionMatrix[x][insertedNum - 1] = None
                        else:
                            PARAMS.positionMatrix[x][insertedNum] = LRUblock

        elif direction == "left":
            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.dest_lru_list = ["!!BLOCKED!!", "!!BLOCKED!!"]
            LRUblock.isEmptyDict["left"] = False
            LRUblock.isEmptyDict["right"] = False

            for x in range(0, maxrow):
                LRU = PARAMS.positionMatrix[x][previousNum]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    if LRU.isEmptyDict["left"] == False:
                        byItselfLRUpushed, LRUpushed, byItselfpreviousLRU = self.isLRUbyItself(PARAMS, x, insertedNum - 1,LRU)
                        if byItselfLRUpushed == True:
                            PARAMS.positionMatrix[x][insertedNum] = LRUpushed
                            PARAMS.positionMatrix[x][insertedNum-1] = None
                        elif byItselfpreviousLRU == True:
                            PARAMS.positionMatrix[x][insertedNum] = LRU
                            PARAMS.positionMatrix[x][insertedNum + 1] = None
                        else:
                            PARAMS.positionMatrix[x][insertedNum] = LRUblock


        else:
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def isLRUbyItself(self,PARAMS,row,col,previousLRU):
        print("PARAMS.positionMatrix.shape",PARAMS.positionMatrix.shape)
        print(previousLRU.source_lru, "at",previousLRU.POSITION.row,previousLRU.POSITION.col)
        print("LRUpushed at",row,col)
        try:
            LRUpushed = PARAMS.positionMatrix[row][col]
        except:
            return False, None, False

        if type(LRUpushed) == type(CC.Lru_Interconnection()):

            if len(LRUpushed.dest_lru_list) > 1:
                byItselfLRUpushed = False
            else:
                byItselfLRUpushed = True

            if len(previousLRU.dest_lru_list) > 1:
                byItselfpreviousLRU = False
            else:
                byItselfpreviousLRU = True

            return byItselfLRUpushed, LRUpushed, byItselfpreviousLRU

        ## if its not an Lru_Interconnection type
        return False, LRUpushed, False

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def blockBetweenCorners(self, PARAMS, LRU1,LRU2):
        print("...block between Corners")

        if LRU1.POSITION.row == LRU2.POSITION.row:

            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.isEmptyDict["left"] = False
            LRUblock.isEmptyDict["right"] = False

            if LRU1.POSITION.col > LRU2.POSITION.col:
                for x in range(LRU2.POSITION.col + 1,LRU1.POSITION.col):
                    PARAMS.positionMatrix[LRU1.POSITION.row][x] = LRUblock
            else:
                for x in range(LRU1.POSITION.col + 1, LRU2.POSITION.col):
                    PARAMS.positionMatrix[LRU1.POSITION.row][x] = LRUblock

        elif LRU1.POSITION.col == LRU2.POSITION.col:

            LRUblock = CC.Lru_Interconnection()
            LRUblock.source_lru = "!!BLOCKED!!"
            LRUblock.isEmptyDict["up"] = False
            LRUblock.isEmptyDict["down"] = False

            if LRU1.POSITION.row > LRU2.POSITION.row:
                for x in range(LRU2.POSITION.row + 1, LRU1.POSITION.row):
                    PARAMS.positionMatrix[x][LRU1.POSITION.col] = LRUblock

            else:
                for x in range(LRU1.POSITION.row + 1, LRU2.POSITION.row):
                    PARAMS.positionMatrix[x][LRU1.POSITION.col] = LRUblock

        else:
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawFirstLRU(self, PARAMS, LRU):
        print("...drawFirstLRU")
        PARAMS.positionMatrix[0][0] = LRU
        LRU.POSITION.row = 0
        LRU.POSITION.col = 0
        LRU.status = PARAMS.statusDict["set"]

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawLRUfromOtherPath(self, PARAMS, LRU):
        print("...drawLRUfromOtherPath")
        emptyDirection = PARAMS.directionDict["down"]

        previousLRU = CC.Lru_Interconnection()
        previousLRU.POSITION.col = copy.deepcopy(self.LRUstarting.POSITION.col)
        maxrow, maxcol = PARAMS.positionMatrix.shape
        previousLRU.POSITION.row = maxrow - 1

        self.insertRowCol(PARAMS, emptyDirection, previousLRU)
        self.placeLRUInMatrix(PARAMS, emptyDirection, previousLRU, LRU)

        LRU.POSITION.row = previousLRU.POSITION.row + 1
        LRU.POSITION.col = previousLRU.POSITION.col
        LRU.status = PARAMS.statusDict["set"]


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawLRUnGetDirection(self, PARAMS, previousLRU, LRU):
        print("...drawLRUnGetDirection")
        print("...previousLRU is", previousLRU.source_lru)
        emptyDirection, inserting = self.getEmptyDirection(PARAMS, previousLRU)
        print("...emptyDirection is", emptyDirection)

        if inserting == True:
            self.insertRowCol(PARAMS, emptyDirection, previousLRU)
            self.updateALLLRUsPositions(PARAMS)
            self.placeLRUInMatrix(PARAMS, emptyDirection, previousLRU, LRU)
            self.setLRUsPosition(PARAMS,emptyDirection, previousLRU, LRU)
        else:
            self.placeLRUInMatrix(PARAMS, emptyDirection, previousLRU, LRU)
            self.setLRUsPosition(PARAMS,emptyDirection, previousLRU, LRU)

        self.updateLRUsIsEmptyDict(PARAMS,emptyDirection, previousLRU, LRU)
        LRU.status = PARAMS.statusDict["set"]

        return emptyDirection


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawLRUwithDirection(self, PARAMS, previousLRU, LRU, emptyDirection):
        print("...drawIt with direction", emptyDirection)
        inserting = self.isInserting(PARAMS, previousLRU, emptyDirection)

        if inserting == True:
            self.insertRowCol(PARAMS, emptyDirection, previousLRU)
            self.updateALLLRUsPositions(PARAMS)
            self.placeLRUInMatrix(PARAMS, emptyDirection, previousLRU, LRU)
            self.setLRUsPosition(PARAMS,emptyDirection, previousLRU, LRU)
        else:
            self.placeLRUInMatrix(PARAMS, emptyDirection, previousLRU, LRU)
            self.setLRUsPosition(PARAMS,emptyDirection, previousLRU, LRU)

        self.updateLRUsIsEmptyDict(PARAMS,emptyDirection, previousLRU, LRU)
        LRU.status = PARAMS.statusDict["set"]

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getRandomDict_list(self, origDict):
        print("...randomize dict:", origDict)

        tempList = []

        for keys in origDict.keys():
            tempList.append(keys)

        random.shuffle(tempList)

        return tempList

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def forPrintingMatrix(self, PARAMS):
        print("...for printing only")

        rows, cols = PARAMS.positionMatrix.shape

        for row in range(0, rows):
            print("")
            for col in range(0, cols):
                LRU = PARAMS.positionMatrix[row][col]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    print("{:15s}".format(LRU.source_lru),end="")
                else:
                    print("{:15s}".format("None"),end="")

        print("")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def forPrintingData(self, PARAMS):
        print("...for printing Data only")

        rows, cols = PARAMS.positionMatrix.shape

        for row in range(0, rows):

            for col in range(0, cols):
                LRU = PARAMS.positionMatrix[row][col]
                if type(LRU) == type(CC.Lru_Interconnection()):
                    print("LRU:", LRU.source_lru," has destinations:", LRU.dest_lru_list)
                    for pin in LRU.pin_interconnections_list:
                        print("source:",pin.SOURCE.lru,"dest:",pin.DEST.lru, "|| ",end="")
                    print("")


