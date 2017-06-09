import xml.etree.ElementTree as ET
import logging
import datetime
import csv
import os
import codecs
from lxml import etree
import numpy
import copy
import math
import GenerateJS as JS
import GenerateHTML as HTML
import DrawOutline as DRAW
import DrawTree as DRAWTREE
import DrawInserting as DRAWINSERTING
import Common as CC
import PrepOutline as PREP
import PrepTree as PREPTREE
import PrepInserting as PREPINSERTING
import Interconnections_lrus as INTER_LRUS
import multiprocess_handler_class as MPH
from collections import OrderedDict
import sys
sys.path.append("../Log")
import myLog


####################################################################################################################
#####
####################################################################################################################
def multiProcessInterconnections(q, _LRU, _additionalInfo,
                                 _delimeterDuplicatingLRU, _lrusExpandedList, _settings):
    ##### q is for queue but it is not used

    #####convert xml string back to xml.  For some reason, multi thread function cannot take an XML element
    _additionalInfo = etree.fromstring(_additionalInfo)

    GIO_LRUS = INTER_LRUS.Interconnection_Generator_Lrus(_LRU, _additionalInfo,
                        _delimeterDuplicatingLRU,_lrusExpandedList,_settings)

####################################################################################################################
#####
####################################################################################################################


class Interconnection_Generator():
    @myLog.catch_wrapper
    def __init__(self,all,pins,adapters,main_root,settings):
        self.all = all
        self.pins = pins
        self.adapters = adapters
        self.main_root = main_root
        self.settings = settings

        #####list of all connections found
        self.found_LRU_list = []
        self.connections_executed_trace_ext_list = []
        self.OrigLRU = None
        self.path = ""
        self.additionalInfo = etree.Element('AdditionalInfo')

        self.html_js_filename = "Interconnection"

        #####global params
        self.PARAMS = CC.Params()

        #####methods
        self.start(self.PARAMS)



    ####################################################################################################################
    #####Main
    ####################################################################################################################
    def start(self, PARAMS):
        #####update size of matrix
        #PARAMS.updateSizeOfPositionMatrix(int(PARAMS.settings.attrib["matrix_size"]))
        #PARAMS.update_csv_matrix(int(PARAMS.settings.attrib["matrix_size"]))

        #####trace connections
        #####Gather connectionList and pins_interconnections_list
        self.startTracing(PARAMS)

        #####write to csv (will be deleted in the future)
        #self.write_csv()

        #print(self.csvMatrix)
        #print(self.connectionList)
        #print(self.pinInterconnectionList)

        self.drawInterconnection(self.PARAMS)


    ####################################################################################################################
    #####Read what to trace from the settings.xml
    ####################################################################################################################
    def startTracing(self, PARAMS):

        print("...Starting start_trace")

        if self.all == True:
            self.TracingAll()
        else:
            for trace in self.pins:
                SOURCE_CONN = CC.Pin()
                SOURCE_CONN.lru = trace[0]
                SOURCE_CONN.lru_label = copy.copy(trace[0])
                SOURCE_CONN.conn = trace[1]
                SOURCE_CONN.pin = trace[2]

                PARAMS.lruToBeTraced = SOURCE_CONN.lru
                self.trace(SOURCE_CONN)


    ####################################################################################################################
    #####
    ####################################################################################################################
    def TracingAll(self):
        print("...Runnning trace all")

        for lrus in self.main_root:
            for CONNS in lrus:
                for PINS in CONNS:
                    SOURCE_CONN = CC.Pin()
                    SOURCE_CONN.lru = lrus.attrib['name']
                    SOURCE_CONN.lru_label = lrus.attrib['name']
                    SOURCE_CONN.conn = CONNS.tag

                    if type(PINS) == etree._Comment:
                        teat = None
                    else:
                        SOURCE_CONN.pin = PINS.tag
                        self.OrigLRU = SOURCE_CONN.lru
                        self.trace(SOURCE_CONN)

    ####################################################################################################################
    #####External connections, then internal
    #####parameters are passed by reference in python
    ####################################################################################################################
    def trace(self, SOURCE_CONN):
        print("...Running trace().  At PIN: ", SOURCE_CONN.lru, SOURCE_CONN.conn, SOURCE_CONN.pin)

        current_LRU = SOURCE_CONN.lru

        #####See if the LRU exist in found_LRU_list
        if SOURCE_CONN.lru in self.found_LRU_list:
            doing = None
        else:
            self.found_LRU_list.append(SOURCE_CONN.lru)
            #self.PARAMS.csv_col_dict[SOURCE_CONN.lru] = self.PARAMS.csv_col

        #####call trace_ext
        DEST_CONN, internal_dest_conn_list = self.traceExternal(SOURCE_CONN)
        TEMP_PIN_INTERCONNECTION = CC.Pin_Interconnection()
        TEMP_PIN_INTERCONNECTION.setSource(SOURCE_CONN)
        TEMP_PIN_INTERCONNECTION.setDest(DEST_CONN)
        TEMP_PIN_INTERCONNECTION.setInternalList(internal_dest_conn_list)
        #####append pin_interconnection to the main list
        self.PARAMS.pinInterconnectionList.append(TEMP_PIN_INTERCONNECTION)
        #####append SOURCE_CONN.string() to connectionList
        self.PARAMS.connectionList.append(SOURCE_CONN.getString())
        print("Source: ", SOURCE_CONN.getString(), "\t Destination: ", DEST_CONN.lru, DEST_CONN.conn, DEST_CONN.pin)

        #####append SOURCE_CONN to connections_executed_trace_ext_list on
        self.connections_executed_trace_ext_list.append(SOURCE_CONN.getString())

        #####save SOURCE_CONN to csvMatrix
        #self.PARAMS.csvMatrix[self.PARAMS.csv_row][self.PARAMS.csv_col] = SOURCE_CONN

        #####increase col
        #self.PARAMS.csv_col = self.PARAMS.csv_col + 1

        #####check if des_conn has been executed with trace_ext
        if DEST_CONN.getString() in self.connections_executed_trace_ext_list:
            #####DEST_CONN has been executed using trace_ext, dont do anything
            doing = None
        else:
            self.trace(DEST_CONN)

        #####Go through internal connections found previously
        if internal_dest_conn_list != None:
            items_num = 0
            for items in internal_dest_conn_list:

                items_num = items_num + 1
                #####check if items has been executed with trace_ext
                if items.getString() in self.connections_executed_trace_ext_list:
                    #####found already
                    if items_num > 1 or current_LRU == self.OrigLRU:
                        #self.PARAMS.csv_col = self.PARAMS.csv_col_dict[SOURCE_CONN.lru] + 1
                        doing = None
                else:
                    if items_num > 1 or current_LRU == self.OrigLRU:
                        #self.PARAMS.csv_row = self.PARAMS.csv_row + 1
                        #self.PARAMS.csv_col = self.PARAMS.csv_col_dict[SOURCE_CONN.lru] + 1
                        doing = None

                    self.trace(items)

    ####################################################################################################################
    #####Get external connections and other info such as LRUType
    ####################################################################################################################
    def traceExternal(self, SOURCE_CONN):
        print("...traceExternal")
        DEST_CONN = CC.Pin()
        internal_dest_conn_list = None

        #####search in database
        for lrus in self.main_root:

            if lrus.attrib['name'] == SOURCE_CONN.lru:
                #####get if its CABLE, LRU, or ADAPTER
                SOURCE_CONN.lruType = lrus.tag
                #####go through each connections
                for connector in lrus:
                    if connector.tag == SOURCE_CONN.conn:

                        DEST_CONN.lru = connector.attrib['ExternalConnLRU']
                        DEST_CONN.lru_label = connector.attrib['ExternalConnLRU']
                        DEST_CONN.conn = connector.attrib['ExternalConnConnector']
                        DEST_CONN.pin = SOURCE_CONN.setConnectedPin(self.main_root)

                        ####LRU may/may not have ExternalConnLRU or ExternalConnConnector
                        if DEST_CONN.lru == "":
                            ####If so, need to find a cable that connects to SOURCE_CONN
                            DEST_CONN = self.getConnectedCables(SOURCE_CONN)

                        internal_dest_conn_list = self.traceInternal(connector, SOURCE_CONN)

        return DEST_CONN, internal_dest_conn_list

    ####################################################################################################################
    #####If LRU doesnt have ExternalConnLRU, get cables that connect to that LRU
    ####################################################################################################################
    def getConnectedCables(self, SOURCE_CONN):

        print("No ExternalConnLRU")

        DEST_CONN = CC.Pin()
        #####search in database
        for lrus in self.main_root:
            for conn in lrus:
                #for name, value in conn.items():
                    #print(name,value)

                attribs_conn = conn.attrib
                try:
                    if attribs_conn["ExternalConnLRU"] == SOURCE_CONN.lru and attribs_conn["ExternalConnConnector"] == SOURCE_CONN.conn:

                        attribs_LRUS = lrus.attrib
                        DEST_CONN.lru = attribs_LRUS['name']
                        DEST_CONN.lru_label = attribs_LRUS['name']
                        DEST_CONN.conn = conn.tag
                        DEST_CONN.pin = SOURCE_CONN.pin

                except:
                    doing = None

        return DEST_CONN

    ####################################################################################################################
    #####Get internal connections and other info such as description, components, type, controls
    ####################################################################################################################
    def traceInternal(self, connector, SOURCE_CONN):
        internal_dest_conn_list = []

        #####go through each pin
        for pins in connector:
            if pins.tag == SOURCE_CONN.pin:
                #####Gather other information on that pin
                SOURCE_CONN.description = pins.attrib['description']
                SOURCE_CONN.components = pins.attrib['components']
                SOURCE_CONN.type = pins.attrib['type']
                SOURCE_CONN.control = pins.attrib['control']

                #####may have commas
                internalconns_string = pins.attrib['InternalConns']

                if internalconns_string != "":
                    internalconns_array = internalconns_string.split(",")

                    #####create an array of connections base on number of items in internalconns_array
                    for item in internalconns_array:
                        INTERNAL_CONN = CC.Pin()

                        item_array = item.split(":")
                        INTERNAL_CONN.lru = SOURCE_CONN.lru
                        INTERNAL_CONN.lru_label = SOURCE_CONN.lru
                        INTERNAL_CONN.conn = item_array[0]
                        INTERNAL_CONN.pin = item_array[1]
                        internal_dest_conn_list.append(INTERNAL_CONN)
                    
        return internal_dest_conn_list

    ####################################################################################################################
    #####Write out to csv
    ####################################################################################################################
    def writeCsv(self):

        for y in range(0, self.PARAMS.maxrow):
            list = []
            for x in range(0, self.PARAMS.maxcol):
                if x % 2 == 0:
                    #####Even, write connection LRU_Conn_Pin
                    try:
                        list.append("description:" + self.PARAMS.csvMatrix[y][x].description + "\n" +
                                    "type:" + self.PARAMS.csvMatrix[y][x].type + "\n" +
                                    "components:" + self.PARAMS.csvMatrix[y][x].components + "\n" +
                                    "control:" + self.PARAMS.csvMatrix[y][x].control + "\n" +
                                    self.PARAMS.csvMatrix[y][x].getString())
                    except:
                        #####No object
                        list.append(None)
                else:
                    #####Odd, write connection Pin_Conn_LRU
                    try:
                        list.append("description:" + self.PARAMS.csvMatrix[y][x].description + "\n" +
                                    "type:" + self.PARAMS.csvMatrix[y][x].type + "\n" +
                                    "components:" + self.PARAMS.csvMatrix[y][x].components + "\n" +
                                    "control:" + self.PARAMS.csvMatrix[y][x].control + "\n" +
                                    self.PARAMS.csvMatrix[y][x].getStringLeft())
                    except:
                        #####No object
                        list.append(None)

            self.PARAMS.csvfile.writerow(list)

        self.PARAMS.csv.close()

    ####################################################################################################################
    #####
    ####################################################################################################################
    def getAdditionalInfos(self, PARAMS):
        print("...getting additional info")

        print("...gather XML info")
        xml_info = etree.Element('XMLInfo')
        for elem in self.main_root:
            for LRUs in PARAMS.LRUInterconnectionList:
                LRU = copy.deepcopy(LRUs)

                if PARAMS.delimeterDuplicatingLRU in LRU.source_lru:
                    #####remove data after delimeter
                    end_here = LRU.source_lru.find(PARAMS.delimeterDuplicatingLRU)
                    LRU.source_lru = LRU.source_lru[:end_here]

                #####found element matching the LRU
                if LRU.source_lru == elem.attrib["name"]:
                    info = copy.deepcopy(elem)
                    for child in info:
                        info.remove(child)

                    xml_info.insert(0,info)
                    break

        print("...XMLInfo:", etree.tostring(xml_info))

        print("...gather Connections info")
        connections_info = etree.Element('ConnectionsInfo')
        lru_covered_list = []
        for LRU in PARAMS.LRUInterconnectionList:
            lru_info = etree.Element('LRU')

            LRUs = copy.deepcopy(LRU)

            if PARAMS.delimeterDuplicatingLRU in LRUs.source_lru:
                #####remove data after delimeter
                end_here = LRUs.source_lru.find(PARAMS.delimeterDuplicatingLRU)
                LRUs.source_lru = LRUs.source_lru[:end_here]

                for lru in PARAMS.lrusExpandedList:
                    if lru.source_lru == LRUs.source_lru:
                        LRUs = copy.deepcopy(lru)

            lru_info.attrib["name"] = LRUs.source_lru


            if LRUs.source_lru in lru_covered_list:
                #####already taken care of before
                doing = None
            else:
                #####add to the list
                lru_covered_list.append(LRUs.source_lru)

                for pins in LRUs.pin_interconnections_list:
                    pin_info = etree.Element('PIN')
                    pin_info.attrib["SRC"] = pins.SOURCE.lru + " :: " +  pins.SOURCE.conn + " :: " + pins.SOURCE.pin
                    pin_info.attrib["DEST"] = pins.DEST.lru + " :: " + pins.DEST.conn + " :: " + pins.DEST.pin
                    lru_info.append(pin_info)

                connections_info.append(lru_info)

        print("...ConnectionsInfo:", etree.tostring(connections_info))


        #####insert to additional info
        self.additionalInfo.insert(0,connections_info)
        self.additionalInfo.insert(0,xml_info)

    ####################################################################################################################
    #####
    ####################################################################################################################
    def deleteLRUwithDelimeterfromLRUInterconnectionList(self, PARAMS):
        print("...deleteLRUwithDelimeterfromLRUInterconnectionList")
        newLRUInterconnectionList = []

        print(len(PARAMS.LRUInterconnectionList))
        for LRU in PARAMS.LRUInterconnectionList:
            print(LRU.source_lru)

        print("PARAMS.lrusExpandedList:")
        for LRUs in PARAMS.lrusExpandedList:
            print(LRUs.source_lru)
            PARAMS.LRUInterconnectionList.append(LRUs)

        for LRU in PARAMS.LRUInterconnectionList:
            if PARAMS.delimeterDuplicatingLRU in LRU.source_lru:
                doing = None
            else:
                lruTypeSame = False
                for PIN in LRU.pin_interconnections_list:
                    if "SAME" in PIN.SOURCE.lruType:
                        lruTypeSame = True
                        break

                if lruTypeSame == False:
                    newLRUInterconnectionList.append(LRU)

        print("newLRUInterconnectionList:")
        for lru in newLRUInterconnectionList:
            print(lru.source_lru)

        PARAMS.LRUInterconnectionList = newLRUInterconnectionList

    ####################################################################################################################
    #####
    ####################################################################################################################
    def drawInterconnection(self, PARAMS):

        print("------------------------------Starting PREP_OUTLINE------------------------------")
        # if PARAMS.settings.attrib["draw_inserting"] == "true":
        #     PREP_OUTLINE = PREPINSERTING.Prep_Inserting(PARAMS)
        # elif PARAMS.settings.attrib["draw_tree"] == "true":
        #     PREP_OUTLINE = PREPTREE.Prep_Tree(PARAMS)
        # else:
        #     PREP_OUTLINE = PREP.Prep_Outline(PARAMS)
        #     PREP_OUTLINE.prep_outline(PARAMS)
        PREP_OUTLINE = PREPINSERTING.Prep_Inserting(PARAMS,self.settings)

        #####gather additional info
        self.getAdditionalInfos(PARAMS)

        print("------------------------------Starting DRAW_OUTLINE------------------------------")
        # if PARAMS.settings.attrib["draw_inserting"] == "true":
        #     DRAW_TREE = DRAWINSERTING.Draw_Inserting(PARAMS)
        # elif PARAMS.settings.attrib["draw_tree"] == "true":
        #     DRAW_TREE = DRAWTREE.Draw_Tree(PARAMS)
        # else:
        #     DRAW_OUTLINE = DRAW.Draw_Outline(PARAMS)
        #     DRAW_OUTLINE.drawOutline(PARAMS)
        DRAW_TREE = DRAWINSERTING.Draw_Inserting(PARAMS,self.settings)


        print("------------------------------Starting set endpoint loc in PREP_OUTLINE------------------------------")
        PREP_OUTLINE.setEndpointLoc(PARAMS)


        print("------------------------------Starting HTML_FILE------------------------------")
        if self.settings["GridView"]["get_internal"] == "False":
            getinternal = False
        else:
            getinternal = True

        HTML_FILE = HTML.Generator_html(PARAMS, self.html_js_filename, self.additionalInfo, get_internal=getinternal)


        print("------------------------------Starting JS_FILE------------------------------")
        JS_FILE = JS.Generator_js(PARAMS, self.html_js_filename, self.settings)

        if self.settings["GridView"]["get_internal"] == "False":
            doing = None
        else:
            self.deleteLRUwithDelimeterfromLRUInterconnectionList(PARAMS)
            print("------------------------------Generate interconnection for all LRUs------------------------------")
            if self.settings["GridView"]["multi_process"] == "True":
                #####create Process_handler object
                ph = MPH.Process_handler()

                #####Gather all jobs to be ran
                for LRU in PARAMS.LRUInterconnectionList:
                    q = None

                    #####deep copying variable just in case
                    #####XML element are converted to strings, or else it errors
                    _LRU = copy.deepcopy(LRU)
                    _additionalInfo = copy.deepcopy(self.additionalInfo)
                    _additionalInfo = etree.tostring(_additionalInfo)
                    _delimeterDuplicatingLRU = copy.deepcopy(PARAMS.delimeterDuplicatingLRU)
                    _lrusExpandedList = copy.deepcopy(PARAMS.lrusExpandedList)
                    _settings = copy.deepcopy(PARAMS.settings)

                    args_ = [_LRU, _additionalInfo,
                            _delimeterDuplicatingLRU,_lrusExpandedList,_settings]

                    ph.gather(multiProcessInterconnections, args_)

                #####Start the jobs
                num_processors = int(self.settings["GridView2"]["num_processes"])
                ph.run_all(num_processors, verbose=True)

                ####join all process to the main process
                for x in range(0, ph.get_num_cores()):
                    if ph.process_number[x].is_alive() == True:
                        ph.process_number[x].join()

            else:
                print("length of PARAMS.LRUInterconnectionList", len(PARAMS.LRUInterconnectionList))
                for LRU in PARAMS.LRUInterconnectionList:
                    GIO_LRUS = INTER_LRUS.Interconnection_Generator_Lrus(LRU, self.additionalInfo,
                                                                                     PARAMS.delimeterDuplicatingLRU,
                                                                                     PARAMS.lrusExpandedList,
                                                                                     self.settings)



#######################################################################################################################
#####MAIN
#######################################################################################################################
if __name__ == '__main__':
    GIO = Interconnection_Generator()

    ## TESTING ONLY
    # all = False
    # pins = [('VCDM1', 'J3', 'K')]
    # adapters = ['adapter1']
    #
    # tree = etree.parse('data.xml')
    # root = tree.getroot()
    #
    #
    #
    # settings = OrderedDict([('Color', OrderedDict(
    #     [('color_unknown', 'white'), ('color_control', 'orange'), ('color_input', 'green'), ('color_same', '#ffff80'),
    #      ('color_output', '#00FF00')])), ('GridView2', OrderedDict(
    #     [('max_num_connections', '4'), ('directory', 'TEST0/'), ('delay_time', '250'), ('num_processes', '20')])), (
    #                             'Shape', OrderedDict(
    #                                 [('shape_output', 'Dot'), ('shape_unknown', 'Dot'), ('shape_same', 'Rectangle'),
    #                                  ('shape_input', 'Dot'), ('shape_control', 'Dot')])), ('GridView', OrderedDict(
    #     [('copy_description_to_missing_xml', 'True'), ('delete_multiple_loops', 'True'), ('multi_process', 'False'),
    #      ('generate_missing_xml', 'True'), ('duplicateLRUasNeeded', 'True'),
    #      ('delete_path_list_loops_no_duplicate', 'False'), ('draw_one_at_a_time', 'True'), ('reorder_paths', 'True'),
    #      ('minimum_path_only', 'True'), ('more_random', 'True'), ('overlap_endpoints', 'True'),
    #      ('get_internal', 'True'), ('duplicateLRU', 'True')])), ('CSS', OrderedDict(
    #     [('lru_border_input_color', 'green'), ('lru_border_unknown_color', 'white'), ('lru_border_radius', '50px'),
    #      ('lru_border_swcontrol_same_color', '#ffff80'), ('background_color_internal', 'gray'),
    #      ('cable_border_radius', '75px'), ('background_color_lru', '#006600'), ('lru_border_px', '18px'),
    #      ('swcontrol_border_radius', '75px'), ('lru_border_component_same_color', '#ffff80'),
    #      ('lru_border_output_color', '#00FF00'), ('component_border_radius', '75px'), ('lru_border_color', 'black'),
    #      ('output_border_radius', '200px'), ('control_border_radius', '200px'), ('lru_border_control_color', 'orange'),
    #      ('lru_border_component_color', 'black'), ('lru_border_swcontrol_color', 'orange'),
    #      ('lru_border_same_color', '#ffff80'), ('background_color_cable', 'gray'), ('unknown_border_radius', '200px'),
    #      ('input_border_radius', '200px')])), ('Log', OrderedDict([('Log', 'debug')]))])
    # GIO = Interconnection_Generator(all, pins, adapters, root, settings)
