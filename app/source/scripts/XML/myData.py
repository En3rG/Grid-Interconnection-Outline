
import os
import sys
import datetime
from lxml import etree
import xml.etree.ElementTree as ET
import logging
from collections import OrderedDict
sys.path.append("../Log")
import myLog


####################################################################################################################
## Update self.root if it has adapters
####################################################################################################################
@myLog.catch_wrapper
def updateDataXML(adapterList,main_root):
    for adapterName in adapterList:
        for element in main_root:
            if element.tag == "ADAPTER" and element.attrib["name"] == adapterName:
                for connectedTo in element:
                    updateLRU1 = connectedTo.attrib["ExternalConnLRU"]
                    updateConn1 = connectedTo.attrib["ExternalConnConnector"]

                    for e in main_root:
                        if e.attrib['name'] == updateLRU1:
                            for child in e:
                                if child.tag == updateConn1:
                                    #####UPDATE LRU CONNECTION TO ADAPTER
                                    updateLRU2 = child.attrib["ExternalConnLRU"]
                                    updateConn2 = child.attrib["ExternalConnConnector"]
                                    child.attrib["ExternalConnLRU"] = adapterName
                                    child.attrib["ExternalConnConnector"] = connectedTo.tag
                                    print(updateLRU2, updateConn2)

                                    for e2 in main_root:
                                        if e2.attrib['name'] == updateLRU2:
                                            for conn in e2:
                                                if conn.tag == updateConn2:
                                                    conn.attrib["ExternalConnLRU"] = "__" + conn.attrib[
                                                        "ExternalConnLRU"]

                                                    #####REMOVE LRU2 CONNECTION, NO LONGER CONNECTING TO LRU1
                                                    #####REMOVING CAN CAUSE INTERNAL CONNECTIONS TO FAIL
                                                    # child.getparent().remove(child)

                                                    ####UPDATE TAG FROM ADAPTER TO LRU
                                                    # element.tag = "LRU"

@myLog.catch_wrapper
def getData(settings,directory_widget):
    class Data():
        def __init__(self,settings):
            self.settings = settings
            self.rootdir = "../files/data/"
            print(directory_widget)
            self.path = str(directory_widget.text())
            self.main_root = etree.Element('data')

        def getFiles(self):
            ## READ DIRECTORY
            listing = os.listdir(self.rootdir + self.path)

            for filename in listing:
                if os.path.isdir(os.path.join(self.path, filename)):
                    ## Its a directory
                    ## Not supporting sub directories currently
                    # read_dir(os.path.join(path, filename))
                    doing = None
                else:
                    start_file = datetime.datetime.now()
                    self.readFiles(filename)
                    end = datetime.datetime.now()
                    print("Read time: ", filename, end - start_file)

            return self.main_root


        def readFiles(self,filename):
            print("...Reading:", filename)

            #####parse the main xml
            logging.info("Parsing: %s", filename)
            #####to handle unique characters in attributes??
            # target_file = codecs.open(rootFiles + path + filename, mode="r", encoding='utf-8')
            # self.current_tree_lxml = ET.parse(target_file)
            self.current_tree_lxml = etree.parse(self.rootdir + self.path + filename)
            self.current_tree_ET = ET.parse(self.rootdir + self.path + filename)

            #####get the root
            logging.info("Get root of: %s", filename)
            self.current_root_lxml = self.current_tree_lxml.getroot()
            self.current_root_ET = self.current_tree_ET.getroot()

            self.validateXml(filename)

            #####append current_root_lxml to main_root
            self.main_root.append(self.current_root_lxml)

        def validateXml(self, filename):

            print("...Validating:", filename)

            unique_conn_list = []

            for conn in self.current_root_ET:
                #####get all pins
                for pins in conn:
                    isFound_before = False
                    current_list = []
                    current_pin = str(conn.tag) + ":" + str(pins.tag)
                    connection_string = pins.attrib['InternalConns']
                    connection_array = connection_string.split(",")

                    current_list.append(current_pin)
                    for internal_conn in connection_array:
                        current_list.append(internal_conn)

                    for temp_list in unique_conn_list:
                        #####see if that pin exist in the current temp_list
                        for pin in current_list:
                            if pin in temp_list:
                                isFound_before = True

                                #####if it exist, check all its connection
                                #####every pin in current_list should also be in temp_list
                                for internal_conn in current_list:
                                    if internal_conn in temp_list:
                                        #####goood
                                        doing = None
                                    else:
                                        #####Error
                                        logging.warning("Filename: %s, pin: %s no internal connection?", filename,
                                                        internal_conn)
                                        print("Warning: Filename:", filename, "pin: ", internal_conn,
                                              " no internal connection?")

                                #####also need to check that everything in templist is in current_list (other way around)
                                for internal_conn2 in temp_list:
                                    if internal_conn2 in current_list:
                                        #####goood
                                        doing = None
                                    else:
                                        #####Error
                                        logging.warning("Filename: %s, pin: %s no internal connection?", filename,
                                                        internal_conn2)
                                        print("Warning: Filename:", filename, "pin: ", internal_conn2,
                                              " no internal connection?")

                                if isFound_before == True:
                                    break

                    if isFound_before == False:
                        #####If not found, must be a unique connection
                        unique_conn_list.append(current_list)

        ####################################################################################################################
        ##### Delete XML files with __ IN FRONT, ADDED ON PREVIOUS RUNS
        ##### ALSO DELETED AUTO_GENERATED ONES
        ####################################################################################################################
        def deleteFilesWith(self):
            listing = os.listdir(self.rootdir + self.path)

            for filename in listing:
                if filename.startswith("__"):
                    os.remove(self.rootdir + self.path + filename)

                elif "auto_generated" in filename:
                    os.remove(self.rootdir + self.path + filename)

        ####################################################################################################################
        #####
        ####################################################################################################################
        def generateMissingXml(self, main_root):
            print("...Generating XML if XML does not exist at all (will not update existing XMLs)")
            self.removeComments()
            ext_lru_xml = self.generateExternalLruXml()

            for ext_lru in ext_lru_xml:
                #####remove _ in the beginning
                extlru = ext_lru.tag[1:]

                found = False
                for lru in self.main_root:
                    if lru.attrib["name"] == extlru:
                        #####xml exist
                        found = True
                        break

                if found == False:
                    print("...did NOT find XML, need to generate XML for", extlru)
                    self.generateXml(ext_lru_xml, extlru)

            ## Save the combined XML to data.xml
            ## All the XML that was parsed
            final_tree = etree.ElementTree(main_root)
            final_tree.write("../files/" + "data.xml", pretty_print=True)

        ####################################################################################################################
        #####
        ####################################################################################################################
        def removeComments(self):
            #####get all the comments in data.xml
            comments = self.main_root.xpath('//comment()')
            #####remove all comments
            for c in comments:
                p = c.getparent()
                p.remove(c)

        ####################################################################################################################
        #####
        ####################################################################################################################
        def generateExternalLruXml(self):
            print("...generate_external_lru_xml")
            #####go through main_root (all XMLs parsed)
            #####gather list of external LRUs
            external_lrus_xml = etree.Element('ExternalLRUs')

            for lru in self.main_root:

                ####SKIPPING ADAPTER??
                if lru.tag == "ADAPTER":
                    continue

                src_name = lru.attrib["name"]
                for connectors in lru:
                    src_conn = connectors.tag
                    exist = False
                    #####check if lru exist in external_lrus_xml
                    for ext_lru in external_lrus_xml:
                        if ext_lru.tag == "_" + connectors.attrib["ExternalConnLRU"]:
                            exist = True
                            connector_xml = etree.Element("_" + connectors.attrib["ExternalConnConnector"])
                            connector_xml.attrib["ExternalConnLRU"] = src_name
                            connector_xml.attrib["ExternalConnConnector"] = src_conn
                            for pins in connectors:
                                try:
                                    pin_xml = etree.Element("_" + pins.attrib["connectedPin"])
                                    pin_xml.attrib["connectedPin"] = str(pins.tag)
                                except:
                                    pin_xml = etree.Element("_" + pins.tag)
                                pin_xml.attrib["description"] = pins.attrib["description"]
                                connector_xml.append(pin_xml)
                                #####append to external_lrus_xml
                                ext_lru.append(connector_xml)
                            break

                    if exist == False:
                        #####lru doesnt exist yet, create new lru xml
                        lru_xml = etree.Element("_" + connectors.attrib["ExternalConnLRU"])
                        connector_xml = etree.Element("_" + connectors.attrib["ExternalConnConnector"])
                        connector_xml.attrib["ExternalConnLRU"] = src_name
                        connector_xml.attrib["ExternalConnConnector"] = src_conn
                        for pins in connectors:
                            try:
                                pin_xml = etree.Element("_" + pins.attrib["connectedPin"])
                                pin_xml.attrib["connectedPin"] = str(pins.tag)
                            except:
                                pin_xml = etree.Element("_" + pins.tag)
                            pin_xml.attrib["description"] = pins.attrib["description"]
                            connector_xml.append(pin_xml)

                        lru_xml.append(connector_xml)
                        external_lrus_xml.append(lru_xml)

            return external_lrus_xml

        ####################################################################################################################
        #####
        ####################################################################################################################
        def generateXml(self, ext_lru_xml, extlru):
            for lrus in ext_lru_xml:
                lru = lrus.tag[1:]

                if lru == extlru:
                    lru_xml = etree.Element("LRU")
                    lru_xml.attrib["name"] = lru
                    lru_xml.attrib["DrawingNo"] = "Auto Generated"
                    lru_xml.attrib["DrawingNomenclature"] = "Auto Generated"
                    lru_xml.attrib["DrawingRevision"] = ""
                    lru_xml.attrib["DrawingDate"] = ""
                    lru_xml.attrib["Images"] = ""

                    for connectors in lrus:
                        conn = connectors.tag[1:]
                        conn_xml = etree.Element(conn)
                        conn_xml.attrib["ExternalConnLRU"] = connectors.attrib["ExternalConnLRU"]
                        conn_xml.attrib["ExternalConnConnector"] = connectors.attrib["ExternalConnConnector"]

                        for pins in connectors:
                            pin = pins.tag[1:]
                            pin_xml = etree.Element(pin)
                            pin_xml.attrib["InternalConns"] = ""
                            if self.settings["GridView"]["copy_description_to_missing_xml"] == "True":
                                pin_xml.attrib["description"] = pins.attrib["description"]
                            else:
                                pin_xml.attrib["description"] = ""
                            pin_xml.attrib["components"] = ""
                            pin_xml.attrib["type"] = ""
                            pin_xml.attrib["control"] = ""
                            try:
                                pin_xml.attrib["connectedPin"] = pins.attrib["connectedPin"]
                            except:
                                doing = None
                            conn_xml.append(pin_xml)
                        lru_xml.append(conn_xml)

                    self.main_root.append(lru_xml)

                    #####Save the XML, have pretty print ON
                    final_tree = etree.ElementTree(lru_xml)
                    final_tree.write(self.rootdir + self.path + lru + "_auto_generated.xml", pretty_print=True)
                    print("...auto generated:", etree.tostring(lru_xml))




    D = Data(settings)
    ## GET/READ FILES
    main_root = D.getFiles()

    ## DELETE XMLS WITH __ IN FRONT AND AUTO_GENERATED
    D.deleteFilesWith()

    if settings["GridView"]["generate_missing_xml"] == "True":
        D.generateMissingXml(main_root)

    return main_root, D

