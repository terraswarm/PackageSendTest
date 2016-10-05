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

// Convert timestamp to time string.
function timestamp2string(time_stamp) {
    try {
        // Python time is in seconds.  JavaScript milliseconds.
        //d = datetime.fromtimestamp(time_stamp / 1000.0);
        var d = new Date(time_stamp);
        //str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f");
        var str1 = d.toISOString();
        console.log("timestamp2string(" + time_stamp + ")" + d + " " + Date.now());

        // Python: 2015-08-28 16:43:37.283000
        // JavaScript: 2016-10-05T03:21:09.617Z 
        return str1;
    } catch (e) {
        console.log(e);
        return '';
    }
}

// Convert the 8 bytes timestamp to long int.
function bytes2int(byte_array) {
    console.log(byte_array);
    var value = ((byte_array[0] & 0xff) | ((byte_array[1] << 8) & 0xff00) | ((byte_array[2] << 16) & 0xff0000)
                 | ((byte_array[3] << 24) & 0xff000000) | ((byte_array[4] << 32) & 0xff00000000)
                 | ((byte_array[5] << 40) & 0xff000000000) | ((byte_array[6] << 48) & 0xff000000000000)
                 | ((byte_array[7] << 56) & 0xff00000000000000)) >>> 0;
    //value = Math.round(value);
    return value;
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
            console.log(trans(data[5 + i * 24 + 1], data[5 + i * 24]) / 10000.0 + " " +
                        trans(data[5 + i * 24 + 3], data[5 + i * 24 + 2]) / 10000.0 + " " +
                        trans(data[5 + i * 24 + 5], data[5 + i * 24 + 4]) / 10000.0 + " " +
                        trans(data[5 + i * 24 + 7], data[5 + i * 24 + 6]) / 10000.0 + " " +
                        trans(data[5 + i * 24 + 9], data[5 + i * 24 + 8]) / 10000.0 + " " +
                        trans(data[5 + i * 24 + 11], data[5 + i * 24 + 10]) / 10000.0 + " " +
                        (data[5 + i * 24 + 12] | (data[5 + i * 24 + 13] << 8) | (data[5 + i * 24 + 14] << 16)) + " " +
                        data[5 + i * 24 + 15] + " " +
                        timestamp2string(bytes2int(data.slice(5 + i * 24 + 16, 5 + i * 24 + 24 + 1))));
        }
    } else if (data.toString("utf-8", 4, 5) === "g") {
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        for(var i = 0; i < 10; i++) {
            console.log(trans(data[5 + i * 14 + 1], data[5 + i * 14]) / 10000.0 + " " +
                        trans(data[5 + i * 14 + 3], data[5 + i * 14 + 2]) / 10000.0 + " " +
                        trans(data[5 + i * 14 + 5], data[5 + i * 14 + 4]) / 10000.0 + " " +
                        timestamp2string(bytes2int(data.slice(5 + i * 14 + 6, 5 + i * 14 + 14 + 1))));
        }
    } else if (data.toString("utf-8", 4, 5) === "b") {
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        console.log(data[5]);
        console.log(timestamp2string(bytes2int(data.slice(6, 14 + 1))));
    } else if (data.toString("utf-8", 4, 5) === "e") {  // unpack the environment package
        console.log(data.toString("utf-8", 0, 4));
        console.log(data.toString("utf-8", 4, 5));
        var num = (data.length - 5) / 18
        for(var i = 0; i < num; i++) {
            // because the pressure value is unsigned, so just combine two bytes
            var UV = trans(data[5 + i * 18 + 7], data[5 + i * 18 + 6]) / 38.8;

            console.log(((data[5 + i * 18 + 1] << 8 | data[5 + i * 18]) * 860.0 / 65535.0 + 250) + " " +
                        (trans(data[5 + i * 18 + 3], data[5 + i * 18 + 2]) - 896) / 64.0 + " " +
                        (trans(data[5 + i * 18 + 5], data[5 + i * 18 + 4]) - 2096) / 50.0 + " " +
                        UV + " " +
                        timestamp2string(bytes2int(data.slice(5 + i * 18 + 10, 5 + i * 18 + 18))));

                 // print (trans(data[5 + i * 18 + 9], data[5 + i * 18 + 8]) / ((0.05 * 0.928 * (0.3102 * UV)) + 0.8525 if (UV < 0.814) else (0.05 * 0.928 * (0.03683 * UV) + 1.075))),
        }
    }
    console.log("");
});

sock.bind(UDP_PORT, UDP_IP);

