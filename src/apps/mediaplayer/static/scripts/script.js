function init() {
    var wrapperWidth = document.getElementById("playing").offsetWidth;
    var fromCenter = (130 * 5 + 25) / 2 + 15;
    var offset = wrapperWidth / 2 - fromCenter;
    document.getElementById("controls").setAttribute("style", "left: " + offset + "px;");
    getCurrent();
    setInterval(getCurrent, 500);
}

function sendRequest(request, handler) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = getReadyStateHandler(xmlhttp, handler);
    xmlhttp.open("GET", request, true);
    xmlhttp.send();
}

function getReadyStateHandler(req, responseHandler) {
    return function() {
        if (req.readyState == 4 && req.status == 200) {
            console.log(req.responseXML)
            responseHandler(req.responseXML)
        }
    }
}

function getCurrent() {
    sendRequest(
        "nowplaying",
        function(xml) {
            console.log(xml);
            var nowPlaying = xml.getElementsByTagName("playing")[0].firstChild.nodeValue;
            document.getElementById("current-file").innerHTML=nowPlaying;
        }
    );
}

function playTrack(media_type, track) {
    console.log(track)
    sendRequest(
        media_type + "/play?file=" + track,
        function(xml) {
            getCurrent();
        }
    );
}

function playFolder(media_type, folder) {
    console.log(folder)
    sendRequest(
        media_type + "/play?folder=" + folder,
        function(xml) {
            getCurrent();
        }
    );
}

function playPause() {
    sendRequest(
        "music/pause",
        function(xml) {
            getCurrent();
        }
    );
}

function playNext() {
    sendRequest(
        "music/play?switch=next",
        function(xml) {
            getCurrent();
        }
    );
}

function playPrev() {
    sendRequest(
        "music/play?switch=previous",
       function(xml) {
            getCurrent();
        }
    );
}

function volumeDown() {
    sendRequest("music/volume?how=down", function(xml) {});
}

function volumeUp() {
    sendRequest("music/volume?how=up", function(xml) {});
}