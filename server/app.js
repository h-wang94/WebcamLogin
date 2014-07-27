var http = require('http');
var server = http.createServer(function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\n');

}).listen(9000);

var BinaryServer = require('binaryjs').BinaryServer;
var fs = require('fs');

// Start Binary.js server
var binaryServer = new BinaryServer({server: server, path: '/'});

// Wait for new user connections
binaryServer.on('connection', function(client){
    // Stream a flower as a hello!
    var file = fs.createReadStream(__dirname + '/icon.png');
    client.send(file); 

    client.on('stream', function(stream, meta) {
        var outFile;
        if (meta.type === "png") {
            outFile = fs.createWriteStream(__dirname + "/images/" + meta.name);
        } else if (meta.type === "json") {
            outFile = fs.createWriteStream(__dirname + "/data/" + meta.name);
        }
        stream.pipe(outFile);
        stream.on('end', function(data) {
            stream.write({end: true});
        });
    });
});
