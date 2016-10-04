// Receive Watch Gesture data and decode it

/*globals Java, exports, require, util */
/*jshint globalstrict: true */
"use strict";
var dgram = require('dgram');

// Convert the 2 bytes data to a integer.
function trans(a, b) {
    var c = a * Math.pow(2, 8);
    c = c + b;
    if (c > Math.pow(2, 15)) { 
        c = (Math.pow(2, 16) - c) * -1;
    }
    return c;
}

// The ip address of the server.
var UDP_IP = "192.168.1.32";

// The socket port number.
var UDP_PORT = 4567;

//initialize the socket and bind it
// sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
var sock = dgram.createSocket('udp4');

sock.on('message', function (data) {
    // Receive the data and parse them and print.
    if (data.toString("utf-8", 4, 5) === "w") {
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        for(var i = 0; i < 10; i++) {
            console.log(trans(data[5 + i * 20 + 1], data[5 + i * 20]) / 10000.0 + " " +
                        trans(data[5 + i * 20 + 3], data[5 + i * 20 + 2]) / 10000.0 + " " +
                        trans(data[5 + i * 20 + 5], data[5 + i * 20 + 4]) / 10000.0 + " " +
                        trans(data[5 + i * 20 + 7], data[5 + i * 20 + 6]) / 10000.0 + " " +
                        trans(data[5 + i * 20 + 9], data[5 + i * 20 + 8]) / 10000.0 + " " +
                        trans(data[5 + i * 20 + 11], data[5 + i * 20 + 10]) / 10000.0 + " " +
                        (data[5 + i * 20 + 12] | (data[5 + i * 20 + 13] << 8) | (data[5 + i * 20 + 14] << 16)) + " " +
                        data[5 + i * 20 + 15] + " " +
                        ((data[5 + i * 20 + 16] | (data[5 + i * 20 + 17] << 8) | (data[5 + i * 20 + 18] << 18) | (data[5 + i * 20 + 19] << 24)) >>> 0)); // Use >>> 0 to convert to unsigned.
        }
    } else if (data.toString("utf-8", 4, 5) === "g") {
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        for(var i = 0; i < 10; i++) {
            console.log(trans(data[5 + i * 10 + 1], data[5 + i * 10]) / 10000.0 + " " +
                        trans(data[5 + i * 10 + 3], data[5 + i * 10 + 2]) / 10000.0 + " " +
                        trans(data[5 + i * 10 + 5], data[5 + i * 10 + 4]) / 10000.0 + " " +
                        ((data[5 + i * 10 + 6] | (data[5 + i * 10 + 7] << 8) | (data[5 + i * 10 + 8] << 16) | (data[5 + i * 10 + 9] << 24)) >>> 0)); // Use >>> 0 to convert to unsigned.
        }
    } else if (data.toString("utf-8", 4, 5) === "b") {
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        console.log(data[5]);
    }
    console.log("");
});

sock.bind(UDP_PORT, UDP_IP);

