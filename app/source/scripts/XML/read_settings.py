import xml.etree.ElementTree as ET
from collections import OrderedDict

class Settings():
    def __init__(self):

        self.settings = OrderedDict()                                    ## GENERATE A DICTIONARY OF SETTINGS

        self.read_settings()
        self.populate_settings()

    def read_settings(self):
        ## PARSE THE settings.xml
        self.tree = ET.parse('../files/settings/settings.xml')
        self.root = self.tree.getroot()

    def populate_settings(self):
        for child in self.root:
            attribs = OrderedDict()

            for k, v in child.attrib.items():
                attribs[k] = v

            self.settings[child.tag] = attribs

