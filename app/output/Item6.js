jsPlumb.ready(function() {

setTimeout(function () {jsPlumb.connect({source:"Unknown_HTR", target:"_wire001", anchor: [[0.5, 0, 0, 0, 0, 0],[0.5, 1, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("Unknown_HTR", { endpoint:"Dot",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: "_001:",visible:true,id: "Unknown_HTR_001:",}]]});
jsPlumb.addEndpoint("_wire001", { endpoint:"Dot",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: "_002:",visible:true,id: "_wire001_002:",}]]});},250);


setTimeout(function () {jsPlumb.connect({source:"Unknown_GND", target:"_wire002", anchor: [[0.5, 0, 0, 0, 0, 0],[0.5, 1, 0, 0, 0, 0]],});
jsPlumb.addEndpoint("Unknown_GND", { endpoint:"Dot",anchor:[0.5, 0, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, 2.5],label: "_003:",visible:true,id: "Unknown_GND_003:",}]]});
jsPlumb.addEndpoint("_wire002", { endpoint:"Dot",anchor:[0.5, 1, 0, 0, 0, 0],paintStyle: { fillStyle:"white", outlineColor:"black", outlineWidth:1},overlays: [["Label", {location: [0.5, -1.5],label: "_004:",visible:true,id: "_wire002_004:",}]]});},500);
});