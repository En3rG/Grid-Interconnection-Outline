from shutil import copyfile
import shutil
import os
import sys
import webbrowser
import myLog
import threading

####################################################################################################################
##
####################################################################################################################
@myLog.catch_wrapper
def clean():
    print("...Deleting Output Contents")
    ## REMOVE CONTENTS OF DIRECTORY

    try: shutil.rmtree("../output")
    except: os.mkdir("../output/")

    ## CAN ONLY COPY FILES, NOT DIRECTORY.  ALSO DIRECTORY LOCATION HAS TO EXIST
    #copyfile("./FILES/css/style.css","./OUTPUT/style.css")

    print("...Copying contents from ../files/assets/")
    ## COPY OVER FILES
    shutil.copytree("../files/assets","../output/")

####################################################################################################################
##
####################################################################################################################

@myLog.catch_wrapper
def openChrome():
    def openBrowswer():
        ## once an exe this wont work
        #directory = os.path.dirname(__file__)
        directory = os.path.dirname(sys.argv[0])
        url = "file:///" + directory + "/../output/Interconnection.html"
        print(url)

        # MacOS
        #chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

        # Windows
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'

        #webbrowser.open(url)
        webbrowser.get(chrome_path).open(url)

    t = threading.Thread(target=openBrowswer, args=())
    t.start()

####################################################################################################################
## GENERATE style.css
####################################################################################################################
@myLog.catch_wrapper
def generateCss(settings):
    print("...Generating styles.css")

    filename = "style.css"
    cssfile = open("../output/css/" + filename, 'w', encoding='utf-8')

    lru_border_color = settings["CSS"]["lru_border_color"]
    lru_border_same_color = settings["CSS"]["lru_border_same_color"]
    lru_border_input_color = settings["CSS"]["lru_border_input_color"]
    lru_border_output_color = settings["CSS"]["lru_border_output_color"]
    lru_border_control_color = settings["CSS"]["lru_border_control_color"]
    lru_border_unknown_color = settings["CSS"]["lru_border_unknown_color"]
    lru_border_component_color = settings["CSS"]["lru_border_component_color"]
    lru_border_swcontrol_color = settings["CSS"]["lru_border_swcontrol_color"]
    lru_border_component_same_color = settings["CSS"]["lru_border_component_same_color"]
    lru_border_swcontrol_same_color = settings["CSS"]["lru_border_swcontrol_same_color"]

    background_color_lru = settings["CSS"]["background_color_lru"]
    background_color_cable = settings["CSS"]["background_color_cable"]
    background_color_internal = settings["CSS"]["background_color_internal"]

    lru_border_radius = settings["CSS"]["lru_border_radius"]
    cable_border_radius = settings["CSS"]["cable_border_radius"]
    input_border_radius = settings["CSS"]["input_border_radius"]
    output_border_radius = settings["CSS"]["output_border_radius"]
    control_border_radius = settings["CSS"]["control_border_radius"]
    unknown_border_radius = settings["CSS"]["unknown_border_radius"]
    component_border_radius = settings["CSS"]["component_border_radius"]
    swcontrol_border_radius = settings["CSS"]["swcontrol_border_radius"]
    lru_border_px = settings["CSS"]["lru_border_px"]

    cssfile.write("""

        /* variables */
        :root {
            --lru-size: 300px;
            --lru-margin-left: 60px;
            /* --lru-border: 15px solid #cccccc; */
            --lru-border: """ + lru_border_px + """ solid """ + lru_border_color + """;
            --lru-border-same: """ + lru_border_px + """ solid """ + lru_border_same_color + """;
            --lru-border-input: """ + lru_border_px + """ solid """ + lru_border_input_color + """;
            --lru-border-output: """ + lru_border_px + """ solid """ + lru_border_output_color + """;
            --lru-border-control: """ + lru_border_px + """ solid """ + lru_border_control_color + """;
            --lru-border-unknown: """ + lru_border_px + """ solid """ + lru_border_unknown_color +  """;
            --lru-border-component: """ + lru_border_px + """ solid """ + lru_border_component_color +  """;
            --lru-border-swcontrol: """ + lru_border_px + """ solid """ + lru_border_swcontrol_color +  """;
            --lru-border-component-same: """ + lru_border_px + """ solid """ + lru_border_component_same_color +  """;
            --lru-border-swcontrol-same: """ + lru_border_px + """ solid """ + lru_border_swcontrol_same_color +  """;

            /* tan */
            /* --background-color-lru: #ffebb3; */
            --background-color-lru: """ + background_color_lru + """;
            /* light gray */
            /* --background-color-cable: #b3b3b3; */
            --background-color-cable: """ + background_color_cable + """;
            --background-color-internal: """ + background_color_internal + """;

            --lru-border-radius: """ + lru_border_radius + """;
            --cable-border-radius: """ + cable_border_radius + """;
            --input-border-radius: """ + input_border_radius + """;
            --output-border-radius: """ + output_border_radius + """;
            --control-border-radius: """ + control_border_radius + """;
            --unknown-border-radius: """ + unknown_border_radius + """;
            --component-border-radius: """ + component_border_radius + """;
            --swcontrol-border-radius: """ + swcontrol_border_radius + """;

        }

        html {
            white-space: nowrap;
        }

        head{
            color: white;
        }

        body {
            background-image: linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.75)), url(img/image.jpg);
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            padding-left: 20px;
            padding-bottom: 0px;
            padding-top: 10px;
            margin-bottom: 0px;
            margin-top: 0px;

            overflow-x: auto;
        }

        h1 {
            color: white;
        }

        h2 {
            color: white;
        }

        h3 {
            font-weight: bold;
        }


        p {
            font-size: 2em;
        }

        #diagramContainer {
            padding: calc(var(--lru-margin-left)/2);
        }

        .lruname{
            text-align: center;
            margin-top: calc(var(--lru-size)*0.40);
            color: black;

        }

        .LRU {
            border-radius: var(--lru-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border);
            /* green */
            /*background-color: #a3d468; */
            /* tan */
            /* background-color: #ffebb3; */
            background-color: var(--background-color-lru);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;
        }

        .ADAPTER {
            border-radius: var(--lru-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border);
            background-color: red;
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;
        }

        .LRUSAME {
            border-radius: var(--lru-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-same);
            /* green */
            /*background-color: #a3d468; */
            /* tan */
            /* background-color: #ffebb3; */
            background-color: var(--background-color-lru);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;
        }

        .CABLE {
            border-radius: var(--cable-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border);
            /* background-color: #a3d468; */
            /* background-color: #b3b3b3; */
            background-color: var(--background-color-cable);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;
        }

        .CABLESAME {
            border-radius: var(--cable-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-same);
            /* background-color: #a3d468; */
            /* background-color: #b3b3b3; */
            background-color: var(--background-color-cable);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;
        }

        .input {
            border-radius: var(--input-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-input);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .output {
            border-radius: var(--output-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-output);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .control {
            border-radius: var(--control-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-control);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .unknown {
            border-radius: var(--unknown-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-unknown);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .COMPONENT {
            border-radius: var(--component-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-component);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .COMPONENTSAME {
            border-radius: var(--component-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-component-same);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .CONTROL {
            border-radius: var(--swcontrol-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-swcontrol);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .CONTROLSAME {
            border-radius: var(--swcontrol-border-radius);
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border-swcontrol-same);
            /* background-color: #a3d468; */
            background-color: var(--background-color-internal);
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;


        }

        .LRU_hidden {
            visibility: hidden;
            height:var(--lru-size); width: var(--lru-size);
            border: var(--lru-border);
            /* background-color: #a3d468; */
            background-color: #ffebb3;
            margin-left: var(--lru-margin-left);
            display: inline-block;
            vertical-align: middle;

        }


        .clear {
            clear: both;
        }

        .mini-button {
        background-color: black;
        display: block;
        padding: 4px;
        cursor: pointer;
        border: none;
        vertical-align: top;
        }


        .box {
        background-color: #BDBDBD;
        border: solid 2px black;
        padding: 8px;
        vertical-align: top;
        margin-top: 12px;
        margin-left: 10px;
        margin-right: 10px;
        max-width: 2000px;
        }

        .box h2 {
        padding: 8px;
        margin-bottom: 1.25em;
        background-color: #a3d468;
        color: black
        }

        .box .LABELS {
        background-color: black;
        color: gray
        }

        .image {
        max-width: 1900px;
        margin-bottom: 1.25em;
        }
    """)

    cssfile.close()
