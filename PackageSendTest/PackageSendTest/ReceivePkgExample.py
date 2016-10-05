import socket
from datetime import datetime


# the example of receiving data and unpack them


# convert the 2 bytes data to a integer
def trans(a, b):
    c = a * (2 ** 8)
    c = c + b
    if c > 2 ** 15:
        c = (2 ** 16 - c) * -1
    return c


# convert timestamp to time string
def timestamp2string(time_stamp):
    try:
        d = datetime.fromtimestamp(time_stamp / 1000.0)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print e
        return ''


# convert the 8 bytes timestamp to long int
def bytes2int(byte_array):
    value = (byte_array[0] & 0xff) | ((byte_array[1] << 8) & 0xff00) | ((byte_array[2] << 16) & 0xff0000) \
            | ((byte_array[3] << 24) & 0xff000000) | ((byte_array[4] << 32) & 0xff00000000) | ((byte_array[5] << 40) & 0xff000000000) \
            | ((byte_array[6] << 48) & 0xff000000000000) | ((byte_array[7] << 56) & 0xff00000000000000)
    value = int(value)
    return value


# the ip address of the server
UDP_IP = '192.168.1.32'

# tge socket port number
UDP_PORT = 4567

# initialize the socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# receive the data and parse them and print
while True:
    data, addr = sock.recvfrom(96000)
    data = bytearray(data)

    if data[4:5].decode("ascii") == 'w':  # unpack the watch IMU and PPG data package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        num = (len(data) - 5) / 24
        for i in range(num):
            print trans(data[5 + i * 24 + 1], data[5 + i * 24]) / 10000.0,
            print trans(data[5 + i * 24 + 3], data[5 + i * 24 + 2]) / 10000.0,
            print trans(data[5 + i * 24 + 5], data[5 + i * 24 + 4]) / 10000.0,
            print trans(data[5 + i * 24 + 7], data[5 + i * 24 + 6]) / 10000.0,
            print trans(data[5 + i * 24 + 9], data[5 + i * 24 + 8]) / 10000.0,
            print trans(data[5 + i * 24 + 11], data[5 + i * 24 + 10]) / 10000.0,
            print (data[5 + i * 20 + 12] | (data[5 + i * 20 + 13] << 8) | (data[5 + i * 20 + 14] << 16)),
            print data[5 + i * 20 + 15],
            print timestamp2string(bytes2int(data[5 + i * 24 + 16:5 + i * 24 + 24]))

    if data[4:5].decode("ascii") == 'g':  # unpack the glass accelerometer data package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        num = (len(data) - 5) / 14
        for i in range(num):
            print trans(data[5 + i * 14 + 1], data[5 + i * 14]) / 10000.0,
            print trans(data[5 + i * 14 + 3], data[5 + i * 14 + 2]) / 10000.0,
            print trans(data[5 + i * 14 + 5], data[5 + i * 14 + 4]) / 10000.0,
            print timestamp2string(bytes2int(data[5 + i * 14 + 6:5 + i * 14 + 14]))

    if data[4:5].decode("ascii") == 'b':  # unpack the watch battery package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        print data[5],
        print timestamp2string(bytes2int(data[6:14]))

    if data[4:5].decode("ascii") == 'e':  # unpack the environment package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        num = (len(data) - 5) / 18
        for i in range(num):
            # because the pressure value is unsigned, so just combine two bytes
            print ((data[5 + i * 18 + 1] << 8 | data[5 + i * 18]) * 860.0 / 65535.0 + 250),
            print (trans(data[5 + i * 18 + 3], data[5 + i * 18 + 2]) - 896) / 64.0,
            print (trans(data[5 + i * 18 + 5], data[5 + i * 18 + 4]) - 2096) / 50.0,
            UV = trans(data[5 + i * 18 + 7], data[5 + i * 18 + 6]) / 38.8
            print UV,
            print (trans(data[5 + i * 18 + 9], data[5 + i * 18 + 8]) / ((0.05 * 0.928 * (0.3102 * UV)) + 0.8525 if (UV < 0.814) else (0.05 * 0.928 * (0.03683 * UV) + 1.075))),
            print timestamp2string(bytes2int(data[5 + i * 18 + 10:5 + i * 18 + 18]))
    print
