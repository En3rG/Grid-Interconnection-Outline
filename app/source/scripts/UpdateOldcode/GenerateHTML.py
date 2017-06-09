from lxml import etree
import myLog

class Generator_html():
    @myLog.catch_wrapper
    def __init__(self, PARAMS, name_of_file, additionalInfo, get_internal=False, delimeterDuplicatingLRU="not_set"):
        ## METHODS
        name_of_file = self.updateFileName(name_of_file, delimeterDuplicatingLRU)
        self.generateHtml(PARAMS, name_of_file, get_internal, additionalInfo)

    ####################################################################################################################
    ##
    ####################################################################################################################
    def updateFileName(self, name_of_file, delimeterDuplicatingLRU):
        if delimeterDuplicatingLRU == "not_passed":
            doing = None
        else:
            ## IF DELIMETER IS IN THE name_of_file, UPDATE name_of_file TO END BEFORE THE DELIMETER
            if delimeterDuplicatingLRU in name_of_file:
                end_here = name_of_file.find(delimeterDuplicatingLRU)
                print("...name of file was:", name_of_file)
                name_of_file = name_of_file[:end_here]
                print("...name of file will now be:", name_of_file)

        return name_of_file

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generateHtml(self, PARAMS, name_of_file, get_internal, additionalInfo):
        myfunction_list = []

        print("...Generating html")
        version = "v" + str(PARAMS.major) + "." + str(PARAMS.minor) + "." + str(PARAMS.build)
        htmlfile = open("../output/" + name_of_file + '.html', 'w', encoding='utf-8')

        htmlfile.write("<!DOCTYPE html>")
        htmlfile.write("<html ng-app="">")

        head_string = self.generateHeadString(version, name_of_file)
        htmlfile.write(head_string)

        htmlfile.write('\n' + "<body>")
        body_string = self.generateBodyString(PARAMS, myfunction_list)
        htmlfile.write(body_string)

        info_string = self.generateInfoString(get_internal, additionalInfo)
        htmlfile.write(info_string)

        script_string = self.generateScriptString(myfunction_list, name_of_file, get_internal)
        htmlfile.write(script_string)

        htmlfile.write('\n' + "</body>")

        htmlfile.close()

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generateHeadString(self, version, name_of_file):

        head_string = """<head>\n"""

        ## HEAD CONTENTS
        head_string = head_string + """<meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
            <!-- Bootstrap -->
            <link href="css/bootstrap.min.css" rel="stylesheet">
            <link href="css/style.css" rel="stylesheet">
            <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
            <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
            <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.jskhk"></script>
            <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.jsjlkjl"></script>
            <![endif]-->
            <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
            <script src="js/jquery.min.js"></script>
            <!-- Include all compiled plugins (below), or include individual files as needed -->
            <script src="js/bootstrap.min.js"></script>
            <!-- <img class='logo' src="img/logo.jpg"> -->
            <title>GIO</title>"""
        head_string = head_string + """<h1>Grid Interconnection Outline (""" + version + """)</h1>"""
        head_string = head_string + "<h2>" + name_of_file + " Drawing: </h2>"
        head_string = head_string + """\n</head>"""

        return head_string

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generateBodyString(self, PARAMS, myfunction_list):
		## BODY CONTENTS
        body_string = ""

        temp_string = ""

		## GO THROUGH THE MATRIX
        maxrow, maxcol = PARAMS.positionMatrix.shape

        for rows in range(0, maxrow):
			## START ROW
            temp_string = temp_string + """<div id="diagramContainer" class="clear"/>"""
            for cols in range(0, maxcol):
				## START COL
                if PARAMS.positionMatrix[rows][cols] != None:
                    # temp_string = temp_string + """<div id="DSP" class="LRU"><h2 class="lruname">DSP</h2></div>"""
                    id = PARAMS.positionMatrix[rows][cols].source_lru
                    print(id)

                    label = PARAMS.positionMatrix[rows][cols].pin_interconnections_list[0].SOURCE.lru_label
                    lru_type = PARAMS.positionMatrix[rows][cols].pin_interconnections_list[0].SOURCE.lruType

                    print("id, label, lru_type:", id, ",", label, ",", lru_type)

                    my_function = "my" + label
                    myfunction_list.append(label)

                    temp_string = temp_string + """<div id=\"""" + id + """\" class=\"""" + lru_type + """\" onclick=\"""" + my_function + """()\"><h2 class="lruname">""" + label + """</h2></div>"""
                else:
					## ELEMENT IS SET TO NONE
                    temp_string = temp_string + """<div class="LRU_hidden"></div>"""
			## END ROW
            temp_string = temp_string + """</div>"""

        body_string = body_string + temp_string

        # body_string = """
        #     <div id="diagramContainer"/>
        #         <div id="DSP" class="LRU"><h2 class="lruname">DSP</h2></div>
        #     </div>
        #
        #     <div id="diagramContainer"/>
        #         <div id="ECM1" class="LRU"><h2 class="lruname">ECM1</h2></div>
        #         <div id="ECM2" class="LRU"><h2 class="lruname">ECM2</h2></div>
        #         <div id="ECM3" class="LRU"><h2 class="lruname">ECM3</h2></div>
        #         <div id="ECM" class="LRU"><h2 class="lruname">ECM</h2></div>
        #     </div>
        #
        #     <div id="diagramContainer"/>
        #         <div class="LRU_hidden"></div>
        #         <div id="VCDM" class="LRU"><h2 class="lruname">VCDM</h2></div>
        #     </div>
        # """

        return body_string

    ####################################################################################################################
    ##
    ####################################################################################################################
    def generateInfoString(self, get_internal, additionalInfo):
		## FOR LRUs
        if get_internal == False:
            pin_info_string = ""
            for elem in additionalInfo:
                if elem.tag == "PINSInfo":
                    for pin in elem:
                        pin_info_string = pin_info_string + """<p>"""
                        for key, value in pin.attrib.items():
                            pin_info_string = pin_info_string + """<span class="LABELS"> """ + key + """:</span> """ + value + """ """
                        pin_info_string = pin_info_string + """</p>"""

            images_info_string = ""
            for elem in additionalInfo:
                if elem.tag == "ImagesInfo":
                    for child in elem:
                        images_info_string = images_info_string + """<div id="box" class="box">"""
                        images_info_string = images_info_string + """<h2>""" + str(child.attrib["Image"]) + """</h2>"""
                        images_info_string = images_info_string + """<img class="image" src="img/""" + str(
                            child.attrib["Image"]) + """\">"""
                        images_info_string = images_info_string + """</div>"""

            info_string = """
                            <div class="path-group">
                                <button type="button" class="mini-button" data-toggle="collapse" data-target="#path-1"><h2>Additional Info</h2></button>
                                <div id="path-1" class="path collapse out">
                                    <div id="box" class="box">
                                        <h2>Info</h2>
                                        """ + pin_info_string + """
                                    </div>
                                    """ + images_info_string + """
                                </div>
                            </div>
                        """

        else:
            ## FOR INTERCONNECTIONS
            xml_info_string = ""
            for elem in additionalInfo:
                if elem.tag == "XMLInfo":
                    for child in elem:
                        xml_info_string = xml_info_string + """<p>"""
                        for key, value in child.attrib.items():
                            if key == "Images":
                                ## SKIP
                                doing = None
                            else:
                                xml_info_string = xml_info_string + """<span class="LABELS"> """ + key + """:</span> """ + value + """ """
                    xml_info_string = xml_info_string + """</p>"""

            # xml_info_string = """
            #                     <p><span class="LABELS">id:</span> v3849949 <span class="LABELS">id:</span> v3849949</p>
            #                     <p><span class="LABELS">Text:</span> Lead Filter Cover and Lead Filter Removal.</p>
            #
            #                     """

            connections_info_string = ""
            for elem in additionalInfo:
                if elem.tag == "ConnectionsInfo":
                    for lru in elem:
                        connections_info_string = connections_info_string + """<h3>""" + lru.attrib[
                            "name"] + """</h3>"""
                        for pin in lru:
                            connections_info_string = connections_info_string + """<p>"""
                            for key, value in pin.attrib.items():
                                connections_info_string = connections_info_string + """<span class="LABELS"> """ + key + """:</span> """ + value + """ """
                            connections_info_string = connections_info_string + """</p>"""

            info_string = """
                            <div class="path-group">
                                <button type="button" class="mini-button" data-toggle="collapse" data-target="#path-1"><h2>Additional Info</h2></button>
                                <div id="path-1" class="path collapse out">
                                    <div id="box" class="box">
                                        <h2>XML Info</h2>
                                        """ + xml_info_string + """
                                    </div>
                                    <div id="box" class="box">
                                        <h2>Connections Info</h2>
                                        """ + connections_info_string + """
                                    </div>
                                </div>
                            </div>
                        """


        return info_string

    ####################################################################################################################
    #####
    ####################################################################################################################
    def generateScriptString(self, myfunction_list, name_of_file, get_internal):
        temp_script = "<script src=\"" + name_of_file + ".js\"></script>"

        script_string = """
                    <script src="js/bootstrap.min.js"></script>
                    <script src="js/jquery.min_jsplumb.js"></script>
                    <script src="js/jquery-ui.min.js"></script>
                    <script src="js/jquery.jsPlumb-1.4.1-all-min.js"></script>
                    """ + temp_script

        ##< button onclick = "myFunction()" > Try it < / button >

        ##< script >
        ##function myFunction()
        ##{
        ##window.open("http://www.w3schools.com", "_blank", "toolbar=no,scrollbars=yes,resizable=yes,top=500,left=500,width=400,height=400");
        ##}
        ##</script >

        temp_string = ""

        if get_internal == True:
			## GO THROUGH THE myfunction LIST
            temp_string = """<script>"""
            for function in myfunction_list:
                temp_string = temp_string + """function my""" + function + """()""" + '\n'
                temp_string = temp_string + """{"""
                temp_string = temp_string + """window.open(\"""" + function + """.html\", "_blank", "toolbar=no,scrollbars=yes,resizable=yes,top=100,left=100,width=400,height=400");"""
                temp_string = temp_string + """}"""

            temp_string = temp_string + """</script>""" + '\n'

        script_string = script_string + temp_string

        return script_string