import myLog

####################################################################################################################
##
####################################################################################################################
class Generator_js():
    @myLog.catch_wrapper
    def __init__(self,PARAMS, nameOfFile, settings, delimeterDuplicatingLRU="not_passed"):
        ## PROPERTIES
        self.drawnConnectionStringList = []
        self.settings = settings

        ## METHODS
        nameOfFile = self.updateFileName(nameOfFile, delimeterDuplicatingLRU)
        self.generateJs(PARAMS, nameOfFile)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def updateFileName(self, nameOfFile, delimeterDuplicatingLRU):
        if delimeterDuplicatingLRU == "not_passed":
            doing = None
        else:
			## IF DELIMETER IS IN THE nameOfFile, UPDATE nameOfFile TO END BEFORE THE DELIMETER
            if delimeterDuplicatingLRU in nameOfFile:
                end_here = nameOfFile.find(delimeterDuplicatingLRU)
                print("...name of file was:", nameOfFile)
                nameOfFile = nameOfFile[:end_here]
                print("...name of file will now be:", nameOfFile)

        return nameOfFile

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generateJs(self, PARAMS, nameOfFile):
        print("...Generating JS")

        ## CREATE A JS FILE CALLED name_of_file
        jsfile = open("../output/" + nameOfFile + '.js', 'w', encoding='utf-8')

        jsfile.write("jsPlumb.ready(function() {")

		## GO THROUGH EACH LRU IN THE LIST
        for LRUS in PARAMS.LRUInterconnectionList:
            print("LRU:", LRUS.source_lru)
			## GO THROUGH EACH OF DEST IN THE LRU IN QUESTION
            for dest in LRUS.dest_lru_list:
                print("dest:", dest)
                temp_pins_list = []
				## GET PINS THAT HAS dest.lru == dest
                for PINS in LRUS.pin_interconnections_list:
                    if PINS.DEST.lru == dest:
                        temp_pins_list.append(PINS)

                print("pins_list", temp_pins_list)
                jsfile.write("\n")
                jsfile.write(self.jsAddEndPoint(PARAMS, temp_pins_list))

        jsfile.write("});")
        jsfile.close()

    ####################################################################################################################
    ##
    ####################################################################################################################
    def jsAddEndPoint(self, PARAMS, temp_pins_list):

        """
        /* *****************************************
        ----- Use Rectangle for output
        ----- Use Dot for input (red for control)
        endpoint:"Dot",

        ----- For control
        fillStyle:"red"
        ----- For others
        fillStyle:"gray"
        ----- For not specified
        fillStyle:"yellow"

        --TOP LEFT
        anchor:[0,0,0,0,0,0],
        --TOP MIDDLE
        anchor:[0.5,0,0,0,0,0],
        --TOP RIGHT
        anchor:[1,0,0,0,0,0],
        -----Label when pin is on TOP
        location: [0.5,1.5],

        --BOTTOM LEFT
        anchor:[0,1,0,0,0,0],
        --BOTTOM MIDDLE
        anchor:[0.5,1,0,0,0,0],
        --BOTTOM RIGHT
        anchor:[1,1,0,0,0,0],
        -----Label when pin is on BOTTOM
        location: [0.5,-.5],

         --LEFT MIDDLE
        anchor:[0,0.5,0,0,0,0],
        -----Label when pin is on LEFT
        location: [1.5,0.5],

        --RIGHT MIDDLE
        anchor:[1,0.5,0,0,0,0],
        -----Label when pin is on RIGHT
        location: [-0.5,0.5],
        *****************************************  */
        """

        total_string = ""

        num_pins = len(temp_pins_list)
        spacing = 1 / (num_pins + 1)
        space = spacing
        for PIN in temp_pins_list:
			## CHECK SOURCE (NO LONGER CHECKING DEST)
            #if PIN.SOURCE.getString() in self.drawnConnectionStringList and PIN.DEST.getString() in self.drawnConnectionStringList and PIN.SOURCE.conn != "" and PIN.SOURCE.pin != "":
            if PIN.SOURCE.getString() in self.drawnConnectionStringList:
				## ALREADY DRAWN BEFORE, DO NOTHING
                print("drawn before:", PIN.SOURCE.getString())
                doing = None
            else:
				## NEED TO DRAW
                self.drawnConnectionStringList.append(PIN.SOURCE.getString())
                self.drawnConnectionStringList.append(PIN.DEST.getString())

                if self.settings["GridView"]["draw_one_at_a_time"] == "True":
                    PARAMS.totalDelay = PARAMS.totalDelay + int(self.settings["GridView2"]["delay_time"])
                    delay = PARAMS.totalDelay
                    endpoint_string = "setTimeout(function () {" + self.writeAddEndPoint(PARAMS, PIN, space) + "}," + str(delay) + ");"
                else:
                    endpoint_string = self.writeAddEndPoint(PARAMS, PIN, space)

                total_string = total_string + "\n" + endpoint_string

            space = space + spacing

        return total_string

    ####################################################################################################################
    ##
    ####################################################################################################################
    def writeAddEndPoint(self, PARAMS, PIN_interconnection, var):

        label_top = [0.5, 2.5]
        label_bottom = [0.5, -1.5]
        label_right = [-2, 0.5]
        label_left = [3, 0.5]

        color_control = self.settings["Color"]["color_control"]
        color_unknown = self.settings["Color"]["color_unknown"]
        color_input = self.settings["Color"]["color_input"]
        color_same = self.settings["Color"]["color_same"]
        color_output = self.settings["Color"]["color_output"]

        shape_control = self.settings["Shape"]["shape_control"]
        shape_unknown = self.settings["Shape"]["shape_unknown"]
        shape_input = self.settings["Shape"]["shape_input"]
        shape_output = self.settings["Shape"]["shape_output"]
        shape_same = self.settings["Shape"]["shape_same"]

        # anchor_top = [var, 0, 0, 0, 0, 0]
        anchor_top = setAnchorOnTop(var)
        # anchor_bottom = [var, 1, 0, 0, 0, 0]
        anchor_bottom = setAnchorOnBottom(var)
        # anchor_left = [0, var, 0, 0, 0, 0]
        anchor_left = setAnchorOnLeft(var)
        # anchor_right = [1, var, 0, 0, 0, 0]
        anchor_right = setAnchorOnRight(var)

        source_anchor = []
        dest_anchor = []
        source_name = ""
        dest_name = ""
        shape = ""
        color = ""
        location = None
        label = ""
        pin_string = ""

		## FOR THE SOURCE
        source_name = PIN_interconnection.SOURCE.lru
        label = PIN_interconnection.SOURCE.conn + ":" + PIN_interconnection.SOURCE.pin

        if PIN_interconnection.SOURCE.type == PARAMS.signalTypeDict["input"]:
            shape = shape_input
            color = color_input
        elif PIN_interconnection.SOURCE.type == PARAMS.signalTypeDict["same"]:
            shape = shape_same
            color = color_same
        elif PIN_interconnection.SOURCE.type == PARAMS.signalTypeDict["output"]:
            shape = shape_output
            color = color_output
        elif PIN_interconnection.SOURCE.type == PARAMS.signalTypeDict["control"]:
            shape = shape_control
            color = color_control
        else:
			## UNKNOWN/NONE
            shape = shape_unknown
            color = color_unknown

        if PIN_interconnection.source_loc == PARAMS.directionDict["up"]:
            source_anchor = anchor_top
            location = label_top
        elif PIN_interconnection.source_loc == PARAMS.directionDict["down"]:
            source_anchor = anchor_bottom
            location = label_bottom
        elif PIN_interconnection.source_loc == PARAMS.directionDict["right"]:
            source_anchor = anchor_right
            location = label_right
        elif PIN_interconnection.source_loc == PARAMS.directionDict["left"]:
            source_anchor = anchor_left
            location = label_left
        else:
            print("Unknown source loc")

        pin_string = pin_string + "\n"
        pin_string = pin_string + "jsPlumb.addEndpoint(\"" + source_name + "\", { "
        pin_string = pin_string + "endpoint:\"" + shape + "\","
        pin_string = pin_string + "anchor:" + str(source_anchor) + ","
        pin_string = pin_string + "paintStyle: { fillStyle:\"" + color + "\", outlineColor:\"black\", outlineWidth:1},"
        pin_string = pin_string + "overlays: [[\"Label\", {"
        pin_string = pin_string + "location: " + str(location) + ","
        pin_string = pin_string + "label: \"" + label + "\","
        pin_string = pin_string + "visible:true,"
        pin_string = pin_string + "id: \"" + source_name + label + "\","

        pin_string = pin_string + "}]]"
        pin_string = pin_string + "});"

		## FOR THE DEST
        dest_name = PIN_interconnection.DEST.lru
        label = PIN_interconnection.DEST.conn + ":" + PIN_interconnection.DEST.pin

        if PIN_interconnection.DEST.type == PARAMS.signalTypeDict["input"]:
            shape = shape_input
            color = color_input
        elif PIN_interconnection.SOURCE.type == PARAMS.signalTypeDict["same"]:
            shape = shape_same
            color = color_same
        elif PIN_interconnection.DEST.type == PARAMS.signalTypeDict["output"]:
            shape = shape_output
            color = color_output
        elif PIN_interconnection.DEST.type == PARAMS.signalTypeDict["control"]:
            shape = shape_control
            color = color_control
        else:
			## UNKNOWN/NONE
            shape = shape_unknown
            color = color_unknown

        if PIN_interconnection.dest_loc == PARAMS.directionDict["up"]:
            if PIN_interconnection.source_loc == PARAMS.directionDict["down"]:
                dest_anchor = anchor_top
                location = label_top
            else:
				## FOR DIAGONAL CONNECTIONS
                var2 = 1 - var
                anchor_top = setAnchorOnTop(var2)
                dest_anchor = anchor_top
                location = label_top

        elif PIN_interconnection.dest_loc == PARAMS.directionDict["down"]:
            if PIN_interconnection.source_loc == PARAMS.directionDict["up"]:
                dest_anchor = anchor_bottom
                location = label_bottom
            else:
                ## FOR DIAGONAL CONNECTIONS
                var2 = 1 - var
                anchor_bottom = setAnchorOnBottom(var2)
                dest_anchor = anchor_bottom
                location = label_bottom


        elif PIN_interconnection.dest_loc == PARAMS.directionDict["right"]:
            if PIN_interconnection.source_loc == PARAMS.directionDict["left"]:
                dest_anchor = anchor_right
                location = label_right
            else:
                ## FOR DIAGONAL CONNECTIONS
                var2 = 1 - var
                anchor_right = setAnchorOnRight(var2)
                dest_anchor = anchor_right
                location = label_right

        elif PIN_interconnection.dest_loc == PARAMS.directionDict["left"]:
            if PIN_interconnection.source_loc == PARAMS.directionDict["right"]:
                dest_anchor = anchor_left
                location = label_left
            else:
                ## FOR DIAGONAL CONNECTIONS
                var2 = 1 - var
                anchor_left = setAnchorOnLeft(var2)
                dest_anchor = anchor_left
                location = label_left
        else:
            print("Unknown source loc")

        pin_string = pin_string + "\n"
        pin_string = pin_string + "jsPlumb.addEndpoint(\"" + dest_name + "\", { "
        pin_string = pin_string + "endpoint:\"" + shape + "\","
        pin_string = pin_string + "anchor:" + str(dest_anchor) + ","
        pin_string = pin_string + "paintStyle: { fillStyle:\"" + color + "\", outlineColor:\"black\", outlineWidth:1},"
        pin_string = pin_string + "overlays: [[\"Label\", {"
        pin_string = pin_string + "location: " + str(location) + ","
        pin_string = pin_string + "label: \"" + label + "\","
        pin_string = pin_string + "visible:true,"
        pin_string = pin_string + "id: \"" + dest_name + label + "\","

        pin_string = pin_string + "}]]"
        pin_string = pin_string + "});"

        """
            jsPlumb.addEndpoint("VCDM", {
                    endpoint:"Dot",
                    anchor:[1,0.5,0,0,0,0],
                    paintStyle: { fillStyle:"red", outlineColor:"black", outlineWidth:1},
                    overlays: [
                        ["Label", {
                            location: [0.5,1.5],
                            label: "P2",
                            visible:true,
                            id: "testing4",
                        }]
                        ]
                });
        """

        connect_string = self.jsConnect(PARAMS, source_name, dest_name, str(source_anchor), str(dest_anchor))
        total_string = connect_string + pin_string

        return total_string

    ####################################################################################################################
    ##
    ####################################################################################################################
    def jsConnect(self, PARAMS, source, target, sourcecoord, targetcoord):
        string = "jsPlumb.connect({source:\"" + source + "\", target:\"" + target + "\", anchor: [" + sourcecoord + "," + targetcoord + "],});"

        return string

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def setAnchorOnTop(var):
    anchor_top = [var, 0, 0, 0, 0, 0]
    return anchor_top

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def setAnchorOnBottom(var):
    anchor_bottom = [var, 1, 0, 0, 0, 0]
    return anchor_bottom

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def setAnchorOnLeft(var):
    anchor_left = [0, var, 0, 0, 0, 0]
    return anchor_left

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def setAnchorOnRight(var):
    anchor_right = [1, var, 0, 0, 0, 0]
    return anchor_right