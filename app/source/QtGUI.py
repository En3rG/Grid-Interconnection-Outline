
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication,QWidget,QPushButton,QAction, \
                            QTabWidget,QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, \
                            QFrame,QSplitter, QTreeWidget, QTreeWidgetItem, QGroupBox, QCheckBox, QStatusBar
import sys
sys.path.append("./scripts/Log")
import myLog
sys.path.append("./scripts/XML")
import read_settings
import myData
from collections import OrderedDict
sys.path.append("./scripts/Output")
import myOutput
sys.path.append("./scripts/UpdateOldcode")
import Interconnections2
import logging
from lxml import etree
import threading


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = read_settings.Settings()
        self.widgetObjs = self.init_widgetObjs()

        ## MAIN WINDOW SETTINGS
        self.title = 'Grid Interconnection Outline'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tree_pins = QTreeWidget()
        self.tree_adapters = QTreeWidget()
        self.tree_pins.setHeaderLabels(["Availabe Pins"])
        self.tree_adapters.setHeaderLabels(["Availabe Adapters"])
        self.tabsWidget = TabsWidget(self,self.widgetObjs,self.settings.settings)               ## CREATE TAB WIDGETS
        self.setCentralWidget(self.tabsWidget)
        self.init_Toolbar()
        self.statusBar()                                                                        ## RETRIEVE STATUS BAR
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)                                                       ## ACTIVATE STATUS BAR
        self.show()

    def load_xml(self):
        myLog.initLogs(self.settings.settings['Log']['Log'])
        self.main_root, self.DATA = myData.getData(self.settings.settings,self.directory)
        self.getTree()

    def getTree(self):
        ## NEED TO REMOVE CURRENT TREE, SINCE IT WILL APPEND BELOW
        root = self.tree_pins.invisibleRootItem()
        numchild = root.childCount()
        for i in range(numchild-1,-1,-1):
            self.tree_pins.takeTopLevelItem(i)

        root2 = self.tree_adapters.invisibleRootItem()
        numchild2 = root2.childCount()
        for i in range(numchild2 - 1, -1, -1):
            self.tree_adapters.takeTopLevelItem(i)

        ## APPENDS TO TREE
        for i,lru in enumerate(self.main_root):
            if lru.tag == "ADAPTER":
                parent = QTreeWidgetItem(self.tree_adapters)
                parent.setText(0, lru.attrib["name"])
                parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                parent.setCheckState(0, Qt.Unchecked)

            else:
                parent = QTreeWidgetItem(self.tree_pins)
                parent.setText(0, lru.attrib["name"])
                parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

                for conn in lru:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                    child.setText(0, conn.tag)
                    child.setCheckState(0, Qt.Unchecked)

                    for pin in conn:
                        child2 = QTreeWidgetItem(child)
                        child2.setFlags(child2.flags() | Qt.ItemIsUserCheckable)
                        child2.setText(0, pin.tag)
                        child2.setCheckState(0, Qt.Unchecked)

    def init_Toolbar(self):
        readAction = QAction(QIcon('../files/assets/icons/load.png'), 'Read XMLs', self)                          ## PROVIDE ICON AND HOVER MESSAGE
        readAction.setStatusTip('Read all XML Data')
        readAction.triggered.connect(self.load_xml)
        #readAction.triggered.connect(lambda: myData.getData(self.settings.settings))        ## CANT PASS PARAMETERS TO FUNCTION CONNECT, USE LAMBDA
        toolbar = self.addToolBar('')
        toolbar.addAction(readAction)

    def init_widgetObjs(self):
        def getWhiteQLineEdit(text):
            whiteQLine = QLineEdit(text)
            whiteQLine.setStyleSheet("QLineEdit {background-color: white;}")
            return whiteQLine

        self.enum_log = {"debug": 0, "info": 1, "warning": 2, "error": 3}
        self.enum_shape = {"Dot": 0, "Rectangle": 1}

        widgetObjs = {}
        widgetObjs["CSS"] = OrderedDict()
        widgetObjs["Color"] = OrderedDict()
        widgetObjs["Shape"] = OrderedDict()
        widgetObjs["Log"] = OrderedDict()
        widgetObjs["GridView"] = OrderedDict()
        widgetObjs["GridView2"] = OrderedDict()

        ## FILL UP CSS widgetObjs
        for k,v in self.settings.settings['CSS'].items():
            widgetObjs["CSS"][k] = getWhiteQLineEdit(v)

        ## FILL UP COLOR widgetObjs
        for k,v in self.settings.settings['Color'].items():
            widgetObjs["Color"][k] = getWhiteQLineEdit(v)

        ## FILL UP SHAPE widgetObjs
        choices = ["Dot", "Rectangle"]
        for k,v in self.settings.settings['Shape'].items():
            widgetObjs["Shape"][k] = get_combo(choices, self.enum_shape[v])

        ## FILL UP LOG widgetObjs
        choices = ["debug", "info", "warning", "error"]
        for k, v in self.settings.settings['Log'].items():
            widgetObjs["Log"]['Log'] = get_combo(choices, self.enum_log[v])

        ## FILL UP GRIDVIEW
        for k, v in self.settings.settings["GridView"].items():
            widgetObjs["GridView"][k] = QCheckBox()
            if self.settings.settings["GridView"][k] == "True":
                widgetObjs["GridView"][k].setChecked(True)

        for k, v in self.settings.settings["GridView2"].items():
            if k == "directory":
                widgetObjs["GridView2"][k] = self.directory = getWhiteQLineEdit(v)
            else:
                widgetObjs["GridView2"][k] = getWhiteQLineEdit(v)

        return widgetObjs

class TabsWidget(QWidget):
    def __init__(self, app, widgetObjs,settings):
        super(QWidget, self).__init__(app)
        self.setStyleSheet("background-color:#DCDCDC;")                                     ## CHANGES BACKGROUND ON ALL TABS
        self.widgetObjs = widgetObjs
        self.settings = settings
        self.app = app
        self.layout = QVBoxLayout(self)                                                     ## INIT LAYOUT

        ## INITIALIZE TAB SCREEN
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        self.tabGrid = QWidget()
        self.tabTree = QWidget()
        self.tabCSS = QWidget()
        self.tabColor = QWidget()
        self.tabShape = QWidget()
        self.tabLog = QWidget()

        # ADD TABS TO TAB WIDGET
        self.tabs.addTab(self.tabGrid,"Grid View")
        self.tabs.addTab(self.tabTree,"Tree View")
        self.tabs.addTab(self.tabCSS, "CSS")
        self.tabs.addTab(self.tabColor, "Color")
        self.tabs.addTab(self.tabShape, "Shape")
        self.tabs.addTab(self.tabLog, "Log")

        ## INITIALIZE EACH TABS
        self.init_TabGrid()
        self.init_TabCSS()
        self.init_TabColor()
        self.init_TabShape()
        self.init_TabLog()

        # ADD TABS TO WIDGET
        self.layout.addWidget(self.tabs)                                                    ## ADD TAB WIDGET TO LAYOUT
        self.setLayout(self.layout)                                                         ## SET LAYOUT


    def init_TabGrid(self):
        def generate():
            self.app.statusBar.showMessage("Running...")
            all, pins, adapters = self.saveValues()
            myOutput.clean()
            myOutput.generateCss(self.settings)

            #####UPDATE self.main_root for ALL ADAPTERS in adaptersList
            myData.updateDataXML(adapters,self.app.main_root)
            self.app.DATA.generateMissingXml(self.app.main_root)

            GIO = Interconnections2.Interconnection_Generator(all, pins, adapters, self.app.main_root, self.settings)
            ## USE DECORATOR INSTEAD
            # try: GIO = Interconnections2.Interconnection_Generator(all,pins,adapters,self.app.main_root,self.settings)
            # except Exception as e:
            #     logging.error(str(e))
            #     print("Error:", str(e))

            self.app.statusBar.showMessage("Done!")
            myOutput.openChrome()


        def getTopLeft():
            topleft = QGroupBox("&Options2")
            topleft.setMinimumSize(50,50)
            vbox = QVBoxLayout()

            layouts = []
            for key, widget in self.widgetObjs["GridView2"].items():
                tempLayout = get_lbl_hbox(key, widget)
                layouts.append(tempLayout)
            for layout in layouts:
                vbox.addLayout(layout)
            topleft.setLayout(vbox)

            return topleft

        def getTopRight():
            topright = QGroupBox("&Options")
            vbox = QVBoxLayout()

            layouts = []
            for key, widget in self.widgetObjs["GridView"].items():
                tempLayout = get_lbl_hbox(key, widget)
                layouts.append(tempLayout)
            for layout in layouts:
                vbox.addLayout(layout)
            topright.setLayout(vbox)

            return topright

        def getBottom():
            bottom = QGroupBox("&Execute")
            button = QPushButton("&Generate Interconnection")
            button.clicked.connect(generate)
            vbox = QVBoxLayout()
            vbox.addWidget(button)
            vbox.addStretch(1)
            bottom.setLayout(vbox)

            return bottom

        self.tabGrid.layout = QHBoxLayout(self)
        self.tree_pins = self.app.tree_pins
        self.tree_adapters = self.app.tree_adapters
        topright = getTopRight()
        topleft = getTopLeft()
        bottom = getBottom()

        splitter0 = QSplitter(Qt.Vertical)
        splitter0.addWidget(self.tree_pins)
        splitter0.addWidget(self.tree_adapters)
        splitter0.addWidget(topleft)

        #####splitter1, horizontal
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(splitter0)
        splitter1.addWidget(topright)

        #####splitter2, vertical
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([500,50])

        self.tabGrid.layout.addWidget(splitter2)
        self.tabGrid.setLayout(self.tabGrid.layout)

    def init_TabCSS(self):
        self.tabCSS.layout = QVBoxLayout(self)
        self.tabCSS.layout.addStretch()
        self.tabCSS.layout.setDirection(3)

        layouts = []
        for key, widget in self.widgetObjs["CSS"].items():
            tempLayout = get_lbl_hbox(key,widget)
            layouts.append(tempLayout)
        for layout in layouts:
            self.tabCSS.layout.addLayout(layout)
        self.tabCSS.setLayout(self.tabCSS.layout)

    def init_TabColor(self):
        ## enum Direction { LeftToRight, RightToLeft, TopToBottom, BottomToTop, Down, Up }
        self.tabColor.layout = QVBoxLayout(self)
        self.tabColor.layout.addStretch()                                                   ## WITHOUT THIS, WILL SPACE OUT EVENLY DEPENDING ON THE WINDOW SIZE
        self.tabColor.layout.setDirection(3)                                                ## PLACES TOPTOBOTTOM

        layouts = []
        for key, widget in self.widgetObjs["Color"].items():
            tempLayout = get_lbl_hbox(key, widget)
            layouts.append(tempLayout)
        for layout in layouts:
            self.tabColor.layout.addLayout(layout)
        self.tabColor.setLayout(self.tabColor.layout)

    def init_TabShape(self):
        self.tabShape.layout = QVBoxLayout(self)
        self.tabShape.layout.addStretch()
        self.tabShape.layout.setDirection(3)

        layouts = []
        for key, widget in self.widgetObjs["Shape"].items():
            tempLayout = get_lbl_hbox(key, widget)
            layouts.append(tempLayout)
        for layout in layouts:
            self.tabShape.layout.addLayout(layout)
        self.tabShape.setLayout(self.tabShape.layout)

    def init_TabLog(self):
        self.tabLog.layout = QVBoxLayout(self)
        self.tabLog.layout.addStretch()
        self.tabLog.layout.setDirection(3)

        self.tabLog.layout.addWidget(self.widgetObjs["Log"]["Log"])
        self.tabLog.setLayout(self.tabLog.layout)

    def saveValues(self):
        main_xml = etree.Element("settings")

        sections = [None for x in range(len(self.widgetObjs))]

        i = 0
        for k, dictItems in self.widgetObjs.items():
            sections[i] = etree.Element(k)

            for key, obj in dictItems.items():
                if isinstance(obj, QLineEdit):
                    sections[i].attrib[str(key)] = str(obj.text())  ## ADD ATTRIBUTE TO XML
                    self.settings[k][key] = str(obj.text())  ## UPDATE SETTINGS

                elif isinstance(obj, QComboBox):
                    sections[i].attrib[str(key)] = str(obj.currentText())
                    self.settings[k][key] = str(obj.currentText())

                elif isinstance(obj, QCheckBox):
                    sections[i].attrib[str(key)] = str(obj.isChecked())
                    self.settings[k][key] = str(obj.isChecked())

            i += 1

        ## INSERT EACH SECTIONS
        for j in range(len(self.widgetObjs)):
            main_xml.append(sections[j])

        ####Save the XML, have pretty print ON
        final_tree = etree.ElementTree(main_xml)
        final_tree.write("../files/settings/settings.xml", pretty_print=True)

        return self.checkTree()

    def checkTree(self):

        all = False
        pins, adapters = [], []
        num_lru_selected = 0

        ## TREE
        root = self.tree_pins.invisibleRootItem()
        rootchild_count = root.childCount()
        for i in range(rootchild_count):
            lru = root.child(i)
            #print(lru.text(0), lru.checkState(0))
            if lru.checkState(0) == 2:
                num_lru_selected += 1


            lruchild_count = lru.childCount()
            for j in range(lruchild_count):
                conn = lru.child(j)
                #print(conn.text(0),conn.isSelected())                            ## IS SELECTED IS FOR WHEN ITS SELECTED, NOT CLICKED
                #print(conn.text(0), conn.checkState(0))                            ## PASSING THE COLUMN NUMBER

                connchild_count = conn.childCount()
                for k in range(connchild_count):
                    pin = conn.child(k)
                    #print(pin.text(0), pin.checkState(0))
                    if pin.checkState(0) == 2:
                        pins.append((lru.text(0),conn.text(0),pin.text(0)))

        ## TREE2
        root2 = self.tree_adapters.invisibleRootItem()
        lru2child_count = root2.childCount()
        for i in range(lru2child_count):
            lru2 = root2.child(i)
            #print(lru2.text(0), lru2.checkState(0))
            if lru2.checkState(0) == 2:
                adapters.append(lru2.text(0))

        if num_lru_selected == rootchild_count:
            all = True

        return all, pins, adapters

def get_lbl_hbox(text,otherWidget):                                                     ## GENERATE AN HBOX WITH A LABEL
    lbl = QLabel()
    lbl.setText(text)
    hbox = QHBoxLayout()
    hbox.addStretch()
    hbox.setDirection(1)                                                                ## PLACES TO THE LEFT
    hbox.addWidget(lbl)
    if isinstance(otherWidget,QLineEdit):
        otherWidget.setFixedWidth(100)
    hbox.addWidget(otherWidget)

    return hbox

def get_combo(items,index):                                                             ## GENERATE A QCOMBO
    combo = QComboBox()
    for item in items:
        combo.addItem(item)
    combo.setCurrentIndex(index)                                                        ## SET DEFAULT BASE ON INDEX VALUE, 0-BASE

    return combo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
