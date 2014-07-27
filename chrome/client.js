//var fs = require('fs');
// Connect to Binary.js server
var client = new BinaryClient('ws://localhost:9000/');

client.on('open', function() {
    var json = "{username: 'rohan', image: '/images/rohan_face.png', audio: '/audio/rohan_audio.mp3'}";
    data = {name: "/data/rohan.json", type: "json"};
    client.send(json, data);
});

// Received new stream from server!
client.on('stream', function(stream) {
    // Buffer for parts
    var parts = [];
    // Got new data
    stream.on('data', function(data){
        parts.push(data);
    });
    stream.on('end', function(){
        // Display new data in browser!
        var img = document.createElement("img");
        img.src = (window.URL || window.webkitURL).createObjectURL(new Blob(parts));
        document.body.appendChild(img);
    });
}); 

