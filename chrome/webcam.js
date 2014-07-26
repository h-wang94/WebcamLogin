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
        var imageData = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
    }

    startButton.addEventListener('click', function(ev){
        takepicture();
        ev.preventDefault();
    }, false);

})();
