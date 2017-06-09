jsPlumb.ready(function() {

setTimeout(function () {jsPlumb.connect({source:"TERMINAL_HTR", target:"_wire001", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("TERMINAL_HTR", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_001:",visible:true,id: "TERMINAL_HTR_001:",}]]});
jsPlumb.addEndpoint("_wire001", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_002:",visible:true,id: "_wire001_002:",}]]});},250);


setTimeout(function () {jsPlumb.connect({source:"_wire001", target:"P1_Z", anchor: [[0.5, 0, 0, 0, 0, 0],[0.5, 1, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire001", { endpoint:"Dot",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: "_004:",visible:true,id: "_wire001_004:",}]]});
jsPlumb.addEndpoint("P1_Z", { endpoint:"Dot",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: "_003:",visible:true,id: "P1_Z_003:",}]]});},500);


setTimeout(function () {jsPlumb.connect({source:"TERMINAL_GND", target:"_wire002", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("TERMINAL_GND", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_005:",visible:true,id: "TERMINAL_GND_005:",}]]});
jsPlumb.addEndpoint("_wire002", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_006:",visible:true,id: "_wire002_006:",}]]});},750);


setTimeout(function () {jsPlumb.connect({source:"P1_J", target:"_wire003____00", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_J", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_007:",visible:true,id: "P1_J_007:",}]]});
jsPlumb.addEndpoint("_wire003____00", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_008:",visible:true,id: "_wire003____00_008:",}]]});},1000);

setTimeout(function () {jsPlumb.connect({source:"P2__1", target:"_wire003____00", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__1", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_009:",visible:true,id: "P2__1_009:",}]]});
jsPlumb.addEndpoint("_wire003____00", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_010:",visible:true,id: "_wire003____00_010:",}]]});},1250);

setTimeout(function () {jsPlumb.connect({source:"P2__2", target:"_wire003____01", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__2", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_011:",visible:true,id: "P2__2_011:",}]]});
jsPlumb.addEndpoint("_wire003____01", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_012:",visible:true,id: "_wire003____01_012:",}]]});},1500);

setTimeout(function () {jsPlumb.connect({source:"P2__3", target:"_wire003____01", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__3", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_013:",visible:true,id: "P2__3_013:",}]]});
jsPlumb.addEndpoint("_wire003____01", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_014:",visible:true,id: "_wire003____01_014:",}]]});},1750);

setTimeout(function () {jsPlumb.connect({source:"P2__4", target:"_wire003____02", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__4", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_015:",visible:true,id: "P2__4_015:",}]]});
jsPlumb.addEndpoint("_wire003____02", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_016:",visible:true,id: "_wire003____02_016:",}]]});},2000);

setTimeout(function () {jsPlumb.connect({source:"P1_K", target:"_wire004____00", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_K", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_017:",visible:true,id: "P1_K_017:",}]]});
jsPlumb.addEndpoint("_wire004____00", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_018:",visible:true,id: "_wire004____00_018:",}]]});},2250);

setTimeout(function () {jsPlumb.connect({source:"P2__5", target:"_wire004____00", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__5", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_019:",visible:true,id: "P2__5_019:",}]]});
jsPlumb.addEndpoint("_wire004____00", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_020:",visible:true,id: "_wire004____00_020:",}]]});},2500);

setTimeout(function () {jsPlumb.connect({source:"P2__6", target:"_wire004____01", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__6", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_021:",visible:true,id: "P2__6_021:",}]]});
jsPlumb.addEndpoint("_wire004____01", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_022:",visible:true,id: "_wire004____01_022:",}]]});},2750);

setTimeout(function () {jsPlumb.connect({source:"P2__7", target:"_wire004____01", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__7", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_023:",visible:true,id: "P2__7_023:",}]]});
jsPlumb.addEndpoint("_wire004____01", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_024:",visible:true,id: "_wire004____01_024:",}]]});},3000);

setTimeout(function () {jsPlumb.connect({source:"P2__8", target:"_wire004____02", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__8", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_025:",visible:true,id: "P2__8_025:",}]]});
jsPlumb.addEndpoint("_wire004____02", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_026:",visible:true,id: "_wire004____02_026:",}]]});},3250);

setTimeout(function () {jsPlumb.connect({source:"P1_G", target:"_wire005", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_G", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_027:",visible:true,id: "P1_G_027:",}]]});
jsPlumb.addEndpoint("_wire005", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_028:",visible:true,id: "_wire005_028:",}]]});},3500);


setTimeout(function () {jsPlumb.connect({source:"_wire005", target:"P3_A", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire005", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_030:",visible:true,id: "_wire005_030:",}]]});
jsPlumb.addEndpoint("P3_A", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_029:",visible:true,id: "P3_A_029:",}]]});},3750);


setTimeout(function () {jsPlumb.connect({source:"P1_H", target:"_wire006", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_H", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_031:",visible:true,id: "P1_H_031:",}]]});
jsPlumb.addEndpoint("_wire006", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_032:",visible:true,id: "_wire006_032:",}]]});},4000);


setTimeout(function () {jsPlumb.connect({source:"_wire006", target:"P3_B", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire006", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_034:",visible:true,id: "_wire006_034:",}]]});
jsPlumb.addEndpoint("P3_B", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_033:",visible:true,id: "P3_B_033:",}]]});},4250);


setTimeout(function () {jsPlumb.connect({source:"P1_a", target:"_wire007", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_a", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_035:",visible:true,id: "P1_a_035:",}]]});
jsPlumb.addEndpoint("_wire007", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_036:",visible:true,id: "_wire007_036:",}]]});},4500);


setTimeout(function () {jsPlumb.connect({source:"P1_S", target:"_wire008", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_S", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_037:",visible:true,id: "P1_S_037:",}]]});
jsPlumb.addEndpoint("_wire008", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_038:",visible:true,id: "_wire008_038:",}]]});},4750);


setTimeout(function () {jsPlumb.connect({source:"_wire008", target:"P4_A", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire008", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_040:",visible:true,id: "_wire008_040:",}]]});
jsPlumb.addEndpoint("P4_A", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_039:",visible:true,id: "P4_A_039:",}]]});},5000);


setTimeout(function () {jsPlumb.connect({source:"P1_R", target:"_wire009", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_R", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_041:",visible:true,id: "P1_R_041:",}]]});
jsPlumb.addEndpoint("_wire009", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_042:",visible:true,id: "_wire009_042:",}]]});},5250);


setTimeout(function () {jsPlumb.connect({source:"_wire009", target:"P4_B", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire009", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_044:",visible:true,id: "_wire009_044:",}]]});
jsPlumb.addEndpoint("P4_B", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_043:",visible:true,id: "P4_B_043:",}]]});},5500);

setTimeout(function () {jsPlumb.connect({source:"_wire009", target:"P4_C", anchor: [[0.5, 1, 0, 0, 0, 0],[0.5, 0, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire009", { endpoint:"Dot",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: "_046:",visible:true,id: "_wire009_046:",}]]});
jsPlumb.addEndpoint("P4_C", { endpoint:"Dot",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: "_045:",visible:true,id: "P4_C_045:",}]]});},5750);



setTimeout(function () {jsPlumb.connect({source:"P1_B", target:"_wire010", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_B", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_047:",visible:true,id: "P1_B_047:",}]]});
jsPlumb.addEndpoint("_wire010", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_048:",visible:true,id: "_wire010_048:",}]]});},6000);


setTimeout(function () {jsPlumb.connect({source:"_wire010", target:"P4_D", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire010", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_050:",visible:true,id: "_wire010_050:",}]]});
jsPlumb.addEndpoint("P4_D", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_049:",visible:true,id: "P4_D_049:",}]]});},6250);


setTimeout(function () {jsPlumb.connect({source:"P1_A", target:"_wire011", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P1_A", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_051:",visible:true,id: "P1_A_051:",}]]});
jsPlumb.addEndpoint("_wire011", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_052:",visible:true,id: "_wire011_052:",}]]});},6500);


setTimeout(function () {jsPlumb.connect({source:"_wire011", target:"P4_E", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire011", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_054:",visible:true,id: "_wire011_054:",}]]});
jsPlumb.addEndpoint("P4_E", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_053:",visible:true,id: "P4_E_053:",}]]});},6750);


setTimeout(function () {jsPlumb.connect({source:"P2__9", target:"_wire012", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__9", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_055:",visible:true,id: "P2__9_055:",}]]});
jsPlumb.addEndpoint("_wire012", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_056:",visible:true,id: "_wire012_056:",}]]});},7000);


setTimeout(function () {jsPlumb.connect({source:"P2__10", target:"_wire013", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__10", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_057:",visible:true,id: "P2__10_057:",}]]});
jsPlumb.addEndpoint("_wire013", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_058:",visible:true,id: "_wire013_058:",}]]});},7250);


setTimeout(function () {jsPlumb.connect({source:"P2__11", target:"_wire014", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__11", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_059:",visible:true,id: "P2__11_059:",}]]});
jsPlumb.addEndpoint("_wire014", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_060:",visible:true,id: "_wire014_060:",}]]});},7500);


setTimeout(function () {jsPlumb.connect({source:"P2__12", target:"_wire015", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P2__12", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_061:",visible:true,id: "P2__12_061:",}]]});
jsPlumb.addEndpoint("_wire015", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_062:",visible:true,id: "_wire015_062:",}]]});},7750);


setTimeout(function () {jsPlumb.connect({source:"P3_C", target:"_wire016", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P3_C", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_063:",visible:true,id: "P3_C_063:",}]]});
jsPlumb.addEndpoint("_wire016", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_064:",visible:true,id: "_wire016_064:",}]]});},8000);


setTimeout(function () {jsPlumb.connect({source:"P4_F", target:"_wire017", anchor: [[0, 0.5, 0, 0, 0, 0],[1, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("P4_F", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_065:",visible:true,id: "P4_F_065:",}]]});
jsPlumb.addEndpoint("_wire017", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_066:",visible:true,id: "_wire017_066:",}]]});},8250);




setTimeout(function () {jsPlumb.connect({source:"_wire003____00", target:"_wire003____01", anchor: [[0.5, 1, 0, 0, 0, 0],[0.5, 0, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire003____00", { endpoint:"Rectangle",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: ":",visible:true,id: "_wire003____00:",}]]});
jsPlumb.addEndpoint("_wire003____01", { endpoint:"Rectangle",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: ":",visible:true,id: "_wire003____01:",}]]});},8500);






setTimeout(function () {jsPlumb.connect({source:"_wire003____02", target:"_wire003____01", anchor: [[0.5, 0, 0, 0, 0, 0],[0.5, 1, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire003____02", { endpoint:"Rectangle",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: ":",visible:true,id: "_wire003____02:",}]]});
jsPlumb.addEndpoint("_wire003____01", { endpoint:"Rectangle",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: ":",visible:true,id: "_wire003____01:",}]]});},8750);



setTimeout(function () {jsPlumb.connect({source:"_wire004____00", target:"_wire004____01", anchor: [[0.5, 1, 0, 0, 0, 0],[0.5, 0, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire004____00", { endpoint:"Rectangle",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: ":",visible:true,id: "_wire004____00:",}]]});
jsPlumb.addEndpoint("_wire004____01", { endpoint:"Rectangle",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: ":",visible:true,id: "_wire004____01:",}]]});},9000);






setTimeout(function () {jsPlumb.connect({source:"_wire004____02", target:"_wire004____01", anchor: [[0.5, 0, 0, 0, 0, 0],[0.5, 1, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("_wire004____02", { endpoint:"Rectangle",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: ":",visible:true,id: "_wire004____02:",}]]});
jsPlumb.addEndpoint("_wire004____01", { endpoint:"Rectangle",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"#ffff80", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: ":",visible:true,id: "_wire004____01:",}]]});},9250);});