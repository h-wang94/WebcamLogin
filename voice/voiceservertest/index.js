var express = require("express");
var cp = require("child_process");
var app = express();
var http = require("http").Server(app);
var io = require("socket.io")(http);

app.get("/", function(req, res) {
	res.sendfile("blahblah.html");
});

io.on('connection', function(socket) {
	console.log("Someone connected");
	socket.on('exec', function(args) {
		console.log("Exec command: " + args);
		cp.exec(args, function(err, stdout, stderr) {
			console.log("Execution completed.");
			socket.emit('response', [stdout, stderr]);
		})
	});
});

http.listen(3000, function() {
	console.log("Listening on *:3000");
});
