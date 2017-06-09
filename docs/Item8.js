jsPlumb.ready(function() {

setTimeout(function () {jsPlumb.connect({source:"J1_A", target:"_wire001", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("J1_A", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_001:",visible:true,id: "J1_A_001:",}]]});
jsPlumb.addEndpoint("_wire001", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_002:",visible:true,id: "_wire001_002:",}]]});},250);


setTimeout(function () {jsPlumb.connect({source:"J1_B", target:"_wire002", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("J1_B", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_003:",visible:true,id: "J1_B_003:",}]]});
jsPlumb.addEndpoint("_wire002", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_004:",visible:true,id: "_wire002_004:",}]]});},500);


setTimeout(function () {jsPlumb.connect({source:"J1_C", target:"_wire003", anchor: [[1, 0.5, 0, 0, 0, 0],[0, 0.5, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("J1_C", { endpoint:"Dot",anchor:[1, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [-2, 0.5],label: "_005:",visible:true,id: "J1_C_005:",}]]});
jsPlumb.addEndpoint("_wire003", { endpoint:"Dot",anchor:[0, 0.5, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [3, 0.5],label: "_006:",visible:true,id: "_wire003_006:",}]]});},750);
});