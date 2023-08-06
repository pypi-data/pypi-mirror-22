(function(lr) {
    var ws = new WebSocket(lr.url);
    ws.onopen = function() {
        ws.send("Register");
    };
    ws.onmessage = function (evt) {
        console.log("Reloading due to change in ", evt.data);
        window.location.reload(true);
    };
})(window.livereload)

