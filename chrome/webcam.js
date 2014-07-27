(function() {

    var streaming = false,
        video        = document.querySelector('#video'),
        canvas       = document.querySelector('#canvas'),
        photo        = document.querySelector('#photo'),
        startButton  = document.querySelector('#startButton'),
        downloadButton = document.querySelector('#downloadButton'),
        width = 480,
        height = 240;
    navigator.getUserMedia = ( navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia ||
                            navigator.msGetUserMedia);
    if (navigator.getUserMedia) {
        navigator.getUserMedia( {
                video: true,
                audio: false
            },
            function successCallback(stream) {
                if (navigator.mozGetUserMedia) {
                    video.mozSrcObject = stream;
                } else {
                    var vendorURL = window.URL || window.webkitURL;
                    video.src = vendorURL.createObjectURL(stream);
                }
                video.play();
            },
            function errorCallback(err) {
                console.log("An error occured! " + err.code);
            }
        );
    } else {
        console.log("Not supported");

    }
    video.addEventListener('canplay', function(ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth/width);
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);

    function takepicture() {
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(video, 0, 0, width, height);
        // socket stuff
        var imageData = canvas.toDataURL('image/png');
        var connection = new WebSocket("ws://localhost:8080");
        connection.onopen = function() {
            connection.send("SEND");
        };

        connection.onerror = function(error) {
            console.log("Error: " + error);
        };

        connection.onmessage = function(e) {
            console.log("Server: " + e);
        };

        var img = imageData.getImageData(0, 0, 480, 240);
        var binary = new Uint8Array(img.data.length);
        var i;
        for (i = 0; i < img.data.length; ++i) {
            binary[i] = img.data[i];
        }
        connection.send(binary.buffer);
    }

    startButton.addEventListener('click', function(ev){
        takepicture();
        ev.preventDefault();
    }, false);

})();
