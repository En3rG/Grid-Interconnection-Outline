import GenerateJS as JS
import GenerateHTML as HTML
import DrawOutline as DRAW
import DrawTree as DRAWTREE
import Common as CC
import PrepOutline as PREP
import PrepTree as PREPTREE
from lxml import etree
import copy
import DrawInserting as DRAWINSERTING
import PrepInserting as PREPINSERTING
import myLog

class Interconnection_Generator_Lrus():
    @myLog.catch_wrapper
    def __init__(self, LRU, xml_info, delimeterDuplicatingLRU="not_passed", lrus_explanded_list=[],
                 settings=None):
        ## PROPERTIES
        self.internal_counter = 0
        self.conn_counter = 0
        self.conn_format = '03d'
        self.wires_dict = {}
        self.internal_string = "_wire"
        self.internal_format = '03d'
        self.delimeterDuplicatingLRU = delimeterDuplicatingLRU
        self.lrusExpandedList = lrus_explanded_list
        self.additionalInfo = etree.Element('AdditionalInfo')
        self.xml_info = xml_info
        self.settings = settings

        ## GLOBAL PARAMS

        self.PARAMS = CC.Params(settings=settings)

        ## METHODS
        self.start(LRU, self.PARAMS)

    ####################################################################################################################
    ## MAIN
    ####################################################################################################################
    def start(self, LRU, PARAMS):
        print("...Starting on Interconnection_Generator_Lrus")

		## GENERATE PIN INTERCONNECTION FOR THE LRU
        self.generatePinInterconnections(PARAMS, LRU)

        self.drawInterconnection(PARAMS, LRU)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generatePinInterconnections(self, PARAMS, LRU):
        # print("Testing Interconnections for LRUs", LRU)
        print("...Generating pin_interconnection: ", LRU.source_lru)
        # LRU.printdata(isPin=True,isConnection=True, isInternal=True)

        print("For testing only ----------------------------------------------------")
        for PIN in LRU.pin_interconnections_list:
            print("SOURCE----")
            PIN.SOURCE.printdata()
            # print("DEST----")
            # pin.DEST.printdata()
            print("internal list-----")
            for connection in PIN.internal_list:
                connection.printdata()
        print("---------------------------------------------------------------------")

        for PIN in LRU.pin_interconnections_list:
            if self.delimeterDuplicatingLRU in PIN.SOURCE.lru:
                ## ITS A DUPLICATE LRU, NEED TO USE LRU IN lrusExpandedList
                if self.delimeterDuplicatingLRU in PIN.SOURCE.lru:
                    end_here = PIN.SOURCE.lru.find(self.delimeterDuplicatingLRU)
                    orig_LRU = PIN.SOURCE.lru[:end_here]

                    for LRU2 in self.lrusExpandedList:
                        if LRU2.source_lru == orig_LRU:
                            for PIN2 in LRU2.pin_interconnections_list:
                                print("...using LRU", LRU2.source_lru, "instead of", orig_LRU)
                                self.setSourceNDestination(PIN2, PARAMS)

            else:
                self.setSourceNDestination(PIN, PARAMS)


        # for PIN in LRU.pin_interconnections_list:
        #     if PIN.SOURCE.type == "same":
        #         print(PIN.SOURCE.lru ,"has 'same'")
        #
        #         if self.delimeterDuplicatingLRU == "not_passed":
        #             doing = None
        #         else:
        #             #####its a duplicate LRU, need to use LRU in lrusExpandedList
        #             if self.delimeterDuplicatingLRU in PIN.SOURCE.lru:
        #                 end_here = PIN.SOURCE.lru.find(self.delimeterDuplicatingLRU)
        #                 orig_LRU = PIN.SOURCE.lru[:end_here]
        #
        #                 for LRU in self.lrusExpandedList:
        #                     print(LRU)
        #                     if LRU.source_lru == orig_LRU:
        #                         for PIN2 in LRU.pin_interconnections_list:
        #                             self.setSourceNDestination(PIN2, PARAMS)
        #
        #     else:
        #         if self.delimeterDuplicatingLRU in PIN.SOURCE.lru:
        #             #####dont do anything, sometimes has __XX but doesnt have 'same' under type
        #             doing = None
        #         else:
        #             self.setSourceNDestination(PIN, PARAMS)


    ####################################################################################################################
    #####
    ####################################################################################################################
    def setSourceNDestination(self, PIN, PARAMS):
        print("...Setting source and destinations")
        print(PIN.SOURCE.lru, "components:", PIN.SOURCE.components)
		## IF COMPONENTS IS EMPTY
        if PIN.SOURCE.components == "":
            print("...components is empty")
            temp_pin = CC.Pin_Interconnection()
            temp_pin_reverse = CC.Pin_Interconnection()
            temp_source = CC.Pin()
            temp_dest = CC.Pin()

			## SET temp_source
            sourcelru = PIN.SOURCE.conn + "_" + PIN.SOURCE.pin
            lrutype = PIN.SOURCE.type
            temp_source = self.setConnectionInfo(PARAMS, temp_source, sourcelru, lrutype)

            exist = False
            wire = ""

			## CHECK IF THE LRU IS IN THE wires_dict
            print("...checking if lru is in the wires_dict: ", self.wires_dict, ".  Currently at lru:", sourcelru)
            for key, value in self.wires_dict.items():
                if key == sourcelru:
                    print(key, " found in: ", self.wires_dict, ".  Use the associated value of wire.")

                    exist = True
                    wire = value
                    break

			## LRU IS IN THE wires_dict, SET destlru TO THE WIRE
            if exist == True:
				## SET temp_dest
                destlru = wire
                lrutype = ""
                temp_dest = self.setConnectionInfo(PARAMS, temp_dest, destlru, lrutype, component="COMPONENT")
			## LRU IS NOT IN THE wires_dict, SET destlru TO A NEW WIRE NUMBER
            else:
				## SET temp_dest
                self.internal_counter = self.internal_counter + 1
                wire = self.internal_string + str(format(self.internal_counter, self.internal_format))
                destlru = wire
                lrutype = ""
                temp_dest = self.setConnectionInfo(PARAMS, temp_dest, destlru, lrutype, component="COMPONENT")

            temp_pin.SOURCE = temp_source
            temp_pin.DEST = temp_dest

            temp_pin_reverse.SOURCE = temp_dest
            temp_pin_reverse.DEST = temp_source

            print("...adding Source:", temp_source.lru, "Destination:", temp_dest.lru)
            PARAMS.pinInterconnectionList.append(temp_pin)
            PARAMS.pinInterconnectionList.append(temp_pin_reverse)

			## SET CONTROL, IF ANY
            self.setControl(PARAMS, PIN)

            self.wires_dict[sourcelru] = wire
            for connection in PIN.internal_list:
                lru = connection.conn + "_" + connection.pin
                self.wires_dict[lru] = wire

		## IF COMPONENTS IS NOT EMPTY
        else:
            print("...components is NOT empty")

			## HANDLE MULTIPLE COMPONENTS
            components = PIN.SOURCE.components
            component_array = components.split(",")
            for x in range(1, len(component_array)):
                self.setSourceToDestination(PARAMS, "COMPONENT", component_array[x - 1], component_array[x])
                # try: self.set_multiple_components(PARAMS, component_array[x], component_array[x+1])
                # except: doing = None
            print("...completed multiple components (if any)")


            temp_pin = CC.Pin_Interconnection()
            temp_pin_reverse = CC.Pin_Interconnection()
            temp_source = CC.Pin()
            temp_dest = CC.Pin()

			## SET temp_source
            sourcelru = PIN.SOURCE.conn + "_" + PIN.SOURCE.pin
            lrutype = PIN.SOURCE.type
            temp_source = self.setConnectionInfo(PARAMS, temp_source, sourcelru, lrutype)
            
			## SET temp_dest
            destlru = component_array[0]
            lrutype = ""
            temp_dest = self.setConnectionInfo(PARAMS, temp_dest, destlru, lrutype, component="COMPONENT")

            temp_pin.SOURCE = temp_source
            temp_pin.DEST = temp_dest

            temp_pin_reverse.SOURCE = temp_dest
            temp_pin_reverse.DEST = temp_source

            print("...adding Source:", temp_source.lru, "Destination:", temp_dest.lru)
            PARAMS.pinInterconnectionList.append(temp_pin)
            PARAMS.pinInterconnectionList.append(temp_pin_reverse)
            
			## SET CONTROL, IF ANY
            self.setControl(PARAMS, PIN)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def setSourceToDestination(self, PARAMS, component, component1, component2):
        print("...multiple", str(component) ,"found")
        temp_pin = CC.Pin_Interconnection()
        temp_pin_reverse = CC.Pin_Interconnection()
        temp_source = CC.Pin()
        temp_dest = CC.Pin()

		## SET temp_source
        sourcelru = component1
        lrutype = ""
        temp_source = self.setConnectionInfo(PARAMS, temp_source, sourcelru, lrutype, component=component)
        
		## SET temp_dest
        destlru = component2
        lrutype = ""
        temp_dest = self.setConnectionInfo(PARAMS, temp_dest, destlru, lrutype, component=component)

        temp_pin.SOURCE = temp_source
        temp_pin.DEST = temp_dest

        temp_pin_reverse.SOURCE = temp_dest
        temp_pin_reverse.DEST = temp_source

        print("...adding Source:", temp_source.lru, "Destination:", temp_dest.lru)
        PARAMS.pinInterconnectionList.append(temp_pin)
        PARAMS.pinInterconnectionList.append(temp_pin_reverse)

		## SET CONTROL, IF ANY
        #self.set_control(PARAMS, pin)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def setControl(self, PARAMS, PIN):
        print("...setting control")

        if PIN.SOURCE.control == "" or PIN.SOURCE.control == None:
            ## DONT DO ANYTHING
            print("...no controls found")
        else:
            print("...a control has been found")

			## HANDLE MULTIPLE CONTROLS
            controls = PIN.SOURCE.control
            controls_array = controls.split(",")
            for x in range(1, len(controls_array)):
                self.setSourceToDestination(PARAMS, "CONTROL", controls_array[x - 1], controls_array[x])
                # try: self.set_multiple_components(PARAMS, component_array[x], component_array[x+1])
                # except: doing = None
            print("...completed multiple controls (if any)")

			## WILL ERROR IF COMPONENT IS THE SAME AS CONTROL
            temp_pin = CC.Pin_Interconnection()
            temp_pin_reverse = CC.Pin_Interconnection()
            temp_source = CC.Pin()
            temp_dest = CC.Pin()

			## SET temp_source
            sourcelru = controls_array[0]
            lrutype = ""
            temp_source = self.setConnectionInfo(PARAMS, temp_source, sourcelru, lrutype, component="CONTROL")

			## WHEN MULTIPLE COMPONENTS, ONLY CONNECT TO FIRST ELEMENT
            components = PIN.SOURCE.components
            component_array = components.split(",")

			## SET temp_dest
            destlru = component_array[0]
            lrutype = ""
            temp_dest = self.setConnectionInfo(PARAMS, temp_dest, destlru, lrutype, component="COMPONENT")

            temp_pin.SOURCE = temp_source
            temp_pin.DEST = temp_dest

            temp_pin_reverse.SOURCE = temp_dest
            temp_pin_reverse.DEST = temp_source

            print("...adding Source:", temp_source.lru, "Destination:", temp_dest.lru )
            PARAMS.pinInterconnectionList.append(temp_pin)
            PARAMS.pinInterconnectionList.append(temp_pin_reverse)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def setConnectionInfo(self, PARAMS, temp_connection, lru, lrutype, component=""):
        print("...setting connection_info")
        # temp_source.lru = pin.SOURCE.conn + "_" + pin.SOURCE.pin
        # temp_source.lru_label = copy.deepcopy(temp_source.lru)
        # temp_source.conn = ""
        # temp_source.pin = ""
        # temp_source.type = pin.SOURCE.type
        # temp_source.lruType = PARAMS.lruTypeDict["INTERNAL"]

        if lrutype == None:
            lrutype = ""

        temp_connection.lru = lru
        temp_connection.lru_label = lru
        self.conn_counter = self.conn_counter + 1
        temp_connection.conn = "_" + str(format(self.conn_counter, self.conn_format))
        temp_connection.pin = ""
        temp_connection.components = component

        if component == "":
            temp_connection.type = lrutype
            temp_connection.lruType = PARAMS.lruTypeDict[lrutype]
        else:
            temp_connection.type = lrutype
            temp_connection.lruType = PARAMS.lruTypeDict[component]

        return temp_connection

    ####################################################################################################################
    ##
    ####################################################################################################################
    def getAdditionalInfo(self, PARAMS, LRU):
        print("...getting additional info (internal)")

        print("...gather PINS info")
        pins_info = etree.Element('PINSInfo')

        LRUs = copy.deepcopy(LRU)

		## ITS A DUPLICATE LRU
        if PARAMS.delimeterDuplicatingLRU in LRUs.source_lru:
			## REMOVE DATA AFTER DELIMETER
            end_here = LRU.source_lru.find(PARAMS.delimeterDuplicatingLRU)
            LRUs.source_lru = LRUs.source_lru[:end_here]

            for LRU2 in self.lrusExpandedList:
                if LRU2.source_lru == LRUs.source_lru:
                    LRUs = copy.deepcopy(LRU2)

        for PINS in LRUs.pin_interconnections_list:

            pin_info = etree.Element('PIN')
            pin_info.attrib["pin"] = PINS.SOURCE.lru + " :: " + PINS.SOURCE.conn + " :: " + PINS.SOURCE.pin
            pin_info.attrib["description"] = PINS.SOURCE.description
            pin_info.attrib["components"] = PINS.SOURCE.components
            pin_info.attrib["type"] = PINS.SOURCE.type
            pin_info.attrib["control"] = PINS.SOURCE.control

            pins_info.insert(0,pin_info)

        print("...PINSInfo:", etree.tostring(pins_info))

        print("...gather IMAGES info")
        images_info = etree.Element('ImagesInfo')
        for elem in self.xml_info:
            if elem.tag == "XMLInfo":
                for lru in elem:
                    if LRU.source_lru == lru.attrib["name"]:
                        images_string = lru.attrib["Images"]
                        if images_string == "":
							## DONT DO ANYTHING
                            doing = None
                        else:
                            images_array = images_string.split(",")

                            for items in images_array:
                                image_info = etree.Element('Image')
                                image_info.attrib["Image"] = items

                                images_info.insert(0,image_info)

        print("...IMAGESInfo:", etree.tostring(images_info))

		## INSERT TO ADDITIONAL INFO
        self.additionalInfo.insert(0, pins_info)
        self.additionalInfo.insert(0, images_info)


    ####################################################################################################################
    ##
    ####################################################################################################################
    def drawInterconnection(self, PARAMS, LRU):
        print("------------------------------Starting PREP_OUTLINE------------------------------")
        # if PARAMS.settings.attrib["draw_inserting"] == "true":
        #     PREP_OUTLINE = PREPINSERTING.Prep_Inserting(PARAMS)
        # elif PARAMS.settings.attrib["draw_tree"] == "true":
        #     PREP_OUTLINE = PREPTREE.Prep_Tree(PARAMS)
        # else:
        #     PREP_OUTLINE = PREP.Prep_Outline(PARAMS)
        #     PREP_OUTLINE.prep_outline(PARAMS)
        PREP_OUTLINE = PREPINSERTING.Prep_Inserting(PARAMS,self.settings)

        ## GATHER ADDITIONAL INFO
        self.getAdditionalInfo(PARAMS, LRU)

        print("------------------------------Starting DRAW_OUTLINE------------------------------")
        # if PARAMS.settings.attrib["draw_inserting"] == "true":
        #     ## ALWAYS GET INTERNAL TO REORDER PATHS FALSE
        #     PARAMS.settings.attrib["reorder_paths"] = "false"
        #     DRAW_TREE = DRAWINSERTING.Draw_Inserting(PARAMS)
        # elif PARAMS.settings.attrib["draw_tree"] == "true":
        #     DRAW_TREE = DRAWTREE.Draw_Tree(PARAMS)
        # else:
        #     DRAW_OUTLINE = DRAW.Draw_Outline(PARAMS)
        #     DRAW_OUTLINE.drawOutline(PARAMS)
        self.settings["GridView"]["reorder_paths"] = "False"
        DRAW_TREE = DRAWINSERTING.Draw_Inserting(PARAMS,self.settings)

        print("------------------------------Starting set endpoint loc in PREP_OUTLINE------------------------------")
        PREP_OUTLINE.setEndpointLoc(PARAMS)

        print("------------------------------Starting HTML_FILE------------------------------")
        HTML_FILE = HTML.Generator_html(PARAMS, LRU.source_lru, self.additionalInfo, delimeterDuplicatingLRU=PARAMS.delimeterDuplicatingLRU)

        print("------------------------------Starting JS_FILE------------------------------")
        JS_FILE = JS.Generator_js(PARAMS, LRU.source_lru, self.settings,delimeterDuplicatingLRU=PARAMS.delimeterDuplicatingLRU)

#######################################################################################################################
## MAIN
#######################################################################################################################
if __name__ == '__main__':
    IGL = Interconnection_Generator_Lrus()

