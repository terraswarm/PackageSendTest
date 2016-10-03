// Send Watch data via UDP Packages.

/*globals Java, exports, require, util */
/*jshint globalstrict: true */
"use strict";
var dgram = require('dgram');

/** Convert short int to 2 bytes array.
 */
function short_to_bytes(n) {
    var b = new Uint8Array([0, 0]);
    if (b < 0) {
        n = (Math.pow(2, 16) + n);
    }
    b[0] = n & 0xFF;
    n >>= 8;
    b[1] = n & 0xFF;
    return b;
}

/** Convert int to 3 bytes array. */
function int_to_3bytes(n) {
    var b = new Uint8Array([0, 0, 0]);
    b[0] = n & 0xFF;
    n >>= 8;
    b[1] = n & 0xFF;
    n >>= 8;
    b[2] = n & 0xFF;
    return b;
}


/** Convert int to 4 bytes array */
function int_to_4bytes(n) {
    var b = new Uint8Array([0, 0, 0, 0]);
    b[0] = n & 0xFF;
    n >>= 8;
    b[1] = n & 0xFF;
    n >>= 8;
    b[2] = n & 0xFF;
    n >>= 8;
    b[3] = n & 0xFF;
    return b;
}

// The ip address of the server.
var UDP_IP = '192.168.1.32';

// The socket port number
var UDP_PORT = 4567;

// package head info -- Device data and Package type
var DEV_ID = '9096';
var WATCH_TYPE = "w".charCodeAt(0);
var GLASS_TYPE = "g".charCodeAt(0);
var BATTERY_TYPE = "b".charCodeAt(0);

// Original data of the data body for all three kinds of package.
var ACCx = 0.98;
var ACCy = 0.01;
var ACCz = -0.02;
var GYRx = 0.2;
var GYRy = -0.3;
var GYRz = 0.4;
var PPG = 100000;
var HR = 70;
var BATTERY_LIFE = 90;

// Convert the original data to the format the data body requires.
var accx = (ACCx * 10000) | 0;
var accy = (ACCy * 10000) | 0;
var accz = (ACCz * 10000) | 0;
var gyrx = (GYRx * 10000) | 0;
var gyry = (GYRy * 10000) | 0;
var gyrz = (GYRz * 10000) | 0;

// Pack the watch IMU and PPG data package, assuming that every package contains 10 data samples
var watch_p = new Uint8Array(205);
watch_p[0] = DEV_ID.charCodeAt(0);
watch_p[1] = DEV_ID.charCodeAt(1);
watch_p[2] = DEV_ID.charCodeAt(2);
watch_p[3] = DEV_ID.charCodeAt(3);
watch_p[4] = WATCH_TYPE;
for(var i = 0; i < 10; i++) {
    var now = Date.now();
    watch_p[5 + i * 20] = short_to_bytes(accx)[0];
    watch_p[5 + i * 20 + 1] = short_to_bytes(accx)[1];
    watch_p[5 + i * 20 + 2] = short_to_bytes(accy)[0];
    watch_p[5 + i * 20 + 3] = short_to_bytes(accy)[1];
    watch_p[5 + i * 20 + 4] = short_to_bytes(accz)[0];
    watch_p[5 + i * 20 + 5] = short_to_bytes(accz)[1];
    watch_p[5 + i * 20 + 6] = short_to_bytes(gyrx)[0];
    watch_p[5 + i * 20 + 7] = short_to_bytes(gyrx)[1];
    watch_p[5 + i * 20 + 8] = short_to_bytes(gyry)[0];
    watch_p[5 + i * 20 + 9] = short_to_bytes(gyry)[1];
    watch_p[5 + i * 20 + 10] = short_to_bytes(gyrz)[0];
    watch_p[5 + i * 20 + 11] = short_to_bytes(gyrz)[1];
    watch_p[5 + i * 20 + 12] = int_to_3bytes(PPG)[0];
    watch_p[5 + i * 20 + 13] = int_to_3bytes(PPG)[1];
    watch_p[5 + i * 20 + 14] = int_to_3bytes(PPG)[2];
    watch_p[5 + i * 20 + 15] = (HR & 0xFF);
    watch_p[5 + i * 20 + 16] = int_to_4bytes(now)[0];
    watch_p[5 + i * 20 + 17] = int_to_4bytes(now)[1];
    watch_p[5 + i * 20 + 18] = int_to_4bytes(now)[2];
    watch_p[5 + i * 20 + 19] = int_to_4bytes(now)[3];
}
// Pack the glasses package, assuming that every package contains 10 data samples
var glass_p = new Uint8Array(105);
glass_p[0] = DEV_ID.charCodeAt(0);
glass_p[1] = DEV_ID.charCodeAt(1);
glass_p[2] = DEV_ID.charCodeAt(2);
glass_p[3] = DEV_ID.charCodeAt(3);
glass_p[4] = GLASS_TYPE;
for(var i = 0; i < 10; i++) {
    var now = Date.now();
    glass_p[5 + i * 10] = short_to_bytes(accx)[0];
    glass_p[5 + i * 10 + 1] = short_to_bytes(accx)[1];
    glass_p[5 + i * 10 + 2] = short_to_bytes(accy)[0];
    glass_p[5 + i * 10 + 3] = short_to_bytes(accy)[1];
    glass_p[5 + i * 10 + 4] = short_to_bytes(accz)[0];
    glass_p[5 + i * 10 + 5] = short_to_bytes(accz)[1];
    glass_p[5 + i * 10 + 6] = int_to_4bytes(now)[0];
    glass_p[5 + i * 10 + 7] = int_to_4bytes(now)[1];
    glass_p[5 + i * 10 + 8] = int_to_4bytes(now)[2];
    glass_p[5 + i * 10 + 9] = int_to_4bytes(now)[3];
}

// Pack the battery life package.
var battery_p = new Uint8Array(6);
battery_p[0] = DEV_ID.charCodeAt(0);
battery_p[1] = DEV_ID.charCodeAt(1);
battery_p[2] = DEV_ID.charCodeAt(2);
battery_p[3] = DEV_ID.charCodeAt(3);
battery_p[4] = BATTERY_TYPE;
battery_p[5] = BATTERY_LIFE;

// initialize the socket and bind it
//sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
var sock = dgram.createSocket('udp4');
var i = 0;

// Every second send a watch data package and a glasses package, every 5 minutes send a battery package
setInterval(function() {
    //console.log(watch_p);
    //sock.sendto(watch_p, (UDP_IP, UDP_PORT)) //Send message to UDP port
    sock.send(Buffer.from(watch_p), UDP_PORT, UDP_IP /*, callback */);

    //time.sleep(0.5)

    // console.log(glass_p);
    //sock.sendto(glass_p, (UDP_IP, UDP_PORT)) //Send message to UDP port
    sock.send(Buffer.from(glass_p), UDP_PORT, UDP_IP /*, callback */);

    //time.sleep(0.5)
    i += 1;
    if (i % 300 == 0) {
        console.log(battery_p);
        //sock.sendto(battery_p, (UDP_IP, UDP_PORT)) //Send message to UDP port
        sock.send(Buffer.from(battery_p), UDP_PORT, UDP_IP /*, callback */);
    }
}, 1000);
