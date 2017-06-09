import copy
import math
import logging
import Common as CC
from lxml import etree
import myLog

####################################################################################################################
## 
####################################################################################################################
class Prep_Outline():
    @myLog.catch_wrapper
    def __init__(self,PARAMS,settings):
        ## properties
        self.settings = settings
        self.format_duplicating_LRU = '02d'
        self.counter_test = 0

        ## methods
        #self.prep_outline(PARAMS)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def prep_outline(self, PARAMS):
        print("...Preping Outline")

        self.setLRUInterconnections(PARAMS)
        self.copyConnectionsFromSource(PARAMS)

        print("\n-----------------Updating LRU with connections over 4-----------------\n")
        if self.settings["GridView"]["duplicateLRU"] == "True":
            self.updateLRUConnectionsOver4(PARAMS)

        print("...Printing PARAMS.LRUInterconnectionList:")
        ## For testing print out only
        for LRU in PARAMS.LRUInterconnectionList:
            print("-----------------", LRU.source_lru)
            for dest in LRU.dest_lru_list:
                print("dest", dest)
            for PINS in LRU.pin_interconnections_list:
                print("pins source:", PINS.SOURCE.lru, PINS.SOURCE.conn, PINS.SOURCE.pin, "\t dest:", PINS.DEST.lru,
                      PINS.DEST.conn, PINS.DEST.pin)

        ## get LRU with most connections
        self.setMostConnections(PARAMS)
        found_new = True
        self.setMostConnectionsCannotBeInLoop(PARAMS, found_new)

    ####################################################################################################################
    ## generate LRUInterconnectionList
    ####################################################################################################################
    def setLRUInterconnections(self, PARAMS):
        print("...setting LRU_interconnections")

        print("...removing duplicates in pinInterconnectionList (if any)")
        ## need to remove duplicates
        unique_pin_list = []
        pin_string_list = []
        for PIN in PARAMS.pinInterconnectionList:
            source_string = PIN.SOURCE.lru + "_" + PIN.SOURCE.conn + "_" + PIN.SOURCE.pin
            dest_string = PIN.DEST.lru + "_" + PIN.DEST.conn + "_" + PIN.DEST.pin
            pin_string = source_string + "_" + dest_string

            if pin_string in pin_string_list:
                doing = None
            else:
                pin_string_list.append(pin_string)
                unique_pin_list.append(PIN)
        ## set to unique ones only
        PARAMS.pinInterconnectionList = unique_pin_list

        print("...Printing updated PARAMS.pinInterconnectionList")
        for PIN in PARAMS.pinInterconnectionList:
            print("source", PIN.SOURCE.lru,PIN.SOURCE.conn,PIN.SOURCE.pin,"dest", PIN.DEST.lru,PIN.DEST.conn,PIN.DEST.pin)

        print("...Gathering unique LRUs from PARAMS.pinInterconnectionList")
        unique_LRUs = []
        for PINS in PARAMS.pinInterconnectionList:
            if PINS.SOURCE.lru in unique_LRUs:
                ## in unique_LRUs already
                doing = None
            else:
                ## not in unique_LRUs, add
                unique_LRUs.append(PINS.SOURCE.lru)

        print("unique_LRUs", unique_LRUs)

        print("...Generating PARAMS.LRUInterconnectionList from unique_LRUs")
        for lrus in unique_LRUs:
            temp_LRU_interconnection = CC.Lru_Interconnection()
            temp_LRU_interconnection.setSourceLru(lrus)

            temp_dest_lrus_list = []

            ## gather all PINS regarding this LRU
            for PINS in PARAMS.pinInterconnectionList:
                if PINS.SOURCE.lru == lrus:
                    temp_LRU_interconnection.addPinInterconnectionsList(PINS)

                    if PINS.DEST.lru in temp_dest_lrus_list:
                        ## dont add
                        doing = None
                    else:
                        ## add dest LRU
                        temp_dest_lrus_list.append(PINS.DEST.lru)
                        temp_LRU_interconnection.addDestLruList(PINS.DEST.lru)
            print("...appending ", temp_LRU_interconnection.source_lru,temp_LRU_interconnection.dest_lru_list,"to PARAMS.LRUInterconnectionList")
            PARAMS.LRUInterconnectionList.append(temp_LRU_interconnection)

    ####################################################################################################################
    ## Since only source connection has description/signal type in pinInterconnectionList of an LRU
    ####################################################################################################################
    def copyConnectionsFromSource(self, PARAMS):
        print("...copying connection data from SOURCE, current description/signals of DEST may currently be incomplete ")
        for LRU in PARAMS.LRUInterconnectionList:
            for PIN in LRU.pin_interconnections_list:
                #####pin to be updated (pin.DEST)
                find = PIN.DEST.getString()

                for PIN2 in PARAMS.pinInterconnectionList:
                    if PIN2.SOURCE.getString() == find:
                        #####set the pin.DEST to PIN2.SOURCE (more complete)
                        PIN.DEST = PIN2.SOURCE


    ####################################################################################################################
    ## If over 4, need to update dest_lru_list, pinInterconnectionList, connection.LRU (not label)
    ####################################################################################################################
    def updateLRUConnectionsOver4(self, PARAMS):

        print("...Updating LRU with connections over 4")

        for OLD_LRU in PARAMS.LRUInterconnectionList:
            ORIG_LRU = copy.deepcopy(OLD_LRU)
            num_connections = len(OLD_LRU.dest_lru_list)
            print("...LRU:", OLD_LRU.source_lru, "has", num_connections, "connections")
            max_num_connections = int(self.settings["GridView2"]["max_num_connections"])
            max_duplicates_connection = max_num_connections - 2
            if num_connections > max_num_connections:
                print("Need to update this list: ", OLD_LRU.dest_lru_list)
                new_num_LRU = num_connections / max_duplicates_connection
                ## round up
                num_LRUs = math.ceil(new_num_LRU)

                ## create a list of LRU_interconnections (for new LRU name)
                temp_lru_interconnection_list = []
                for y in range(0, num_LRUs):
                    temp_lru_interconnection = copy.deepcopy(OLD_LRU)
                    temp_lru_interconnection_list.append(temp_lru_interconnection)

                ## will now have num_LRUs of the LRU.
                ## Update each dest_lru_list
                for x in range(0, num_LRUs):
                    temp_dest_list = []
                    temp_lru_interconnection_list[x].source_lru = OLD_LRU.source_lru + PARAMS.delimeterDuplicatingLRU + str(format(x, self.format_duplicating_LRU))
                    ## each new_LRU will have different parts of the list, divisible by 2
                    temp_dest_list = OLD_LRU.dest_lru_list[(x * max_duplicates_connection):(x * max_duplicates_connection + max_duplicates_connection)]
                    ## set dest_lru_list to blank
                    temp_lru_interconnection_list[x].dest_lru_list = []
                    ## assign to temp_dest_list
                    temp_lru_interconnection_list[x].dest_lru_list = temp_dest_list

                    ## Update pin interconnection list (remove dest source not in dest_lru_list)
                    ## use reverse since removing items could cause loop not to finish all the way
                    for item in reversed(temp_lru_interconnection_list[x].pin_interconnections_list):
                        if item.DEST.lru in temp_lru_interconnection_list[x].dest_lru_list:
                            ## in dest_lru_list, dont do anything
                            doing = None
                        else:
                            ## not in new dest_lru_list, remove
                            temp_lru_interconnection_list[x].pin_interconnections_list.remove(item)


                    ## Update pin interconnection list (change source LRU name)
                    for item in temp_lru_interconnection_list[x].pin_interconnections_list:
                        ## set connection.lru to new LRU name
                        item.SOURCE.lru = temp_lru_interconnection_list[x].source_lru

                self.addConnectionsBetweenNewLRU(PARAMS, num_LRUs, temp_lru_interconnection_list, OLD_LRU)

                ## append this for future use
                PARAMS.lrusExpandedList.append(ORIG_LRU)

                ## delete LRU from LRUInterconnectionList
                PARAMS.LRUInterconnectionList.remove(OLD_LRU)

            else:
                print("...No updating required")

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def addConnectionsBetweenNewLRU(self, PARAMS, num_LRUs, temp_lru_interconnection_list, OLD_LRU):

        print("...Adding connections between new LRUs")
        conn_text = ""
        pin_text = ""
        type_text = "same"

        ## add connection between new LRUs (dest and pins)
        for z in range(0, num_LRUs):
            if z == 0:
                ## First elem, add second elem as dest lru
                temp_lru_interconnection_list[z].addDestLruList(
                    temp_lru_interconnection_list[z + 1].source_lru)

                TEMP_PIN = CC.Pin_Interconnection()
                TEMP_PIN.SOURCE.lru = temp_lru_interconnection_list[z].source_lru
                TEMP_PIN.SOURCE.lru_label = OLD_LRU.pin_interconnections_list[0].SOURCE.lru_label
                TEMP_PIN.SOURCE.conn = conn_text
                TEMP_PIN.SOURCE.pin = pin_text
                TEMP_PIN.SOURCE.type = type_text
                TEMP_PIN.SOURCE.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                TEMP_PIN.DEST.lru = temp_lru_interconnection_list[z + 1].source_lru
                TEMP_PIN.DEST.conn = conn_text
                TEMP_PIN.DEST.pin = pin_text
                TEMP_PIN.DEST.type = type_text
                TEMP_PIN.DEST.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                temp_lru_interconnection_list[z].pin_interconnections_list.append(TEMP_PIN)

            elif z == num_LRUs - 1:
                ## last elem, add second to the last elem as dest lru
                temp_lru_interconnection_list[z].addDestLruList(
                    temp_lru_interconnection_list[z - 1].source_lru)

                TEMP_PIN = CC.Pin_Interconnection()
                TEMP_PIN.SOURCE.lru = temp_lru_interconnection_list[z].source_lru
                TEMP_PIN.SOURCE.lru_label = OLD_LRU.pin_interconnections_list[0].SOURCE.lru_label
                TEMP_PIN.SOURCE.conn = conn_text
                TEMP_PIN.SOURCE.pin = pin_text
                TEMP_PIN.SOURCE.type = type_text
                TEMP_PIN.SOURCE.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                TEMP_PIN.DEST.lru = temp_lru_interconnection_list[z - 1].source_lru
                TEMP_PIN.DEST.conn = conn_text
                TEMP_PIN.DEST.pin = pin_text
                TEMP_PIN.DEST.type = type_text
                TEMP_PIN.DEST.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                temp_lru_interconnection_list[z].pin_interconnections_list.append(TEMP_PIN)

            else:
                ## in the middle, add elems before and after
                temp_lru_interconnection_list[z].addDestLruList(
                    temp_lru_interconnection_list[z - 1].source_lru)
                temp_lru_interconnection_list[z].addDestLruList(
                    temp_lru_interconnection_list[z + 1].source_lru)

                TEMP_PIN = CC.Pin_Interconnection()
                TEMP_PIN.SOURCE.lru = temp_lru_interconnection_list[z].source_lru
                TEMP_PIN.SOURCE.lru_label = OLD_LRU.pin_interconnections_list[0].SOURCE.lru_label
                TEMP_PIN.SOURCE.conn = conn_text
                TEMP_PIN.SOURCE.pin = pin_text
                TEMP_PIN.SOURCE.type = type_text
                TEMP_PIN.SOURCE.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                TEMP_PIN.DEST.lru = temp_lru_interconnection_list[z + 1].source_lru
                TEMP_PIN.DEST.conn = conn_text
                TEMP_PIN.DEST.pin = pin_text
                TEMP_PIN.DEST.type = type_text
                TEMP_PIN.DEST.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                temp_lru_interconnection_list[z].pin_interconnections_list.append(TEMP_PIN)

                TEMP_PIN = CC.Pin_Interconnection()
                TEMP_PIN.SOURCE.lru = temp_lru_interconnection_list[z].source_lru
                TEMP_PIN.SOURCE.lru_label = OLD_LRU.pin_interconnections_list[0].SOURCE.lru_label
                TEMP_PIN.SOURCE.conn = conn_text
                TEMP_PIN.SOURCE.pin = pin_text
                TEMP_PIN.SOURCE.type = type_text
                TEMP_PIN.SOURCE.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                TEMP_PIN.DEST.lru = temp_lru_interconnection_list[z - 1].source_lru
                TEMP_PIN.DEST.conn = conn_text
                TEMP_PIN.DEST.pin = pin_text
                TEMP_PIN.DEST.type = type_text
                TEMP_PIN.DEST.lruType = temp_lru_interconnection_list[z].pin_interconnections_list[0].SOURCE.lruType
                temp_lru_interconnection_list[z].pin_interconnections_list.append(TEMP_PIN)

            print(temp_lru_interconnection_list[z].source_lru, "has connections: ",
                  temp_lru_interconnection_list[z].dest_lru_list)


        ## append each of the temp_interconnection in the list
        for new_LRU_interconnection in temp_lru_interconnection_list:
            ## update lryType to add "SAME" in it
            new_LRU_interconnection.pin_interconnections_list[0].SOURCE.lruType = new_LRU_interconnection.pin_interconnections_list[0].SOURCE.lruType + "SAME"
            PARAMS.LRUInterconnectionList.append(new_LRU_interconnection)

            ## update LRUs connecting to old LRU to now connect to new LRU
            for dest in new_LRU_interconnection.dest_lru_list:
                for LRU_INTER in PARAMS.LRUInterconnectionList:
                    if LRU_INTER.source_lru == dest:
                        ## need to update dest_lru_list
                        for destination in LRU_INTER.dest_lru_list:
                            ## update dest from OLD_LRU to new_LRU
                            if destination == OLD_LRU.source_lru:
                                ## updating the destination here doesnt update the list
                                ## so remove from list and add new one

                                ## remove
                                LRU_INTER.dest_lru_list.remove(destination)

                                destination = new_LRU_interconnection.source_lru
                                ## add
                                LRU_INTER.dest_lru_list.append(destination)

                        ## need to update pin_interconnections_list
                        for PINS in LRU_INTER.pin_interconnections_list:
                            ## update pin_interconnection dest LRU from OLD_LRU to new_LRU
                            if PINS.DEST.lru == OLD_LRU.source_lru:
                                PINS.DEST.lru = new_LRU_interconnection.source_lru

    ####################################################################################################################
    ## set LRUSTARTINGCONNECTION and startingLruPickedList to LRU with most connections
    ####################################################################################################################
    def setMostConnections(self, PARAMS):

        print("...Setting most connections")
        max = 0
        for LRU in PARAMS.LRUInterconnectionList:
            if len(LRU.dest_lru_list) > max:
                max = len(LRU.dest_lru_list)
                PARAMS.LRUSTARTINGCONNECTION = LRU

        print("...Starting LRU will be", PARAMS.LRUSTARTINGCONNECTION.source_lru)
        PARAMS.startingLruPickedList.append(PARAMS.LRUSTARTINGCONNECTION.source_lru)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setMostConnectionsCannotBeInLoop(self, PARAMS, found_new):

        print("...Making sure most connections is not in a loop")

        temp_list = []
        temp_list.append(PARAMS.LRUSTARTINGCONNECTION.source_lru)
        PARAMS.pathList = []
        self.getPaths(PARAMS, temp_list, PARAMS.LRUSTARTINGCONNECTION, PARAMS.LRUSTARTINGCONNECTION)

        ## get other paths if any
        unique_LRUs = self.getOtherPaths(PARAMS)

        if self.settings["GridView"]["minimum_path_only"] == "True":
            self.getMinimumPaths(PARAMS, unique_LRUs)

        self.categorizePaths(PARAMS)

        self.reorganizePaths(PARAMS)

        self.getPathLoops(PARAMS)
        self.getPathLoopsNoDuplicate(PARAMS)

        self.getPathLoopsNoDuplicateDictList(PARAMS)


        self.verifyPathListDicts(PARAMS)

        if found_new == True:
            ## check if its in the loop
            for paths_dict in PARAMS.pathLoopsNoDuplicateDictList:
                for lru in paths_dict["Loop1"]:
                    if PARAMS.LRUSTARTINGCONNECTION.source_lru == lru:
                        foundnew = self.setNewStartingConnection(PARAMS)

                        if foundnew == False:
                            ## only reach here if didnt find anything outside the loop
                            ## will get the most connections
                            self.setMostConnections(PARAMS)

                        self.setMostConnectionsCannotBeInLoop(PARAMS, foundnew)
        else:
            ## only reach here if didnt find anything outside the loop
            ## will get the most connections
            doing = None

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def reorganizePaths(self, PARAMS):
        print("...reorganizing paths by length")

        temp_dict = {}

        for paths in PARAMS.pathList:

            length = len(paths)
            print(paths, length)
            try:
                ## dictionary for it already exist
                testing = temp_dict[length]
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

        #PARAMS.pathList = new_path_list


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def categorizePaths(self, PARAMS):
        print("...categorizing paths")

        # paths_tree = etree.Element('paths')
        ## generate a sub element with tag paths and attribute name
        # child = etree.SubElement(paths_tree, 'paths', name=str(first_elems))

        PATH_TREE = self.getTreePaths(PARAMS.pathList, 2)

        self.forPrintingONLY(PATH_TREE)

        print("DONE", self.counter_test)

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def forPrintingONLY(self, PATH_TREE):

        for BRANCH in PATH_TREE.branches_list:
            if len(BRANCH.paths_list) == 2 or len(BRANCH.paths_list) == 1:
            #if BRANCH.branch_tree.branches_list == [] or (len(BRANCH.branch_tree.branches_list) == 1):
                print("prefix", BRANCH.prefix, "pathList", BRANCH.paths_list)
                self.counter_test = self.counter_test + 1
            else:
                self.forPrintingONLY(BRANCH.branch_tree)

        # for BRANCH in PATH_TREE.branches_list:
        #     print("prefix", BRANCH.prefix, "pathList", BRANCH.paths_list)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getTreePaths(self, pathList, num):
        first_elems_list = []
        PATH_TREE = CC.Pathtree()

        if len(pathList) == 1:
            ## only 1 path
            doing = None
        else:
            for paths in pathList:
                first_elems = paths[:num]
                if first_elems in first_elems_list:
                    ## already taken into account
                    doing = None
                else:
                    first_elems_list.append(first_elems)
                    PATH_BRANCH = CC.Pathbranch()
                    PATH_BRANCH.prefix = first_elems
                    PATH_TREE.branches_list.append(PATH_BRANCH)

                for BRANCH in PATH_TREE.branches_list:
                    if BRANCH.prefix == first_elems:
                        BRANCH.paths_list.append(paths)



            for BRANCH in PATH_TREE.branches_list:
                num2 = num + 1
                BRANCH.branch_tree = self.getTreePaths(BRANCH.paths_list, num2)

        return PATH_TREE





    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getMinimumPaths(self, PARAMS, unique_LRUs):
        ## This cause multiple loops to NOT work.  Investigate later
        print("...Getting minimum path, only paths that have new LRUs")
        new_path_list = []
        covered_lru_list = []
        for path in PARAMS.pathList:
            new_path = False
            for LRU in path:
                if LRU in covered_lru_list:
                    ## already in the covered_lru_list
                    doing = None
                else:
                    new_path = True
                    covered_lru_list.append(LRU)
            if new_path == True:
                new_path_list.append(path)

            if len(set(covered_lru_list)) == len(set(unique_LRUs)):
                print("...Covered all LRUs from self.unique_LRUs")
                break

        print("Final updated paths (", len(new_path_list), ") items")
        PARAMS.pathList = new_path_list
        for path in PARAMS.pathList:
            print("paths:", path)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getOtherPaths(self, PARAMS):
        print("Previous paths:")
        for path in PARAMS.pathList:
            print("paths:", path)

        print(
            "...Need to get other paths not included in the previous paths gathered (if any).  For connections not connected from before.")
        ## need to get other paths not included in the previous get_paths
        unique_LRUs = []
        for LRUS in PARAMS.LRUInterconnectionList:
            temp_unique_lru = []
            unique_LRUs.append(LRUS)
            for pathList in PARAMS.pathList:
                for item in pathList:
                    temp_unique_lru.append(item)

            ## remove duplicates
            temp_unique_lru = set(temp_unique_lru)

            if LRUS.source_lru not in temp_unique_lru:
                print("...other paths found.")
                self.getOtherPaths2(PARAMS, PARAMS.pathList, LRUS, LRUS)
            else:
                print("...No other paths found")

        unique_LRUs = set(unique_LRUs)

        print("Updated paths with other paths, if any.  Total (", len(PARAMS.pathList), ") items:")
        for path in PARAMS.pathList:
            print("paths:", path)

        return unique_LRUs

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getOtherPaths2(self, PARAMS, pathList, LRU, from_LRU):
        ## LRU is initially the LRU with most connections

        print("...Getting other paths")

        ##  FOR ADAPTERS
        ##  ADDING A PATH FOR ADAPTER, NOT WORKING AT THE MOMENT
        # if LRU.pin_interconnections_list[0].SOURCE.lruType == "ADAPTER":
        #     temp_list = [LRU.source_lru]
        #     temp_list.extend(LRU.dest_lru_list)
        #     PARAMS.pathList.append(temp_list)
        #     return

        dest_len = len(LRU.dest_lru_list)

        for lru_dest in LRU.dest_lru_list:
            print(lru_dest)
            if lru_dest == None:
                ## Error
                logging.error("LRU_dest = None for %s", LRU.source_lru)
                print("Error: LRU_dest = None")

            temp_list = []
            #LRU_INTERCONN = PARAMS.getLRUInterconnection(lru_dest)
            for LRU_INTERCONN in PARAMS.LRUInterconnectionList:
                if lru_dest == LRU_INTERCONN.source_lru:
                    if LRU_INTERCONN.source_lru in pathList:
                        if LRU_INTERCONN.source_lru == from_LRU.source_lru:
                            ## just connecting back to orig_LRU
                            if dest_len == 1:
                                ## append to self.pathList
                                PARAMS.pathList.append(temp_list)
                        else:
                            ## loopback
                            temp_list.append(lru_dest)
                            ## append to self.pathList
                            PARAMS.pathList.append(temp_list)
                    else:
                        temp_list.append(lru_dest)
                        self.getPaths(PARAMS, temp_list, LRU_INTERCONN, LRU)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getPaths(self, PARAMS, pathList, LRU, from_LRU):
        ## LRU is initially the LRU with most connections

        print("...Getting paths")

        dest_len =  len(LRU.dest_lru_list)

        for lru_dest in LRU.dest_lru_list:
            if lru_dest == None:
                ## Error
                logging.error("LRU_dest = None for %s", LRU.source_lru)
                print("Error: LRU_dest = None")

            temp_list = copy.deepcopy(pathList)

            #LRU_INTERCONN = PARAMS.getLRUInterconnection(lru_dest)
            for LRU_INTERCONN in PARAMS.LRUInterconnectionList:
                if lru_dest == LRU_INTERCONN.source_lru:
                    if LRU_INTERCONN.source_lru in pathList:
                        if LRU_INTERCONN.source_lru == from_LRU.source_lru:
                            ## just connecting back to orig_LRU
                            if dest_len == 1:
                                ## append to self.pathList
                                PARAMS.pathList.append(temp_list)
                        else:
                            ## loopback
                            temp_list.append(lru_dest)
                            ## append to self.pathList
                            PARAMS.pathList.append(temp_list)
                    else:
                        temp_list.append(lru_dest)
                        self.getPaths(PARAMS, temp_list, LRU_INTERCONN, LRU)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getPathLoops(self, PARAMS):
        print("...Getting path_loops")

        ## Look through all the paths, see which on has duplicates, meaning loopbacks
        PARAMS.pathLoopsList = []

        for paths in PARAMS.pathList:
            ## Check if there are duplicates
            if len(paths) != len(set(paths)):
                ## has duplicates, is a loop
                PARAMS.pathLoopsList.append(paths)

        for path_loops in PARAMS.pathLoopsList:
            print("loop paths:", path_loops)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getPathLoopsNoDuplicate(self, PARAMS):

        print("...Getting path_loops_no_duplicate")

        PARAMS.path_list_loops_no_duplicate = []

        print("...pathLoopsList has", len(PARAMS.pathLoopsList) ,"path_loops. Iterating...")
        if self.settings["GridView"]["delete_path_list_loops_no_duplicate"] == "True":
            ## need to be for complex ones?? for now
            print("...setting PARAMS.path_list_loops_no_duplicate = []")
            PARAMS.path_list_loops_no_duplicate = []
        else:
            for paths in PARAMS.pathLoopsList:
                if (paths in PARAMS.path_list_loops_no_duplicate) or (paths in PARAMS.pathLoopsRemovedList):
                    ## dont do anything
                    print(paths, "already taken into account before (either removed or added to no duplicate")
                else:
                    PARAMS.path_list_loops_no_duplicate.append(paths)
                    for paths2 in PARAMS.pathLoopsList:
                        if paths == paths2:
                            ## ignore
                            doing = None
                        elif set(paths) == set(paths2):
                            ## compare (ignore order)
                            PARAMS.pathLoopsRemovedList.append(paths2)
                            #PARAMS.path_list_loops_no_duplicate.append(paths)


        print("...Printing PARAMS.path_list_loops_no_duplicate (", len(PARAMS.path_list_loops_no_duplicate) ,") items")
        for path_list_loops in PARAMS.path_list_loops_no_duplicate:
            print("loop no duplicate paths:", path_list_loops)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getPathLoopsNoDuplicateDictList(self, PARAMS):
        print("...Getting pathLoopsNoDuplicateDictList")
        PARAMS.pathLoopsNoDuplicateDictList = []

        for paths in PARAMS.path_list_loops_no_duplicate:

            length = len(paths)

            ## Get last item, since thats what loops
            loop_item = paths[-1]

            ## find where loop_item first occurs
            loop_item_index = 0
            for lru_string in paths:
                if lru_string == loop_item:
                    ## found first instance of loop item
                    break
                loop_item_index = loop_item_index + 1

            ####starts where loop item is
            Loop1 = []
            for x in range(loop_item_index, length - 3):
                Loop1.append(paths[x])

            """
            Example path:   ['MCS', '1W2', 'VCDM', '1W3', 'DSP', '1W1', 'BATT', '1W2']
            Loop1:          ['1W2', 'VCDM', '1W3', 'DSP']
            LoopCorner:     ['1W1', 'BATT']

            Drawing:              BATT               1W1
                            MCS   1W2   VCDM   1W3   DSP
            """

            LoopCorner = []
            for x in range(length - 3, length - 1):
                LoopCorner.append(paths[x])


            Loop1_End = Loop1[-1]

            ## For multiple loops, will be assigned later
            """
            Path example: X0, A, B, Y0, Y1, C, D, E, X1

            Drawing:      X0, A, B,    Y0
                          X1, E, D, C, Y1

            Loops_A:      X0, A, B, Y0
            Loops_B:      X1, E, D, C, Y1
            Loops_C:      E, D, C
            Loops_D:      X1, Y1
            """
            Loops_A = []
            Loops_B = []
            Loops_C = []
            Loops_D = []
            Loops_at = None

            temp_dict = {"Paths": paths, "Loop1": Loop1, "Loop1_End":Loop1_End, "LoopCorner": LoopCorner, "Loops_A":Loops_A, "Loops_B":Loops_B, "Loops_C":Loops_C,"Loops_D":Loops_D, "Loops_at":Loop1[0]}
            PARAMS.pathLoopsNoDuplicateDictList.append(temp_dict)

        for items in PARAMS.pathLoopsNoDuplicateDictList:
            print("PARAMS.pathLoopsNoDuplicateDictList: ", items)

    ####################################################################################################################
    ## Returns false if all LRU has already been picked before
    ####################################################################################################################
    def setNewStartingConnection(self, PARAMS):
        print("...Setting another starting connection/LRU")
        PARAMS.LRUSTARTINGCONNECTION = None

        found_new_one = False

        for LRU in PARAMS.LRUInterconnectionList:
            if LRU.source_lru in PARAMS.startingLruPickedList:
                ## pick another one, was already picked before
                doing = None
            else:
                PARAMS.LRUSTARTINGCONNECTION = LRU
                found_new_one = True
                break

        if found_new_one == True:
            PARAMS.startingLruPickedList.append(PARAMS.LRUSTARTINGCONNECTION.source_lru)

        return found_new_one


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setEndpointLoc(self, PARAMS):
        print("...Setting endpoint_loc")

        ## Go through each LRU in the list
        for LRUs in PARAMS.LRUInterconnectionList:

            ## SKIPPING ADAPTER??
            if LRUs.pin_interconnections_list[0].SOURCE.lruType == "ADAPTER":
                continue

            dest_dict = {}
            ## create a dict, its keys will be dest lrus
            for dest in LRUs.dest_lru_list:
                dest_dict[dest] = None

            ## Go through each of dest in the LRU in question
            for dest in LRUs.dest_lru_list:
                ## Get pins that has dest.lru == dest
                for PINS in LRUs.pin_interconnections_list:
                    if PINS.DEST.lru == dest:
                        src_LRU, dst_LRU = self.getLRUInterconnections(PARAMS, PINS.SOURCE.lru, PINS.DEST.lru)
                        print(src_LRU.source_lru, src_LRU.POSITION.row, src_LRU.POSITION.col, dst_LRU.source_lru, dst_LRU.POSITION.row, dst_LRU.POSITION.col)
                        print("self.settings[GridView][overlap_endpoints]:", self.settings["GridView"]["overlap_endpoints"])

                        ## if col is same, top or bottom
                        if src_LRU.POSITION.col == dst_LRU.POSITION.col:
                            if src_LRU.POSITION.row > dst_LRU.POSITION.row:
                                if self.settings["GridView"]["overlap_endpoints"] == "True":
                                    PINS.source_loc = PARAMS.directionDict["up"]
                                    PINS.dest_loc = PARAMS.directionDict["down"]
                                else:
                                    ## dont allow overlap
                                    PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "up")
                                    PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "down")

                            else:
                                if self.settings["GridView"]["overlap_endpoints"] == "True":
                                    PINS.source_loc = PARAMS.directionDict["down"]
                                    PINS.dest_loc = PARAMS.directionDict["up"]
                                else:
                                    ## dont allow overlap
                                    PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "down")
                                    PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "up")


                            ## change value from None
                            dest_dict[PINS.DEST.lru] = "Done"

                            ## update XXXXX_empty to True
                            if PINS.source_loc == PARAMS.directionDict["up"]:
                                src_LRU.isTop_empty = False
                            if PINS.source_loc == PARAMS.directionDict["down"]:
                                src_LRU.isBottom_empty = False
                            if PINS.dest_loc == PARAMS.directionDict["up"]:
                                dst_LRU.isTop_empty = False
                            if PINS.dest_loc == PARAMS.directionDict["down"]:
                                dst_LRU.isBottom_empty = False



                        ## if row is same, left or right
                        if src_LRU.POSITION.row == dst_LRU.POSITION.row:
                            if src_LRU.POSITION.col < dst_LRU.POSITION.col:
                                if self.settings["GridView"]["overlap_endpoints"] == "True":
                                    PINS.source_loc = PARAMS.directionDict["right"]
                                    PINS.dest_loc = PARAMS.directionDict["left"]
                                else:
                                    ## dont allow overlap
                                    PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "right")
                                    PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "left")

                            else:

                                if self.settings["GridView"]["overlap_endpoints"] == "True":
                                    PINS.source_loc = PARAMS.directionDict["left"]
                                    PINS.dest_loc = PARAMS.directionDict["right"]
                                else:
                                    ## dont allow overlap
                                    PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "left")
                                    PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "right")


                            ## change value from None
                            dest_dict[PINS.DEST.lru] = "Done"

                            ## update XXXXX_empty to True
                            if PINS.source_loc == PARAMS.directionDict["up"]:
                                src_LRU.isTop_empty = False
                            if PINS.source_loc == PARAMS.directionDict["down"]:
                                src_LRU.isBottom_empty = False
                            if PINS.dest_loc == PARAMS.directionDict["up"]:
                                dst_LRU.isTop_empty = False
                            if PINS.dest_loc == PARAMS.directionDict["down"]:
                                dst_LRU.isBottom_empty = False

                        print("PINS.source_loc: ", PINS.source_loc, "PINS.dest_loc:", PINS.dest_loc)

            ## iterate through the dictionary
            for key, value in dest_dict.items():
                if value == None:
                    ## Not a direct/straight connection
                    ## must go diagonally
                    print("...Not a direct/straight connection")

                    ## Get PINS that has dest.lru == dest
                    for PINS in LRUs.pin_interconnections_list:
                        if PINS.DEST.lru == key:
                            src_LRU, dst_LRU = self.getLRUInterconnections(PARAMS, PINS.SOURCE.lru, PINS.DEST.lru)


                            ## dest is somewhere in the bottom
                            if src_LRU.POSITION.row < dst_LRU.POSITION.row:
                                if src_LRU.POSITION.col < dst_LRU.POSITION.col:
                                    ## dest to the right
                                    if self.settings["GridView"]["overlap_endpoints"] == "True":
                                        if src_LRU.isBottom_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["down"]

                                        elif src_LRU.isRight_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["right"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", src_LRU.source_lru, " no available connections")

                                        if dst_LRU.isTop_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["up"]

                                        elif dst_LRU.isLeft_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["left"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", dst_LRU.source_lru, " no available connections")
                                    else:

                                        if src_LRU.isBottom_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["down"]

                                        elif src_LRU.isRight_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["right"]

                                        else:
                                            PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "right")


                                        if dst_LRU.isTop_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["up"]

                                        elif dst_LRU.isLeft_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["left"]

                                        else:
                                            PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "left")



                                else:
                                    if self.settings["GridView"]["overlap_endpoints"] == "True":
                                        ## dest to the left
                                        if src_LRU.isLeft_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["left"]

                                        elif src_LRU.isBottom_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["down"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", src_LRU.source_lru, " no available connections")

                                        if dst_LRU.isTop_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["up"]

                                        elif dst_LRU.isRight_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["right"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", dst_LRU.source_lru, " no available connections")

                                    else:
                                        ## dest to the left
                                        if src_LRU.isLeft_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["left"]

                                        elif src_LRU.isBottom_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["down"]

                                        else:
                                            PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "down")

                                        if dst_LRU.isTop_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["up"]

                                        elif dst_LRU.isRight_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["right"]

                                        else:
                                            PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "right")


                            ## dest is somewhere in the top
                            if src_LRU.POSITION.row > dst_LRU.POSITION.row:
                                if src_LRU.POSITION.col < dst_LRU.POSITION.col:
                                    if self.settings["GridView"]["overlap_endpoints"] == "True":
                                        ## dest to the right
                                        if src_LRU.isTop_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["up"]

                                        elif src_LRU.isRight_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["right"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", src_LRU.source_lru, " no available connections")

                                        if dst_LRU.isBottom_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["down"]

                                        elif dst_LRU.isLeft_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["left"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", dst_LRU.source_lru, " no available connections")

                                    else:
                                        ## dest to the right
                                        if src_LRU.isTop_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["up"]

                                        elif src_LRU.isRight_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["right"]

                                        else:
                                            PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "right")

                                        if dst_LRU.isBottom_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["down"]

                                        elif dst_LRU.isLeft_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["left"]

                                        else:
                                            PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "left")



                                else:
                                    if self.settings["GridView"]["overlap_endpoints"] == "True":
                                        ## dest to the left
                                        if src_LRU.isLeft_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["left"]

                                        elif src_LRU.isTop_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["up"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", src_LRU.source_lru, " no available connections")

                                        if dst_LRU.isBottom_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["down"]

                                        elif dst_LRU.isRight_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["right"]

                                        else:
                                            ## Error
                                            logging.error("%s has no more available connections", src_LRU.source_lru)
                                            print("Error:", dst_LRU.source_lru, " no available connections")

                                    else:
                                        ## dest to the left
                                        if src_LRU.isLeft_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["left"]

                                        elif src_LRU.isTop_empty == True:
                                            PINS.source_loc = PARAMS.directionDict["up"]

                                        else:
                                            PINS.source_loc = self.pickDirection(PARAMS, src_LRU, "up")

                                        if dst_LRU.isBottom_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["down"]

                                        elif dst_LRU.isRight_empty == True:
                                            PINS.dest_loc = PARAMS.directionDict["right"]

                                        else:
                                            PINS.dest_loc = self.pickDirection(PARAMS, dst_LRU, "right")

                    ## update XXXXX_empty to True
                    if PINS.source_loc == PARAMS.directionDict["up"]:
                        src_LRU.isTop_empty = False
                    if PINS.source_loc == PARAMS.directionDict["down"]:
                        src_LRU.isBottom_empty = False
                    if PINS.dest_loc == PARAMS.directionDict["up"]:
                        dst_LRU.isTop_empty = False
                    if PINS.dest_loc == PARAMS.directionDict["down"]:
                        dst_LRU.isBottom_empty = False

                    print("PINS.source_loc: ", PINS.source_loc, "PINS.dest_loc:", PINS.dest_loc)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def pickDirection(self, PARAMS, LRU, direction):
        print("...picking a direction")
        PINS_loc = None

        if direction == "up":
            if LRU.isTop_empty == True:
                PINS_loc = PARAMS.directionDict["up"]
            else:
                ## Need to get another availabe direction/loc
                PINS_loc = self.pickNewDirection(PARAMS, LRU)

        elif direction == "down":
            if LRU.isBottom_empty == True:
                PINS_loc = PARAMS.directionDict["down"]
            else:
                ## Need to get another availabe direction/loc
                PINS_loc = self.pickNewDirection(PARAMS, LRU)

        elif direction == "left":
            if LRU.isLeft_empty == True:
                PINS_loc = PARAMS.directionDict["left"]
            else:
                ## Need to get another availabe direction/loc
                PINS_loc = self.pickNewDirection(PARAMS, LRU)

        elif direction == "right":
            if LRU.isRight_empty == True:
                PINS_loc = PARAMS.directionDict["right"]
            else:
                ## Need to get another availabe direction/loc
                PINS_loc = self.pickNewDirection(PARAMS, LRU)

        else:
            doing = None


        return PINS_loc



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def pickNewDirection(self, PARAMS, LRU):
        print("...picking another direction")
        PINS_loc = None

        if LRU.isTop_empty == True:
            PINS_loc = PARAMS.directionDict["up"]
        elif LRU.isBottom_empty == True:
            PINS_loc = PARAMS.directionDict["down"]
        elif LRU.isLeft_empty == True:
            PINS_loc = PARAMS.directionDict["left"]
        elif LRU.isRight_empty == True:
            PINS_loc = PARAMS.directionDict["right"]
        else:
            doing = None

        return PINS_loc


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getLRUInterconnections(self, PARAMS, source_LRU, dest_LRU):
        print("...Getting LRU with source:",source_LRU,"and DEST:", dest_LRU  , "from PARAMS.LRUInterconnectionList")
        for LRUs in PARAMS.LRUInterconnectionList:
            if LRUs.source_lru == source_LRU:
                source_LRU_interconnection = LRUs
            elif LRUs.source_lru == dest_LRU:
                dest_LRU_interconnection = LRUs
            else:
                ## do nothing
                doing = None

        return source_LRU_interconnection, dest_LRU_interconnection

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def verifyPathListDicts(self, PARAMS):
        print("...Verify path_list_dicts.  Cannot be multiple loops")
        ## Need to check loops, cannot be multiple loops
        Loop1_1st_list = []

        ## Get all the 1st elements, put it in a list
        for path_dicts in PARAMS.pathLoopsNoDuplicateDictList:
            Loop1_list = path_dicts["Loop1"]
            first_elem = Loop1_list[0]
            Loop1_1st_list.append(first_elem)

        ## Generate a dictionary base on 1st elements
        for item in Loop1_1st_list:
            PARAMS.LoopsDict[item] = []

        ## insert path_dicts in the dictionary
        for path_dicts in PARAMS.pathLoopsNoDuplicateDictList:
            Loop1_list = path_dicts["Loop1"]
            first_elem = Loop1_list[0]
            PARAMS.LoopsDict[first_elem].append(path_dicts)

        if self.settings["GridView"]["delete_multiple_loops"] == "False":
            ## Go through the dict, if len is greater than 1, need to do update (special loop)
            for key, value in PARAMS.LoopsDict.items():
                if len(value) > 1:
                    print("...Multiple loops detected at", key)
                    PARAMS.multipleLoopsKey.append(key)
                    pathList = value
                    ## gather unique ones (delete its LoopCorner, delete non unique ones
                    self.getUniquePathsOnly(PARAMS, pathList)

                    if self.settings["GridView"]["duplicateLRU"] == "True":
                        ## setting LoopA/LoopB
                        self.setLoopAB(PARAMS, key, value)
                else:
                    print("...no multiple loops detected")


        print("Testing only-------")
        print("PARAMS.multipleloopsCornerLRUDict", PARAMS.multipleloopsCornerLRUDict)
        print("PARAMS.LoopsDict: ", PARAMS.LoopsDict)
        for each in PARAMS.pathLoopsNoDuplicateDictList:
            print("PARAMS.pathLoopsNoDuplicateDictList dicts:", each)


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getUniquePathsOnly(self, PARAMS, pathList):
        print("...Getting unique_ones_only.  Delete its LoopCorner, delete non unique ones")
        unique_LRUs = []
        delete_list = []

        x = -1

        for dict in pathList:
            x = x + 1
            has_new = False
            for lru in dict['Paths']:
                if lru in unique_LRUs:
                    doing = None
                else:
                    ## not in unique yet
                    unique_LRUs.append(lru)
                    has_new = True

            if has_new == True:
                ## keep path, but remove LoopCorner
                dict['LoopCorner'] = []
                dict['Loop1'] = []
            else:
                ## delete path from 'PARAMS.pathLoopsNoDuplicateDictList' and 'pathList'
                self.deleteFromPathListDicts(PARAMS, dict)
                delete_list.append(x)

        if delete_list != []:
            for index in reversed(delete_list):
                pathList.remove(pathList[index])


    ####################################################################################################################
    ## 
    ####################################################################################################################
    def deleteFromPathListDicts(self, PARAMS, dict):
        delete_list = []

        x = -1
        for path_dicts in PARAMS.pathLoopsNoDuplicateDictList:
            x = x + 1
            if path_dicts['Paths'] == dict['Paths']:
                delete_list.append(x)

        if delete_list != []:
            for index in reversed(delete_list):
                PARAMS.pathLoopsNoDuplicateDictList.remove(PARAMS.pathLoopsNoDuplicateDictList[index])



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def setLoopAB(self, PARAMS, key, value_list):
        print("...Setting loopA_loopB")

        unique_lru_dict =  self.getNumInstances(PARAMS, value_list)

        print("unique_lru_dict: ", unique_lru_dict)

        ## return the corner LRUs for loops
        loops_cornerLRU_dict = self.getLoopsCornerLRU(PARAMS, unique_lru_dict)
        PARAMS.multipleloopsCornerLRUDict = loops_cornerLRU_dict
        ## return new names for the corner LRUs
        renameDict = self.getLoopsCornerLRUNewLRUnames(PARAMS, loops_cornerLRU_dict)
        ## return switched key/value of renameDict
        rename_dict_switched = self.switchRename_dict(renameDict)
        ## return updated value of rename_dict_switched, including preceding LRUs
        rename_dict_switched_complete = self.renameDictComplete(PARAMS, rename_dict_switched)

        ## rename LRUs in pathlist.  Pathloops also got changed
        self.renameLRUsInPathlist(PARAMS, rename_dict_switched_complete)

        ## set loop A and loop B for PARAMS.pathLoopsNoDuplicateDictList
        self.loopAB(PARAMS, loops_cornerLRU_dict)

        self.updateLRUConnectionsLoops(PARAMS, renameDict)

        ## if LRUSTARTINGCONNECTION is an LRU that was renamed, set it to new LRU with 0
        for key, value in renameDict.items():
            if PARAMS.LRUSTARTINGCONNECTION.source_lru == key:
                LRU_new = None
                for item in PARAMS.LRUInterconnectionList:
                    if item.source_lru == key + PARAMS.delimeterDuplicatingLRU + str(format(0, self.format_duplicating_LRU)):
                        LRU_new = item

                PARAMS.LRUSTARTINGCONNECTION = LRU_new

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def loopAB(self, PARAMS, loops_cornerLRU_dict):
        print("...Setting loops A, B, C, D")
        print("loopA_loopB:", loops_cornerLRU_dict)

        for key1, corners_list in loops_cornerLRU_dict.items():
            for key2, pathloops_list in PARAMS.LoopsDict.items():
                ## check if it part of multiple loops
                if key2 in PARAMS.multipleLoopsKey:
                    for dict in pathloops_list:

                        for cornerlru in corners_list:
                            if dict["Loops_B"] == []:
                                temp_path_list = dict["Paths"]
                                loopA = []
                                loopB = []
                                inLoop = 'A'

                                for lru in temp_path_list:
                                    ## check if ECM0
                                    if lru == str(cornerlru)+ PARAMS.delimeterDuplicatingLRU + format(0, self.format_duplicating_LRU):
                                        loopA.append(lru)
                                        inLoop = '_B'

                                    if inLoop == 'A':
                                        loopA.append(lru)
                                    elif inLoop == 'B':
                                        loopB.append(lru)
                                    elif inLoop == '_B':
                                        inLoop = 'B'
                                    else:
                                        doing = None


                        dict["Loops_A"] = loopA
                        dict["Loops_B"] = loopB

                        loopC = []
                        loopD = []

                        ## gather loopC
                        for item in dict["Loops_B"]:
                            isFound = False
                            for key, renameDict in PARAMS.renameDict.items():
                                for lru, value in renameDict.items():
                                    if item == lru:
                                        isFound = True
                                        break

                            if isFound == False:
                                loopC.append(item)
                            else:
                                ## dont add if it ends with 0
                                if item[-1] == str(0):
                                    doing = None
                                else:
                                    loopD.append(item)

                        dict["Loops_C"] = loopC
                        dict["Loops_D"] = loopD



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def updateLRUConnectionsLoops(self, PARAMS, renameDict):
        print("\n...Updating LRU connections in LoopsA/LoopsB")
        print("renameDict:", renameDict)

        for keyLRU, newLRU_connection_dict in renameDict.items():
            ## reinitialize variables
            temp_lru_interconnection_list = []
            num_LRUs = 0
            LRU_ORIG = None

            LRU = PARAMS.getLRUInterconnection(keyLRU)
            print("Need to rename: ", LRU.source_lru)

            LRU_ORIG = LRU
            ORIG_LRU = copy.deepcopy(LRU)

            ## printdata, for testing purposes
            #LRU.printdata(isPin=True,isConnection=True, isInternal=True)

            for newlruname, cable_connection in newLRU_connection_dict.items():
                print("newlruname: ", newlruname, "cable_connection: ", cable_connection)

                ## copy orig
                LRU_new = copy.deepcopy(LRU)

                ## append new interconnection to the list
                temp_lru_interconnection_list.append(LRU_new)
                num_LRUs = num_LRUs + 1

                ## rename source_lru
                LRU_new.source_lru = newlruname

                ## update dest_lru_list base on cable_connection
                remove_list = []
                ## If it starts with 0, like DSP0
                if newlruname == keyLRU + str(0):

                    remove_lru_list = []

                    ## remove every connection that are in the renameDict except with XXXX0
                    for key, cables in newLRU_connection_dict.items():
                        if key != newlruname:
                            remove_lru_list.append(cables)

                    for x in range(0, len(LRU_new.dest_lru_list)):
                        if LRU_new.dest_lru_list[x] in remove_lru_list:
                            remove_list.append(x)
                    for items in reversed(remove_list):
                        LRU_new.dest_lru_list.pop(items)
                else:
                    for x in range(0,len(LRU_new.dest_lru_list)):
                        ## remove every connection except the cable_connection
                        if LRU_new.dest_lru_list[x] != cable_connection:
                            remove_list.append(x)
                    for items in reversed(remove_list):
                        LRU_new.dest_lru_list.pop(items)

                ## update pin_interconnections_list
                remove_list = []
                for x in range(0, len(LRU_new.pin_interconnections_list)):
                    if LRU_new.pin_interconnections_list[x].DEST.lru in LRU_new.dest_lru_list:
                        LRU_new.pin_interconnections_list[x].SOURCE.lru = newlruname
                    else:
                        remove_list.append(x)
                for num in reversed(remove_list):
                    LRU_new.pin_interconnections_list.pop(num)

                ## printdata, for testing purposes
                #LRU_new.printdata(isPin=True)


            print("...Before changing the order of list")
            for item in temp_lru_interconnection_list:
                print(item.source_lru)

            temp_dict = {}
            for item in temp_lru_interconnection_list:
                ## set key as last letter (num) of source_lru
                key = int(item.source_lru[-1])
                temp_dict[key] = item
            ## reset temp_lru_interconnection_list
            temp_lru_interconnection_list = []
            ## change order of list from 0 to max
            for x in range(0,num_LRUs):
                ## go through each key, from 0 to max
                temp_lru_interconnection_list.append(temp_dict[x])

            print("...Ater changing the order of list")
            for item in temp_lru_interconnection_list:
                print(item.source_lru)

            ## add connections between new LRUs
            self.addConnectionsBetweenNewLRU(PARAMS, num_LRUs, temp_lru_interconnection_list, LRU_ORIG)

            ## append this for future use
            PARAMS.lrusExpandedList.append(ORIG_LRU)

            ## delete LRU from LRUInterconnectionList
            PARAMS.LRUInterconnectionList.remove(LRU_ORIG)


    ####################################################################################################################
    ## Get the corner of the loops
    ####################################################################################################################
    def getLoopsCornerLRU(self, PARAMS, unique_lru_dict):
        print("...Getting loops_cornerLRU")
        loops_cornerLRU_dict = {}

        ## get the unique_lru in a list form
        unique_lru_list = []
        for key, value in unique_lru_dict.items():
            unique_lru_list.append(key)

        for dicts in PARAMS.pathLoopsNoDuplicateDictList:
            ## add to loops_cornerLRU_list, if its not there yet

            ## check if dicts has lrus unique_lru_dict items
            inUniquelru = True
            for lru in dicts["Paths"]:
                if lru in unique_lru_list:
                    doing = None
                else:
                    inUniquelru = False
                    break

            ## check if dicts has lrus unique_lru_dict items
            if inUniquelru == True:
                try:
                    print(loops_cornerLRU_dict[dicts["Loops_at"]])
                except:
                    ## Key doenst exist yet, make it
                    loops_cornerLRU_dict[dicts["Loops_at"]] = [dicts["Loops_at"]]


                for lru in reversed(dicts["Paths"]):
                    if lru != dicts["Loops_at"]:
                        ## Cannot be where it loops at
                        ## where it loops at will automatically be duplicated
                        if unique_lru_dict[lru] > 1:
                            if lru in loops_cornerLRU_dict[dicts["Loops_at"]]:
                                doing = None
                            else:
                                loops_cornerLRU_dict[dicts["Loops_at"]].append(lru)
                            break

            else:
                doing = None

        print("loops_cornerLRU_dict: ", loops_cornerLRU_dict)

        return loops_cornerLRU_dict

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getLoopsCornerLRUNewLRUnames(self, PARAMS, loops_cornerLRU_dict):
        print("...Getting loops_cornerLRU_newLRUnames")
        print("...Updating LRUs in loops_cornerLRU_list!!!!!!")

        for LRUstartingKey, cornerLRU_list in loops_cornerLRU_dict.items():
            print("LRUstartingKey: ", LRUstartingKey, "\tcornerLRU: ", cornerLRU_list)
            current_list = PARAMS.LoopsDict[LRUstartingKey]
            renameDict = {}

            for x in range(0, len(cornerLRU_list)):
                lru_listed = []
                lru_rename = cornerLRU_list[x]
                renameDict[lru_rename] = {}
                for dict in current_list:
                    print("dict: ", dict)
                    for y in range(0, len(dict['Paths'])):

                        ## if out of range, get the last item
                        try: itemBefore = dict['Paths'][y-1]
                        except: itemBefore = dict['Paths'][len(dict['Paths'])]

                        itemNow = dict['Paths'][y]

                        ## #if out of range, get the first item
                        try: itemAfter = dict['Paths'][y+1]
                        except: itemAfter = dict['Paths'][0]

                        if itemNow == lru_rename:

                            ## first item
                            if x == 0 and y == 0:
                                if itemAfter not in lru_listed:
                                    newitem = len(renameDict[lru_rename])
                                    newLRU = lru_rename + PARAMS.delimeterDuplicatingLRU + str(format(newitem, self.format_duplicating_LRU))

                                    renameDict[lru_rename][newLRU] = itemAfter
                                    lru_listed.append(itemAfter)
                            else:
                                ## check itemBefore
                                if (itemBefore not in lru_listed) and (itemBefore != itemNow):
                                    newitem = len(renameDict[lru_rename])
                                    newLRU = lru_rename + PARAMS.delimeterDuplicatingLRU + str(format(newitem, self.format_duplicating_LRU))

                                    renameDict[lru_rename][newLRU] = itemBefore
                                    lru_listed.append(itemBefore)

                                ## check itemAfter
                                if (itemAfter not in lru_listed) and (itemAfter != itemNow):
                                    newitem = len(renameDict[lru_rename])
                                    newLRU = lru_rename + PARAMS.delimeterDuplicatingLRU + str(format(newitem, self.format_duplicating_LRU))

                                    renameDict[lru_rename][newLRU] = itemAfter
                                    lru_listed.append(itemAfter)

            print("...Need to rename LRUs listed below:")
            print("renameDict", renameDict)
            print("lru_listed", lru_listed)

            PARAMS.renameDict = renameDict

            return renameDict

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def switchRename_dict(self, renameDict):
        print("...Switching renameDict")
        rename_dict_switched = {}

        print("Before switching: ", renameDict)
        for key, dict in renameDict.items():
            rename_dict_switched[key] = {}
            new_dict = {}

            for key2, value in dict.items():
                new_dict[value] = []
                new_dict[value].append(key2)

            rename_dict_switched[key] = new_dict

        print("After switching: ", rename_dict_switched)
        return rename_dict_switched

    ####################################################################################################################
    ## 
    ####################################################################################################################
    def renameDictComplete(self, PARAMS, rename_dict_switched):
        print("...renaming dict_complete")
        print("Before completing: ", rename_dict_switched)

        for key, dict in rename_dict_switched.items():
            for key2, list in dict.items():
                ## get the last number
                num = int(list[0][-1])
                ## not LRU0
                if num != 0:
                    while num != 0:
                        lruname = key + PARAMS.delimeterDuplicatingLRU + str(format(num - 1, self.format_duplicating_LRU))
                        list.insert(0,lruname)
                        num = num - 1

        rename_dict_switched_complete = rename_dict_switched

        print("After completing: ", rename_dict_switched_complete)
        return rename_dict_switched_complete

    ####################################################################################################################
    ## for some reason, changing PARAMS.pathList updated PARAMS.pathLoopsNoDuplicateDictList
    ####################################################################################################################
    def renameLRUsInPathlist(self, PARAMS, rename_dict_switched_complete):
        print("...renaming LRUs in pathlist")
        print(rename_dict_switched_complete)

        revertback_path_list = copy.deepcopy(PARAMS.pathList)

        print("...before renaming ",PARAMS.pathList)
        for pathlist in PARAMS.pathList:
            for n, lru in enumerate(pathlist):
                for key, dict in rename_dict_switched_complete.items():
                    if key == lru:
                        for key2, lrulist in dict.items():

                            if n == 0:
                                ## start
                                if pathlist[n+1] == key2:
                                    if len(lrulist) > 1:
                                        ## remove original
                                        pathlist.pop(n)
                                        ## insert new values
                                        for items in reversed(lrulist):
                                            pathlist.insert(n,items)
                                    else:
                                        pathlist[n] = lrulist[0]

                            elif n == (len(pathlist)-1):
                                ## end
                                if pathlist[n - 1] == key2:
                                    if len(lrulist) > 1:
                                        ## remove original
                                        pathlist.pop(n)
                                        ## insert new values
                                        for items in lrulist:
                                            pathlist.insert(n, items)
                                    else:
                                        pathlist[n] = lrulist[0]

                            else:
                                ## in the middle

                                ## check afterwards, before hand should be handled
                                if pathlist[n + 1] == key2:
                                    if len(lrulist) > 1:
                                        ## remove original
                                        pathlist.pop(n)
                                        ## insert new values
                                        for items in reversed(lrulist):
                                            pathlist.insert(n, items)
                                    else:
                                        pathlist[n] = lrulist[0]

        print("afterward renaming", PARAMS.pathList)



    ####################################################################################################################
    ## 
    ####################################################################################################################
    def getNumInstances(self, PARAMS, value_list):
        print("...Getting number of instances an LRU is called/connected to?")
        unique_lru_list = []
        ## Get unique_lru_list for the current LRU key
        for dict in value_list:
            for lru in dict["Paths"]:
                if lru in unique_lru_list:
                    doing = None
                else:
                    unique_lru_list.append(lru)

        ## Count number of times lru comes out in the paths for the current LRU key
        unique_lru_dict = {}
        for lru in unique_lru_list:
            unique_lru_dict[lru] = 0
            for dict in value_list:
                if lru in dict["Paths"]:
                    unique_lru_dict[lru] = unique_lru_dict[lru] + 1

        return unique_lru_dict



