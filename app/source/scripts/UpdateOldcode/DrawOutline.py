import copy
import numpy
import logging
import Common as CC
import myLog

####################################################################################################################
## 
####################################################################################################################
class Draw_Outline():
    @myLog.catch_wrapper
    def __init__(self,PARAMS):
        ## properties
        self.jumpNewConnection = 1
        self.loopsA_loopsB_loopsC_renameDict = {}
        self.counter = 0
        self.couldnt_set_dict_list = []

        ## methods
        #self.draw_outline(PARAMS)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def drawOutline(self, PARAMS):
        print("...Starting drawing outline")

        print("...Printing LRUs in PARAMS.LRUInterconnectionList")
        x = 0
        for LRUs in PARAMS.LRUInterconnectionList:
            try:
                print("LRU[" + str(x) + "]\t" + LRUs.source_lru)
            except:
                print("Error: ", LRUs.source_lru , "not found?")
            x = x + 1

        print("...Starting connection: ", PARAMS.LRUSTARTINGCONNECTION.source_lru)

        #print(PARAMS.positionMatrix)

        print("...Setting position and placing in positionMatrix of", PARAMS.LRUSTARTINGCONNECTION.source_lru)
        ## Set LRU with most connection
        TEMP_POSITION = CC.Position()
        TEMP_POSITION.row = int(PARAMS.maxrow/2)
        TEMP_POSITION.col = int(PARAMS.maxcol/2)
        PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = PARAMS.LRUSTARTINGCONNECTION
        PARAMS.LRUSTARTINGCONNECTION.POSITION.col = TEMP_POSITION.col
        PARAMS.LRUSTARTINGCONNECTION.POSITION.row = TEMP_POSITION.row
        PARAMS.LRUSTARTINGCONNECTION.status = PARAMS.statusDict["set"]
        self.drawOutlineTemps(PARAMS, PARAMS.LRUSTARTINGCONNECTION, TEMP_POSITION)

        ## set loopsA, loopsB, loopsC, jump, etc
        self.setLoopsABCRename_dict(PARAMS)

        ## keep calling draw() until all LRU are set
        all_set = False
        while all_set == False:
            self.draw(PARAMS)

            print("...checking status of LRUs")
            all_set = True
            for TEMP_LRU in PARAMS.LRUInterconnectionList:
                print("...",TEMP_LRU.source_lru,"has status", TEMP_LRU.status)
                if TEMP_LRU.status == "set":
                    doing = None
                else:
                    all_set = False
                    break

        print("...printing status of each LRUs")
        for TEMP_LRU in PARAMS.LRUInterconnectionList:
            print(TEMP_LRU.source_lru, TEMP_LRU.status)

        ## delete empty ones
        PARAMS.positionMatrix = deleteUnusedRownCol(PARAMS.positionMatrix)

        ## -------------TESTING ONLY
        (x, y) = PARAMS.positionMatrix.shape
        for rows in range(0,x):
            for cols in range(0,y):
                #print(PARAMS.positionMatrix[rows][cols])
                if PARAMS.positionMatrix[rows][cols] == "block":
                    print("TEMPORARY FIX, need to fix why its still block")
                    PARAMS.positionMatrix[rows][cols] = None
                if PARAMS.positionMatrix[rows][cols] == "skipped":
                    print("TEMPORARY FIX")
                    PARAMS.positionMatrix[rows][cols] = None
        ## -------------TESTING ONLY

        #print(PARAMS.positionMatrix)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def draw(self, PARAMS):
        print("...at draw()")

        print("...Going through each path in pathList, ignore LoopCorners")
        ## go through each path in pathList (ignore LoopCorner??)
        for paths in PARAMS.pathList:
            print("...going through current path:", paths)
            temp_path_list = []
            is_skip = False

            for current_lru in paths:
                print("...currently at", current_lru, "in current path:", paths)
                if is_skip == True:
                    print("...is_skip is True, so skip for now")
                    temp_path_list.append(current_lru)

                else:
                    print("...is_skip is False")
                    is_inLoopCorner = False
                    is_inLoop1_End = False

                    TEMP_LRU = PARAMS.getLRUInterconnection(current_lru)

                    print("...match current lru from PARAMS.LRUInterconnectionList")
                    if TEMP_LRU.status == PARAMS.statusDict["set"]:
                        ## skip
                        print("...", current_lru, "has status set, dont do anything")
                    else:
                        print("...look through all path in PARAMS.pathLoopsNoDuplicateDictList")
                        for each_path in PARAMS.pathLoopsNoDuplicateDictList:
                            if current_lru in each_path['LoopCorner']:
                                print("...", current_lru, "in LoopCorner, skipping")
                                is_inLoopCorner = True
                                break

                            if current_lru in each_path['Loop1_End'] and each_path['Loop1'] != []:
                                print("...", current_lru, "In Loop1_End and Loop1 != [], skipping")
                                temp_dict = {}
                                temp_dict["Loops_at"] = each_path["Loops_at"]
                                temp_dict["Loop1_End"] = current_lru

                                temp_dict["LoopCorner_first"] = each_path["LoopCorner"][-1]
                                PARAMS.Loop1EndDictList.append(temp_dict)
                                is_inLoop1_End = True
                                break

                        if current_lru == PARAMS.LRUSTARTINGCONNECTION.source_lru:
                            ## do nothing
                            print(current_lru, "is the starting connection, dont do anything")
                        elif is_inLoopCorner == True or is_inLoop1_End == True:
                            ## if in LoopCorner, skip from here on out
                            print("...setting is_skip to True, skipping from here on out")
                            is_skip = True
                            temp_path_list.append(current_lru)

                        else:

                            if TEMP_LRU.POSITION.row == None and TEMP_LRU.POSITION.col == None:
                                print("LRU ", TEMP_LRU.source_lru,
                                      "currently has no POSITION, will assign...was probably not connected to other paths or couldn't fit before")

                                couldntset = False
                                temp_dict = {}
                                ## check if it couldnt have been set before
                                for temp_dict in self.couldnt_set_dict_list:
                                    for key, value_dict in temp_dict.items():
                                        if key == TEMP_LRU.source_lru:
                                            couldntset = True
                                            temp_dict = value_dict
                                            break
                                    if couldntset == True:
                                        break

                                if couldntset == True:
                                    print("...", TEMP_LRU.source_lru,"could NOT be drawn before, will now be drawn somewhere else.")
                                    TEMP_POSITION = CC.Position()
                                    TEMP_POSITION.row, TEMP_POSITION.col = self.setCouldntSetBefore(PARAMS, temp_dict)
                                    print("...will now be set at",TEMP_POSITION.row, TEMP_POSITION.col)
                                    PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU
                                    TEMP_LRU.POSITION.col = TEMP_POSITION.col
                                    TEMP_LRU.POSITION.row = TEMP_POSITION.row
                                    TEMP_LRU.status = PARAMS.statusDict["set"]
                                    self.drawOutlineTemps(PARAMS, TEMP_LRU, TEMP_POSITION)
                                else:
                                    print("...most likely an LRU not connected to main path")
                                    ## most likely an LRU not connected to main path
                                    TEMP_POSITION = CC.Position()
                                    TEMP_POSITION.row = self.getHighestRow(PARAMS) + self.jumpNewConnection
                                    TEMP_POSITION.col = int(PARAMS.maxcol / 2)
                                    PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU
                                    TEMP_LRU.POSITION.col = TEMP_POSITION.col
                                    TEMP_LRU.POSITION.row = TEMP_POSITION.row
                                    TEMP_LRU.status = PARAMS.statusDict["set"]
                                    self.drawOutlineTemps(PARAMS, TEMP_LRU, TEMP_POSITION)

                            else:
                                print("...Reading LRU from pathList", TEMP_LRU.source_lru, TEMP_LRU.POSITION.row,
                                      TEMP_LRU.POSITION.col, TEMP_LRU.direction)

                                self.setBlockOrUnblock(PARAMS, TEMP_LRU.POSITION, TEMP_LRU.direction, None)

                                print("At LRU: ", TEMP_LRU.source_lru, "\tPosition: ", TEMP_LRU.POSITION.row,
                                      TEMP_LRU.POSITION.col)

                                ## ----------------for loops
                                isJumping = False
                                jump = 1

                                ## end of loopA, may need to jump
                                for key, value_dict in self.loopsA_loopsB_loopsC_renameDict.items():
                                    if TEMP_LRU.source_lru == value_dict["end_loopA"]:
                                        print("...", TEMP_LRU.source_lru, "in end of loopA, may need to jump")
                                        isJumping = True
                                        jump = int(value_dict["jump"])
                                        break
                                ## ----------------

                                available_num = self.getAvailableSpaces(PARAMS, TEMP_LRU)
                                destination_num = len(TEMP_LRU.dest_lru_list)

                                print("Available space: ", available_num, "\tNumber of destination: ",
                                      destination_num - 1)

                                ## destination_num - 1, since minus the source
                                if (available_num) >= (destination_num - 1) and isJumping != True:
                                    print("Enough space, setting LRU")
                                    self.setLRUAndDrawOutlineTemps(PARAMS, TEMP_LRU)

                                else:
                                    ## need to move its position in the direction
                                    print("Not enough space, moving LRU then set or isJumping")
                                    self.moveLRUInDirection(PARAMS, TEMP_LRU, jump)
                                    self.setLRUAndDrawOutlineTemps(PARAMS, TEMP_LRU)

            if is_skip == True:
                ## append to pathSkippedList
                PARAMS.pathSkippedList.append(temp_path_list)

        self.setLoop1EndPositions(PARAMS)

        ## Then go through each path on path_loops_list skipped that are in the corners??
        self.setLoopCornerPositions(PARAMS)

        ## Then go through each path on path_loops_list skipped??
        for paths in PARAMS.pathSkippedList:
            for current_lru in paths:

                if current_lru == PARAMS.LRUSTARTINGCONNECTION.source_lru:
                    ## do nothing
                    doing = None

                else:
                    TEMP_LRU = PARAMS.getLRUInterconnection(current_lru)

                    if TEMP_LRU.status == PARAMS.statusDict["set"]:
                        ## skip
                        doing = None
                    else:
                        print("Read LRU from pathSkippedList", TEMP_LRU.source_lru, TEMP_LRU.POSITION.row,
                              TEMP_LRU.POSITION.col, TEMP_LRU.direction)

                        self.setBlockOrUnblock(PARAMS, TEMP_LRU.POSITION, TEMP_LRU.direction, None)

                        print("here", TEMP_LRU.source_lru, TEMP_LRU.POSITION.row, TEMP_LRU.POSITION.col)

                        available_num = self.getAvailableSpaces(PARAMS, TEMP_LRU)
                        destination_num = len(TEMP_LRU.dest_lru_list)

                        print(available_num, destination_num - 1)

                        ## destination_num - 1, since minus the source
                        if (available_num) >= (destination_num - 1):
                            print("Enough space, setting LRU")
                            self.setLRUAndDrawOutlineTemps(PARAMS, TEMP_LRU)

                        else:
                            ## need to move its position in the direction
                            print("Not enough space, moving LRU then set")
                            self.moveLRUInDirection(PARAMS, TEMP_LRU)
                            self.setLRUAndDrawOutlineTemps(PARAMS, TEMP_LRU)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setCouldntSetBefore(self, PARAMS, temp_dict):
        from_row = int(temp_dict["FROM_LRU_ROW"])
        from_col = int(temp_dict["FROM_LRU_COL"])
        direction = temp_dict["FROM_LRU_direction"]

        if temp_dict["direction"] == "down":
            if temp_dict["FROM_LRU_direction"] == "down":
                new_row = from_row + 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "up":
                print("Error!?")
            elif temp_dict["FROM_LRU_direction"] == "left":
                new_row = from_row
                new_col = from_col - 2
            elif temp_dict["FROM_LRU_direction"] == "right":
                new_row = from_row
                new_col = from_col + 2
            else:
                print("Error?")
        elif temp_dict["direction"] == "up":
            if temp_dict["FROM_LRU_direction"] == "down":
                print("Error!?")
            elif temp_dict["FROM_LRU_direction"] == "up":
                new_row = from_row - 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "left":
                new_row = from_row
                new_col = from_col - 2
            elif temp_dict["FROM_LRU_direction"] == "right":
                new_row = from_row
                new_col = from_col + 2
            else:
                print("Error?")
        elif temp_dict["direction"] == "left":
            if temp_dict["FROM_LRU_direction"] == "down":
                new_row = from_row + 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "up":
                new_row = from_row - 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "left":
                new_row = from_row
                new_col = from_col - 2
            elif temp_dict["FROM_LRU_direction"] == "right":
                print("Error!?")
            else:
                print("Error?")
        elif temp_dict["direction"] == "right":
            if temp_dict["FROM_LRU_direction"] == "down":
                new_row = from_row + 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "up":
                new_row = from_row - 2
                new_col = from_col
            elif temp_dict["FROM_LRU_direction"] == "left":
                print("Error!?")
            elif temp_dict["FROM_LRU_direction"] == "right":
                new_row = from_row
                new_col = from_col + 2
            else:
                print("Error?")
        else:
            print("Error?")

        row, col = self.moveUntilNone(PARAMS, new_row, new_col, direction)
        return row, col

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def moveUntilNone(self, PARAMS, new_row, new_col, direction):

        print("...moving until empty")
        if PARAMS.positionMatrix[new_row][new_col] == None:
            return new_row, new_col
        else:
            #PARAMS.positionMatrix[new_row][new_col] = "skipped"

            if direction == "down":
                new_row = new_row + 1
                row, col = self.moveUntilNone(PARAMS, new_row, new_col, direction)
            elif direction == "up":
                new_row = new_row - 1
                row, col = self.moveUntilNone(PARAMS, new_row, new_col, direction)
            elif direction == "left":
                new_col = new_col - 1
                row, col = self.moveUntilNone(PARAMS, new_row, new_col, direction)
            elif direction == "right":
                new_col = new_col + 1
                row, col = self.moveUntilNone(PARAMS, new_row, new_col, direction)
            else:
                print("Error???")

        return row, col


    ####################################################################################################################
    ##
    ####################################################################################################################
    def getHighestRow(self, PARAMS):
        print("...getting highest row")
        max = 0
        startrow = int(PARAMS.maxrow/2)
        max_row, max_col = PARAMS.positionMatrix.shape

        for row in range(startrow,max_row):
            hasElements = False
            for col in range(0,max_col):
                ## using != doesnt work sometime, not sure why
                if PARAMS.positionMatrix[row][col] == None or PARAMS.positionMatrix[row][col] == "block":
                    doing = None
                else:
                    hasElements = True
                    print(PARAMS.positionMatrix[row][col])
                    max = row
                    break

            if hasElements == False:
                break

        print("...highest row is:", max)
        return max

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setLoop1EndPositions(self, PARAMS):
        print("...Setting Loop1_End_positions")

        print("PARAMS.Loop1EndDictList:", PARAMS.Loop1EndDictList)
        for current_dict in PARAMS.Loop1EndDictList:
            print("...at current_dict:", current_dict)
            loop1_end = current_dict["Loop1_End"]

            TEMP_LRU = PARAMS.getLRUInterconnection(loop1_end)

            print("...match loop1_end:", loop1_end, "from LRU interconnection list")
            if TEMP_LRU.status != PARAMS.statusDict["set"]:
                print("Read LRU from pathList", TEMP_LRU.source_lru, TEMP_LRU.POSITION.row,
                      TEMP_LRU.POSITION.col, TEMP_LRU.direction)

                self.setBlockOrUnblock(PARAMS, TEMP_LRU.POSITION, TEMP_LRU.direction, None)

                print("At LRU: ", TEMP_LRU.source_lru, "\tPosition: ", TEMP_LRU.POSITION.row,
                      TEMP_LRU.POSITION.col)


                jump = self.getLoop1EndJumpNum(PARAMS, current_dict)

                ## need to move its position in the direction
                print("Jumping Loop1_End to a number:", jump)
                self.moveLRUInDirection(PARAMS, TEMP_LRU, jump)
                self.setLRUAndDrawOutlineTemps(PARAMS, TEMP_LRU)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getLoop1EndJumpNum(self, PARAMS, current_dict):
        print("...Getting Loop1_End_jump")
        print("loops_at_lru:", current_dict)

        direction = None
        START_POSITION = None
        END_POSITION = None
        level = None
        start = None
        end = None

        TEMP_LRU = PARAMS.getLRUInterconnection(current_dict["LoopCorner_first"])
        direction = copy.deepcopy(TEMP_LRU.direction)

        TEMP_LRU = PARAMS.getLRUInterconnection(current_dict["Loops_at"])
        START_POSITION = copy.deepcopy(TEMP_LRU.POSITION)

        TEMP_LRU = PARAMS.getLRUInterconnection(current_dict["Loop1_End"])
        END_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        _START_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        _direction = copy.deepcopy(TEMP_LRU.direction)


        print("for TOP")
        level, start, end = self.getLevelnStartnEnd(PARAMS, direction, START_POSITION, END_POSITION)
        find_max_level = self.getMaxLevelLoopCorner(PARAMS, direction, level, start, end)
        print(find_max_level)

        _END_POSITION = CC.Position()

        if _direction == PARAMS.directionDict["up"] or _direction == PARAMS.directionDict["down"]:
            _END_POSITION.col = find_max_level
            _END_POSITION.row = _START_POSITION.row
            start_loc = _START_POSITION.row
        elif _direction == PARAMS.directionDict["left"] or _direction == PARAMS.directionDict["right"]:
            _END_POSITION.row = find_max_level
            _END_POSITION.col = _START_POSITION.col
            start_loc = _START_POSITION.col
        else:
            doing = None

        print("for END")

        self.counter = 0
        level, start, end = self.getLevelnStartnEnd(PARAMS, _direction, _START_POSITION, _END_POSITION)
        find_max = self.getMaxLevelLoopCorner(PARAMS, _direction, level, start, end)
        print(find_max)


        #jump = abs(start_loc - find_max)
        jump = self.counter - 1

        print(jump, self.counter)
        return int(jump)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getLevelnStartnEnd(self, PARAMS, direction, START_POSITION, END_POSITION):

        print("...At get_level_start_end, with direction", direction)

        if direction == PARAMS.directionDict["up"] or direction == PARAMS.directionDict["down"]:
            ## decrease the row
            #level = START_POSITION.row - 1
            level = START_POSITION.row
            if START_POSITION.col < END_POSITION.col:
                start = START_POSITION.col
                end = END_POSITION.col
            else:
                end = START_POSITION.col
                start = END_POSITION.col

        elif direction == PARAMS.directionDict["left"] or direction == PARAMS.directionDict["right"]:
            ## decrease the col
            #level = START_POSITION.col - 1
            level = START_POSITION.col
            if START_POSITION.row < END_POSITION.row:
                start = START_POSITION.row
                end = END_POSITION.row
            else:
                end = START_POSITION.row
                start = END_POSITION.row


        else:
            ## should never get here
            doing = None

        return level, start, end

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getMaxLevelLoopCorner(self, PARAMS, direction, level, start, end):

        print("...At get_max_level_loopCorner, with direction", direction)

        self.counter = self.counter + 1

        isEmpty = True

        if direction == PARAMS.directionDict["up"] or direction == PARAMS.directionDict["down"]:
            print("up or down")
            for x in range(start + 1 , end):
                try: lru = PARAMS.positionMatrix[level][x].source_lru
                except: lru = PARAMS.positionMatrix[level][x]
                print(level,x, lru)
                if PARAMS.positionMatrix[level][x] == None or PARAMS.positionMatrix[level][x] == "block":
                    doing = None
                else:
                    print("not empty", PARAMS.positionMatrix[level][x].source_lru)
                    isEmpty = False
                    break

        elif direction == PARAMS.directionDict["left"] or direction == PARAMS.directionDict["right"]:
            print("left or right")
            for x in range(start + 1, end):
                try: lru = PARAMS.positionMatrix[x][level].source_lru
                except: lru = PARAMS.positionMatrix[x][level]
                print(x, level, lru)
                if PARAMS.positionMatrix[x][level] == None or PARAMS.positionMatrix[x][level] == "block":
                    doing = None
                else:
                    print("not empty", PARAMS.positionMatrix[x][level].source_lru)
                    isEmpty = False
                    break

        else:
            print("else??")
            doing = None

        if isEmpty == True:
            return level
        else:
            if direction == PARAMS.directionDict["up"]:
                ## decrease the row
                level = level - 1

            elif direction == PARAMS.directionDict["down"]:
                ## increase the row
                level = level + 1

            elif direction == PARAMS.directionDict["left"]:
                ## decrease the col
                level = level - 1

            elif direction == PARAMS.directionDict["right"]:
                ## increase the col
                level = level + 1

            else:
                ## should never get here
                doing = None

            find_max = self.getMaxLevelLoopCorner(PARAMS, direction, level, start, end)

            return find_max



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setLoopsABCRename_dict(self, PARAMS):
        print("...At set_loopsA_loopsB_loopsC_rename_dict")

        ## go through PARAMS.multipleloopsCornerLRUDict
        print("PARAMS.multipleloopsCornerLRUDict", PARAMS.multipleloopsCornerLRUDict)
        for lrukey, cornerlist in PARAMS.multipleloopsCornerLRUDict.items():
            temp_dict = {}

            for key, dict_list in PARAMS.LoopsDict.items():
                max_loopC = 0

                if key == lrukey:
                    for dict in dict_list:
                        if max_loopC < len(dict["Loops_C"]):
                            max_loopC = len(dict["Loops_C"])


                    len_loopA = len(dict["Loops_A"])

            ## loopA - 1 + jump = max(loopC) + 1
            num_jump = max_loopC + 2 - len_loopA
            if num_jump < 0:
                num_jump = 0

            temp_dict["corner"] = cornerlist
            temp_dict["len_loopA"] = len_loopA
            temp_dict["max_loopC"] = max_loopC
            temp_dict["jump"] = num_jump
            temp_dict["end_loopA"] = dict["Loops_A"][-1]

            self.loopsA_loopsB_loopsC_renameDict[lrukey] = temp_dict

        print("PARAMS.multipleloopsCornerLRUDict", PARAMS.multipleloopsCornerLRUDict)
        print("self.loopsA_loopsB_loopsC_renameDict: ", self.loopsA_loopsB_loopsC_renameDict)


    ####################################################################################################################
    ## Only do this when all dest will fit, if not move position of LRU (done before calling this)
    ####################################################################################################################
    def drawOutlineTemps(self, PARAMS, LRU, POSITION):
        print("...drawing outline temps, at LRU", LRU.source_lru)

        ## only used for the first one (starting connection lru)
        if LRU.direction == None:
            print("...LRU direction is None, First?")
            directionDict = {'up': None, 'right': None, 'down': None, 'left': None}
            ## set temps in all 4 directions (if applicable)
            ## only call when all dest can be placed adjacent to the LRU
            self.setUpDownLeftRight(PARAMS, LRU, POSITION, directionDict)

        elif LRU.direction == PARAMS.directionDict["up"]:
            print("...LRU direction is up")
            directionDict = {'up': None, 'right': None, 'left': None}
            ## only call when all dest can be placed adjacent to the LRU
            self.setUpRightLeft(PARAMS, LRU, POSITION, directionDict)

        elif LRU.direction == PARAMS.directionDict["down"]:
            print("...LRU direction is down")
            directionDict = {'right': None, 'down': None, 'left': None}
            ## only call when all dest can be placed adjacent to the LRU
            self.setRightDownLeft(PARAMS, LRU, POSITION, directionDict)

        elif LRU.direction == PARAMS.directionDict["left"]:
            print("...LRU direction is left")
            directionDict = {'up': None, 'down': None, 'left': None}
            ## only call when all dest can be placed adjacent to the LRU
            self.setUpDownLeft(PARAMS, LRU, POSITION, directionDict)

        elif LRU.direction == PARAMS.directionDict["right"]:
            print("...LRU direction is right")
            directionDict = {'up': None, 'right': None, 'down': None}
            ## only call when all dest can be placed adjacent to the LRU
            self.setUpRightDown(PARAMS, LRU, POSITION, directionDict)
        else:
            ## Error
            logging.error("Unknown LRU.direction: %s", LRU.direction)
            print("Error: Unknown LRU.direction", LRU.direction)

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def setUpDownLeftRight(self, PARAMS, LRU, POSITION, directionDict):
        print("...set_up_down_left_right")
        ## set temps in all 4 directions (if applicable)

        self.goThroughDestLruAndSet(PARAMS, LRU, POSITION, directionDict, "set_up_down_left_right")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setUpDownLeftRight2(self, PARAMS, TEMP_LRU, POSITION, key):
        print("...set_up_down_left_right2: assign LRU a position in the matrix and block its direction", TEMP_LRU.source_lru)

        TEMP_LRU.direction = key
        self.setDirectionLoops(PARAMS, TEMP_LRU)
        TEMP_POSITION = copy.deepcopy(POSITION)
        if key == PARAMS.directionDict["up"]:
            TEMP_POSITION.row = TEMP_POSITION.row - 1
        elif key == PARAMS.directionDict["down"]:
            TEMP_POSITION.row = TEMP_POSITION.row + 1
        elif key == PARAMS.directionDict["right"]:
            TEMP_POSITION.col = TEMP_POSITION.col + 1
        elif key == PARAMS.directionDict["left"]:
            TEMP_POSITION.col = TEMP_POSITION.col - 1
        else:
            ## Error
            logging.error("Unknown direction: %s", key)
            print("Error: Unknown direction", key)

        status = ""
        ## Place LRU in matrix
        print("...placing LRU in", TEMP_POSITION.row, TEMP_POSITION.col, ".This currently has:",
              PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col])
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU

            ## set LRU position
            TEMP_LRU.POSITION.row = TEMP_POSITION.row
            TEMP_LRU.POSITION.col = TEMP_POSITION.col

            ## set LRU status
            TEMP_LRU.status = PARAMS.statusDict["temp"]

            ## block that direction
            self.setBlockOrUnblock(PARAMS, TEMP_POSITION, key, "block")
            print("status is go")
            status = "go"
        else:
            ## something is there already
            print("status is nogo")
            status = "nogo"

        return status

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def setUpRightLeft(self, PARAMS, LRU, POSITION, directionDict):
        print("...set_up_right_left")
        ## set temps in all 4 directions (if applicable)

        self.goThroughDestLruAndSet(PARAMS, LRU, POSITION, directionDict, "set_up_right_left")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setUpRightLeft2(self, PARAMS, TEMP_LRU, POSITION, key):
        print("...set_up_right_left2: assign LRU a position in the matrix and block its direction", TEMP_LRU.source_lru)

        TEMP_LRU.direction = key
        self.setDirectionLoops(PARAMS, TEMP_LRU)
        TEMP_POSITION = copy.deepcopy(POSITION)
        if key == PARAMS.directionDict["up"]:
            TEMP_POSITION.row = TEMP_POSITION.row - 1
        elif key == PARAMS.directionDict["right"]:
            TEMP_POSITION.col = TEMP_POSITION.col + 1
        elif key == PARAMS.directionDict["left"]:
            TEMP_POSITION.col = TEMP_POSITION.col - 1
        else:
            ## Error
            logging.error("Unknown .direction: %s", key)
            print("Error: Unknown direction", key)

        status = ""
        ## Place LRU in matrix
        print("...placing LRU in", TEMP_POSITION.row, TEMP_POSITION.col, ".This currently has:",
              PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col])
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU

            ## set LRU position
            TEMP_LRU.POSITION.row = TEMP_POSITION.row
            TEMP_LRU.POSITION.col = TEMP_POSITION.col

            ## set LRU status
            TEMP_LRU.status = PARAMS.statusDict["temp"]

            ## block that direction
            self.setBlockOrUnblock(PARAMS, TEMP_POSITION, key, "block")
            print("status is go")
            status = "go"
        else:
            ## something is there already

            print("status is nogo")
            status = "nogo"

        return status

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def setRightDownLeft(self, PARAMS, LRU, POSITION, directionDict):
        print("...set_right_down_left")
        ## set temps in all 4 directions (if applicable)

        self.goThroughDestLruAndSet(PARAMS, LRU, POSITION, directionDict, "set_right_down_left")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setRightDownLeft2(self, PARAMS, TEMP_LRU, POSITION, key):
        print("...set_right_down_left2: assign LRU a position in the matrix and block its direction", TEMP_LRU.source_lru)

        TEMP_LRU.direction = key
        self.setDirectionLoops(PARAMS, TEMP_LRU)
        TEMP_POSITION = copy.deepcopy(POSITION)

        if key == PARAMS.directionDict["down"]:
            TEMP_POSITION.row = TEMP_POSITION.row + 1
        elif key == PARAMS.directionDict["right"]:
            TEMP_POSITION.col = TEMP_POSITION.col + 1
        elif key == PARAMS.directionDict["left"]:
            TEMP_POSITION.col = TEMP_POSITION.col - 1
        else:
            ## Error
            logging.error("Unknown .direction: %s", key)
            print("Error: Unknown direction", key)

        status = ""
        ## Place LRU in matrix
        print("...placing LRU in", TEMP_POSITION.row, TEMP_POSITION.col, ".This currently has:",
              PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col])
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU

            ## set LRU position
            TEMP_LRU.POSITION.row = TEMP_POSITION.row
            TEMP_LRU.POSITION.col = TEMP_POSITION.col

            ## set LRU status
            TEMP_LRU.status = PARAMS.statusDict["temp"]

            ## block that direction
            self.setBlockOrUnblock(PARAMS, TEMP_POSITION, key, "block")
            print("status is go")
            status = "go"
        else:
            ## something is there already
            print("status is nogo")
            status = "nogo"

        return status

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def setUpDownLeft(self, PARAMS, LRU, POSITION, directionDict):
        print("...set_up_down_left")
        ## set temps in all 4 directions (if applicable)
        self.goThroughDestLruAndSet(PARAMS, LRU, POSITION, directionDict, "set_up_down_left")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setUpDownLeft2(self, PARAMS, TEMP_LRU, POSITION, key):

        print("...set_up_down_left2: assign LRU a position in the matrix and block its direction", TEMP_LRU.source_lru)

        TEMP_LRU.direction = key
        self.setDirectionLoops(PARAMS, TEMP_LRU)
        TEMP_POSITION = copy.deepcopy(POSITION)
        if key == PARAMS.directionDict["up"]:
            TEMP_POSITION.row = TEMP_POSITION.row - 1
        elif key == PARAMS.directionDict["down"]:
            TEMP_POSITION.row = TEMP_POSITION.row + 1
        elif key == PARAMS.directionDict["left"]:
            TEMP_POSITION.col = TEMP_POSITION.col - 1
        else:
            ## Error
            logging.error("Unknown .direction: %s", key)
            print("Error: Unknown direction", key)

        status = ""
        ## Place LRU in matrix
        print("...placing LRU in", TEMP_POSITION.row, TEMP_POSITION.col, ".This currently has:",
              PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col])
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU

            ## set LRU position
            TEMP_LRU.POSITION.row = TEMP_POSITION.row
            TEMP_LRU.POSITION.col = TEMP_POSITION.col

            ## set LRU status
            TEMP_LRU.status = PARAMS.statusDict["temp"]

            ## block that direction
            self.setBlockOrUnblock(PARAMS, TEMP_POSITION, key, "block")
            print("status is go")
            status = "go"
        else:
            ## something is there already
            print("status is nogo")
            status = "nogo"

        return status

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def setUpRightDown(self, PARAMS, LRU, POSITION, directionDict):
        print("...set_up_right_down")
        ## set temps in all 4 directions (if applicable)
        self.goThroughDestLruAndSet(PARAMS, LRU, POSITION, directionDict, "set_up_right_down")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setUpRightDown2(self, PARAMS, TEMP_LRU, POSITION, key):
        print("...set_up_right_down2: assign LRU a position in the matrix and block its direction", TEMP_LRU.source_lru)

        TEMP_LRU.direction = key
        self.setDirectionLoops(PARAMS, TEMP_LRU)
        TEMP_POSITION = copy.deepcopy(POSITION)
        if key == PARAMS.directionDict["up"]:
            TEMP_POSITION.row = TEMP_POSITION.row - 1
        elif key == PARAMS.directionDict["down"]:
            TEMP_POSITION.row = TEMP_POSITION.row + 1
        elif key == PARAMS.directionDict["right"]:
            TEMP_POSITION.col = TEMP_POSITION.col + 1
        else:
            ## Error
            logging.error("Unknown .direction: %s", key)
            print("Error: Unknown direction", key)

        status = ""
        ## Place LRU in matrix
        print("...placing LRU in", TEMP_POSITION.row, TEMP_POSITION.col, ".This currently has:",
              PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col])
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU

            ## set LRU position
            TEMP_LRU.POSITION.row = TEMP_POSITION.row
            TEMP_LRU.POSITION.col = TEMP_POSITION.col

            ## set LRU status
            TEMP_LRU.status = PARAMS.statusDict["temp"]

            ## block that direction
            self.setBlockOrUnblock(PARAMS, TEMP_POSITION, key, "block")
            print("status is go")
            status = "go"
        else:
            ## something is there already
            print("status is nogo")
            status = "nogo"

        return status

    ####################################################################################################################
    ## Assumes all dest of the LRU can fit adjacent to the LRU
    ####################################################################################################################
    def goThroughDestLruAndSet(self, PARAMS, LRU, POSITION, directionDict, set_direction):
        print("...going through dest lru of the LRU", LRU.source_lru , "and set it")
        ## Do ones with directions first (ones that have direction already has higher priority)
        for dest_lru in LRU.dest_lru_list:
            print("...setting temp on", LRU.source_lru,"'s destination: ",  dest_lru)
            TEMP_LRU = PARAMS.getLRUInterconnection(dest_lru)

            if TEMP_LRU.status == PARAMS.statusDict["set"]:
                ## dont do anything
                print("...",dest_lru, "status is already set")
            elif TEMP_LRU.status == PARAMS.statusDict["temp"]:
                ## dont do anything
                print("...",dest_lru, "status is already temp")
            else:
                ## check if that LRU has direction already
                if TEMP_LRU.direction == None:
                    ## will be handled below
                    print("...",dest_lru, "has no direction.  Will set direction later")
                    break

                else:
                    ## already has direction
                    print("...",dest_lru, "already has a direction")
                    ## so that direction will not be taken by others
                    directionDict[TEMP_LRU.direction] = PARAMS.statusDict["set"]
                    print("setting direction directionDict[", TEMP_LRU.direction,"]", PARAMS.statusDict["set"])


        ## For ones with no directions yet
        for dest_lru in LRU.dest_lru_list:
            print("...",dest_lru ,"had no direction before, will be setting now")

            for TEMP_LRU in PARAMS.LRUInterconnectionList:
                ## found LRU
                if TEMP_LRU.source_lru == dest_lru:
                    if TEMP_LRU.status == PARAMS.statusDict["set"]:
                        ## dont do anything
                        print("...",dest_lru, "status is already set")
                    elif TEMP_LRU.status == PARAMS.statusDict["temp"]:
                        ## dont do anything
                        print("...",dest_lru, "status is already temp")
                    else:
                        ## check if that LRU has direction already
                        print("...",dest_lru, "has direction: ", TEMP_LRU.direction)

                        if TEMP_LRU.direction == None:
                            print("...current directionDict:", directionDict, "for", LRU.source_lru)
                            status = None
                            for key, value in directionDict.items():
                                print("... picking key:", key, "and value:", value)
                                if value == None:
                                    print("...",key, "is None.  Set direction to this key")
                                    ## set direction to that key

                                    ## if LRU is starting connection, need to see if its an end of a loop1 or loopsA
                                    ## if it is, need to block opposite direction
                                    if LRU.source_lru == PARAMS.LRUSTARTINGCONNECTION.source_lru:
                                        directionDict = self.mayBlockOppositeDirection(PARAMS, LRU, key, directionDict)

                                    if set_direction == "set_up_down_left_right":
                                        status = self.setUpDownLeftRight2(PARAMS, TEMP_LRU, POSITION, key)

                                    elif set_direction == "set_up_right_left":
                                        status = self.setUpRightLeft2(PARAMS, TEMP_LRU, POSITION, key)

                                    elif set_direction == "set_right_down_left":
                                        status = self.setRightDownLeft2(PARAMS, TEMP_LRU, POSITION, key)

                                    elif set_direction == "set_up_down_left":
                                        status = self.setUpDownLeft2(PARAMS, TEMP_LRU, POSITION, key)

                                    elif set_direction == "set_up_right_down":
                                        status = self.setUpRightDown2(PARAMS, TEMP_LRU, POSITION, key)

                                    else:
                                        ## Error
                                        logging.error("Unknown set_direction: %s", set_direction)
                                        print("Error: Unknwon set_direction", set_direction)

                                    if status == "nogo":
                                        ## go to the next one
                                        print("was nogo, try another direction")
                                        doing = None
                                    else:
                                        directionDict[key] = PARAMS.statusDict["set"]
                                        break

                            if status == "nogo":
                                print("...", TEMP_LRU.source_lru ,"was never set, will draw later")
                                key_dict = {}
                                values_dict = {}
                                values_dict["direction"] = key
                                values_dict["FROM_LRU_ROW"] = POSITION.row
                                values_dict["FROM_LRU_COL"] = POSITION.col
                                values_dict["FROM_LRU_direction"] = LRU.direction
                                key_dict[TEMP_LRU.source_lru] = values_dict
                                self.couldnt_set_dict_list.append(key_dict)
                            break

                        else:
                            ## already has direction
                            print("...Already has direction")

                            if set_direction == "set_up_down_left_right":
                                status = self.setUpDownLeftRight2(PARAMS, TEMP_LRU, POSITION, TEMP_LRU.direction)

                            elif set_direction == "set_up_right_left":
                                    status = self.setUpRightLeft2(PARAMS, TEMP_LRU, POSITION, TEMP_LRU.direction)

                            elif set_direction == "set_right_down_left":
                                status = self.setRightDownLeft2(PARAMS, TEMP_LRU, POSITION, TEMP_LRU.direction)

                            elif set_direction == "set_up_down_left":
                                status = self.setUpDownLeft2(PARAMS, TEMP_LRU, POSITION, TEMP_LRU.direction)

                            elif set_direction == "set_up_right_down":
                                status = self.setUpRightDown2(PARAMS, TEMP_LRU, POSITION, TEMP_LRU.direction)

                            else:
                                ## Error
                                logging.error("Unknown set_direction: %s", set_direction)
                                print("Error: Unknwon set_direction", set_direction)

                            if status == "nogo":
                                ## go to the next one
                                print("was nogo.  Direction it was set is no good.")
                                doing = None
                            else:
                                directionDict[TEMP_LRU.direction] = PARAMS.statusDict["set"]
                                break

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def mayBlockOppositeDirection(self, PARAMS, LRU, direction, directionDict):
        print("...may block opposite direction")
        for dict in PARAMS.pathLoopsNoDuplicateDictList:
            print("...at dict", dict)
            if dict["Loop1"] != []:
                print("...Loop1 != [], block opposite direction of", direction)
                if LRU.source_lru == dict["Loop1"][0] or LRU.source_lru == dict["Loop1"][-1]:
                    ## block opposite direction
                    if direction == PARAMS.directionDict["up"]:
                        directionDict["down"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["down"]:
                        directionDict["up"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["right"]:
                        directionDict["left"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["left"]:
                        directionDict["right"] = PARAMS.statusDict["set"]
                    else:
                        doing = None

            elif dict["Loops_A"] != []:
                print("...Loop_A != [], block opposite direction of", direction)
                if LRU.source_lru == dict["Loops_A"][0] or LRU.source_lru == dict["Loops_A"][-1]:
                    ## block opposite direction
                    if direction == PARAMS.directionDict["up"]:
                        directionDict["down"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["down"]:
                        directionDict["up"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["right"]:
                        directionDict["left"] = PARAMS.statusDict["set"]
                    elif direction == PARAMS.directionDict["left"]:
                        directionDict["right"] = PARAMS.statusDict["set"]
                    else:
                        doing = None

            else:
                print("...not updating directionDict")

        return directionDict


    ####################################################################################################################
    ## Assign directions to loops
    ## Should only be called if the LRU is getting set new direction
    ####################################################################################################################
    def setDirectionLoops(self, PARAMS, LRU):
        print("...set_direction_loops called")
        if LRU.direction == None:
            ## dont do anything, its the start LRU
            print("LRU.direction == None, dont do anything")
        else:
            new_direction = LRU.direction
            for dict in PARAMS.pathLoopsNoDuplicateDictList:
                if LRU.source_lru in dict["Loop1"]:
                    print("...", LRU.source_lru, "in dict['Loop1']")

                    for item in dict["Loop1"]:
                        LRUs = PARAMS.getLRUInterconnection(item)

                        if LRUs.direction == None:
                            print(LRUs.source_lru, "direction set to ", new_direction)
                            LRUs.direction = new_direction
                elif LRU.source_lru in dict["LoopCorner"]:
                    print("...", LRU.source_lru, "in dict['LoopCorner']")

                    for item in dict["LoopCorner"]:
                        LRUs = PARAMS.getLRUInterconnection(item)

                        if LRUs.direction == None:
                            print(LRUs.source_lru, "direction set to ", new_direction)
                            LRUs.direction = new_direction

                elif LRU.source_lru in dict["Loops_A"]:
                    print("...", LRU.source_lru, "in dict['Loops_A']")
                    print("...loop through loopA:", dict["Loops_A"])
                    for item in dict["Loops_A"]:
                        LRUs = PARAMS.getLRUInterconnection(item)

                        if LRUs.direction == None:
                            print(LRUs.source_lru, "direction set to ", new_direction)
                            LRUs.direction = new_direction

                    print("...loop through loopC:", dict["Loops_C"])
                    for item in dict["Loops_C"]:
                        LRUs = PARAMS.getLRUInterconnection(item)

                        if LRUs.direction == None:
                            LRUs.direction = LRU.getOppositeDirection(new_direction)
                            print(LRUs.source_lru, "direction set to ", LRUs.direction)

                    print("...loop through loopD:", dict["Loops_D"])
                    for item in dict["Loops_D"]:
                        LRUs = PARAMS.getLRUInterconnection(item)

                        if LRUs.direction == None:
                            LRUs.direction = LRU.getToTheRightDirection(new_direction)
                            print(LRUs.source_lru, "direction set to ", LRUs.direction)

                else:
                    ## do nothing
                    doing = None


    ####################################################################################################################
    ## set
    ####################################################################################################################
    def setBlockOrUnblock(self, PARAMS, position, direction, set_value):
        print("...setting block/unblock with direction", direction, "from position: row", position.row, "col", position.col)
        ## position is a class position

        TEST_LRU = CC.Lru_Interconnection()

        if direction == PARAMS.directionDict["up"]:
            ## block up
            for x in range(0, position.row):
                if type(PARAMS.positionMatrix[x][position.col]) == type(TEST_LRU):
                    ## do not block/unblock
                    doing = None
                else:
                    PARAMS.positionMatrix[x][position.col] = set_value

        elif direction == PARAMS.directionDict["down"]:
            ## block down
            for x in range(position.row + 1, PARAMS.maxrow):
                if type(PARAMS.positionMatrix[x][position.col]) == type(TEST_LRU):
                    ## do not block/unblock
                    doing = None
                else:
                    PARAMS.positionMatrix[x][position.col] = set_value

        elif direction == PARAMS.directionDict["left"]:
            ## block left
            for x in range(0, position.col):
                if type(PARAMS.positionMatrix[position.row][x]) == type(TEST_LRU):
                    ## do not block/unblock
                    doing = None
                else:
                    PARAMS.positionMatrix[position.row][x] = set_value

        elif direction == PARAMS.directionDict["right"]:
            ## block right
            for x in range(position.col + 1, PARAMS.maxcol):
                if type(PARAMS.positionMatrix[position.row][x]) == type(TEST_LRU):
                    ## do not block/unblock
                    doing = None
                else:
                    PARAMS.positionMatrix[position.row][x] = set_value

        else:
            ## Error
            logging.error("Unknown direction: %s", direction)
            print("Error:", direction, " unknown direction")



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getAvailableSpaces(self, PARAMS, TEMP_LRU):
        print("------Get available spaces-----")
        available_num = 0

        ## up
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        TEMP_POSITION.row = TEMP_POSITION.row - 1

        print(PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col], TEMP_POSITION.row, TEMP_POSITION.col)

        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            available_num = available_num + 1

        ## right
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        TEMP_POSITION.col = TEMP_POSITION.col + 1

        print(PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col], TEMP_POSITION.row, TEMP_POSITION.col)

        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            available_num = available_num + 1

        ## down
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        TEMP_POSITION.row = TEMP_POSITION.row + 1

        print(PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col], TEMP_POSITION.row, TEMP_POSITION.col)

        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            available_num = available_num + 1

        ## left
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        TEMP_POSITION.col = TEMP_POSITION.col - 1

        print(PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col], TEMP_POSITION.row, TEMP_POSITION.col)

        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] == None:
            available_num = available_num + 1

        print("----------------------------------")
        return available_num

    ####################################################################################################################
    ##
    ####################################################################################################################
    def setLRUAndDrawOutlineTemps(self, PARAMS, TEMP_LRU):
        print("...set lru and draw outline temps")
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)
        TEMP_LRU.status = PARAMS.statusDict["set"]
        PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = TEMP_LRU
        self.drawOutlineTemps(PARAMS, TEMP_LRU, TEMP_POSITION)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def moveLRUInDirection(self, PARAMS, TEMP_LRU, jump = 1):
        print("...moving lru in direction")
        TEMP_POSITION = copy.deepcopy(TEMP_LRU.POSITION)

        ## need to remove lru in matrix, if its set there already
        if PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] != None:
            PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = None

        #PARAMS.positionMatrix[TEMP_POSITION.row][TEMP_POSITION.col] = "skipped"

        increment = jump

        if TEMP_LRU.direction == PARAMS.directionDict["up"]:
            TEMP_POSITION.row = TEMP_POSITION.row - increment
        elif TEMP_LRU.direction == PARAMS.directionDict["right"]:
            TEMP_POSITION.col = TEMP_POSITION.col + increment
        elif TEMP_LRU.direction == PARAMS.directionDict["left"]:
            TEMP_POSITION.col = TEMP_POSITION.col - increment
        elif TEMP_LRU.direction == PARAMS.directionDict["down"]:
            TEMP_POSITION.row = TEMP_POSITION.row + increment
        else:
            ## Error
            logging.error("Unknown LRU.direction: %s", TEMP_LRU.direction)
            print("Error: Unknown LRU.direction", TEMP_LRU.direction)

        TEMP_LRU.POSITION = TEMP_POSITION

        available_num = self.getAvailableSpaces(PARAMS, TEMP_LRU)
        destination_num = len(TEMP_LRU.dest_lru_list)

        print(TEMP_LRU.source_lru, available_num, destination_num - 1)
        ## destination_num - 1, since minus the source
        if (available_num) >= (destination_num - 1):
            ## good, do nothing
            doing = None
        else:
            ## need to move its position in the direction
            self.moveLRUInDirection(PARAMS, TEMP_LRU)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setLoopCornerPositions(self, PARAMS):
        print("...setting LoopCorner positions")

        print("...go through each path in PARAMS.pathLoopsNoDuplicateDictList")
        for each_path in PARAMS.pathLoopsNoDuplicateDictList:
            print("...at path:", each_path)
            if each_path['LoopCorner'] == []:
                ## dont do anything
                doing = None
            else:
                LoopCorner_1 = each_path['LoopCorner'][0]
                LoopCorner_2 = each_path['LoopCorner'][-1]

                print("LoopCorner #1", LoopCorner_1)
                print("LoopCorner #2", LoopCorner_2)

                LRU_1 = PARAMS.getLRUInterconnection(LoopCorner_1)
                LRU_2 = PARAMS.getLRUInterconnection(LoopCorner_2)

                if LRU_1.POSITION.row == None and LRU_2.POSITION.row == None:
                    ## not set yet
                    doing = None
                else:

                    if self.isPositionGood(PARAMS, LRU_1, LRU_2) == False:
                        ## set the temp position to None
                        PARAMS.positionMatrix[LRU_1.POSITION.row][LRU_1.POSITION.col] = None
                        PARAMS.positionMatrix[LRU_2.POSITION.row][LRU_2.POSITION.col] = None
                        self.moveCornerUntilGood(PARAMS, LRU_1, LRU_2)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def isPositionGood(self, PARAMS, LRU_1, LRU_2):
        print("...is position good? For", LRU_1.source_lru, "and", LRU_2.source_lru)
        is_status = True

        if LRU_1.POSITION.col == LRU_2.POSITION.col:
            if LRU_1.POSITION.row > LRU_2.POSITION.row:
                start = LRU_2.POSITION.row
                end = LRU_1.POSITION.row
            else:
                start = LRU_1.POSITION.row
                end = LRU_2.POSITION.row

            for y in range(start + 1, end):
                if PARAMS.positionMatrix[y][LRU_1.POSITION.col] == None:
                    doing = None
                else:
                    is_status = False
                    break

        elif LRU_1.POSITION.row == LRU_2.POSITION.row:
            if LRU_1.POSITION.col > LRU_2.POSITION.col:
                start = LRU_2.POSITION.col
                end = LRU_1.POSITION.col
            else:
                start = LRU_1.POSITION.col
                end = LRU_2.POSITION.col

            for x in range(start + 1, end):
                if PARAMS.positionMatrix[LRU_1.POSITION.row][x] == None:
                    doing = None
                else:
                    is_status = False
                    break

        else:
            doing = None

        print("...is_status is", is_status)
        return is_status

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def moveCornerUntilGood(self, PARAMS, LRU_1, LRU_2):
        print("...moving corner until good")

        if LRU_1.direction == PARAMS.directionDict["up"]:
            LRU_1.POSITION.row = LRU_1.POSITION.row - 1
            LRU_2.POSITION.row = LRU_2.POSITION.row - 1

            if self.isPositionGood(PARAMS, LRU_1, LRU_2) == False:
                #PARAMS.positionMatrix[LRU_1.POSITION.row][LRU_1.POSITION.col] = "skipped"
                #PARAMS.positionMatrix[LRU_2.POSITION.row][LRU_2.POSITION.col] = "skipped"
                self.moveCornerUntilGood(PARAMS, LRU_1, LRU_2)

        elif LRU_1.direction == PARAMS.directionDict["down"]:
            LRU_1.POSITION.row = LRU_1.POSITION.row + 1
            LRU_2.POSITION.row = LRU_2.POSITION.row + 1

            if self.isPositionGood(PARAMS, LRU_1, LRU_2) == False:
                #PARAMS.positionMatrix[LRU_1.POSITION.row][LRU_1.POSITION.col] = "skipped"
                #PARAMS.positionMatrix[LRU_2.POSITION.row][LRU_2.POSITION.col] = "skipped"
                self.moveCornerUntilGood(PARAMS, LRU_1, LRU_2)

        elif LRU_1.direction == PARAMS.directionDict["left"]:
            LRU_1.POSITION.col = LRU_1.POSITION.col - 1
            LRU_2.POSITION.col = LRU_2.POSITION.col - 1

            if self.isPositionGood(PARAMS, LRU_1, LRU_2) == False:
                #PARAMS.positionMatrix[LRU_1.POSITION.row][LRU_1.POSITION.col] = "skipped"
                #PARAMS.positionMatrix[LRU_2.POSITION.row][LRU_2.POSITION.col] = "skipped"
                self.moveCornerUntilGood(PARAMS, LRU_1, LRU_2)

        elif LRU_1.direction == PARAMS.directionDict["right"]:
            LRU_1.POSITION.col = LRU_1.POSITION.col + 1
            LRU_2.POSITION.col = LRU_2.POSITION.col + 1

            if self.isPositionGood(PARAMS, LRU_1, LRU_2) == False:
                #PARAMS.positionMatrix[LRU_1.POSITION.row][LRU_1.POSITION.col] = "skipped"
                #PARAMS.positionMatrix[LRU_2.POSITION.row][LRU_2.POSITION.col] = "skipped"
                self.moveCornerUntilGood(PARAMS, LRU_1, LRU_2)

        else:
            doing = None

####################################################################################################################
## 
####################################################################################################################
@myLog.catch_wrapper
def deleteUnusedRownCol(curr_matrix):
    print("...delete unused row and col")
    isEmpty = True
    ## Check from bottom right to whenever a data is found
    while isEmpty:
        ## get current size of matrix
        max_row, max_col = curr_matrix.shape
        curr_row = max_row - 1
        curr_col = max_col - 1

        ## look through all columns
        for cols in range(0, max_col):
            if curr_matrix[curr_row][cols] != None:
                isEmpty = False
                break

        if isEmpty == True:
            ## look through all rows
            for rows in range(0, max_row):
                if curr_matrix[rows][curr_col] != None:
                    isEmpty = False
                    break

        if isEmpty == True:
            ## row/col is the same number, since its a square matrix
            curr_matrix = deleteRownCol(curr_matrix, curr_row, curr_col)

    isEmpty = True
    ## Check from top left to whenever a data is found
    while isEmpty:
        ## get current size of matrix
        max_row, max_col = curr_matrix.shape
        curr_row = 0
        curr_col = 0

        ## look through all columns
        for cols in range(0, max_col):
            if curr_matrix[curr_row][cols] != None:
                isEmpty = False
                break

        if isEmpty == True:
            ## look through all rows
            for rows in range(0, max_row):

                if curr_matrix[rows][curr_col] != None:
                    isEmpty = False
                    break

        if isEmpty == True:
            ## row/col is the same number, since its a square matrix
            curr_matrix = deleteRownCol(curr_matrix, curr_row, curr_col)

    curr_matrix = deleteUnusedCol(curr_matrix)
    curr_matrix = deleteUnusedRowOnTop(curr_matrix)
    curr_matrix = deleteUnusedRowOnBottom(curr_matrix)

    return curr_matrix

####################################################################################################################
## 
####################################################################################################################
@myLog.catch_wrapper
def deleteUnusedCol(curr_matrix):
    print("...delete unused col")
    ## Clear all unused columns on the left
    isEmpty = True
    while isEmpty:
        ## get current size of matrix
        max_row, max_col = curr_matrix.shape

        curr_col = 0

        ## look through all rows in current col
        for rows in range(0, max_row):
            if curr_matrix[rows][curr_col] != None:
                isEmpty = False
                break

        if isEmpty == True:
            ## row/col is the same number, since its a square matrix
            curr_matrix = deleteCol(curr_matrix, curr_col)

    return curr_matrix


####################################################################################################################
## 
####################################################################################################################
@myLog.catch_wrapper
def deleteUnusedRowOnTop(curr_matrix):
    print("...delete unused row from top")
    ## Clear all unused rows on the top
    isEmpty = True
    while isEmpty:
        ## get current size of matrix
        max_row, max_col = curr_matrix.shape

        curr_row = 0

        ## look through all cols in current row
        for cols in range(0, max_col):
            if curr_matrix[curr_row][cols] != None:
                isEmpty = False
                break

        if isEmpty == True:
            ## row/col is the same number, since its a square matrix
            curr_matrix = deleteRow(curr_matrix, curr_row)

    return curr_matrix

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def deleteUnusedRowOnBottom(curr_matrix):
    print("...delete unused row from bottom")
    ## Clear all unused rows on the bottom
    isEmpty = True
    while isEmpty:
        ## get current size of matrix
        max_row, max_col = curr_matrix.shape

        curr_row = max_row - 1

        ## look through all cols in current row
        for cols in range(0, max_col):
            if curr_matrix[curr_row][cols] != None:
                isEmpty = False
                break

        if isEmpty == True:
            ## row/col is the same number, since its a square matrix
            curr_matrix = deleteRow(curr_matrix, curr_row)

    return curr_matrix



####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def deleteRow(matrix, row):
    #print("...deleting row", row)
    ## delete row
    matrix = numpy.delete(matrix, (row), axis=0)

    return matrix


####################################################################################################################
## 
####################################################################################################################
@myLog.catch_wrapper
def deleteCol(matrix, col):
    #print("...deleting col", col)
    ## delete col
    matrix = numpy.delete(matrix, (col), axis=1)

    return matrix

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def deleteRownCol(matrix, row, col):
    #print("...deleting row", row ,"and col", col)
    ## delete row
    matrix = numpy.delete(matrix,(row), axis=0)
    ## elete col
    matrix = numpy.delete(matrix, (col), axis=1)

    return matrix