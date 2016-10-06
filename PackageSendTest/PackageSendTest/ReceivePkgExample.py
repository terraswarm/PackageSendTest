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
        d = datetime.fromtimestamp(time_stamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print e
        return ''


# convert the 8 bytes timestamp to float
def bytes2float(byte_array):
    value = (byte_array[0] & 0xff) | ((byte_array[1] << 8) & 0xff00) | ((byte_array[2] << 16) & 0xff0000) \
            | ((byte_array[3] << 24) & 0xff000000)
    value += ((((byte_array[4]) & 0xff) | ((byte_array[5] << 8) & 0xff00)) / 1000.0)
    return value


# the ip address of the server
UDP_IP = '128.32.38.101'

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
        num = (len(data) - 5) / 22
        for i in range(num):
            print trans(data[5 + i * 22 + 1], data[5 + i * 22]) / 10000.0,
            print trans(data[5 + i * 22 + 3], data[5 + i * 22 + 2]) / 10000.0,
            print trans(data[5 + i * 22 + 5], data[5 + i * 22 + 4]) / 10000.0,
            print trans(data[5 + i * 22 + 7], data[5 + i * 22 + 6]) / 10000.0,
            print trans(data[5 + i * 22 + 9], data[5 + i * 22 + 8]) / 10000.0,
            print trans(data[5 + i * 22 + 11], data[5 + i * 22 + 10]) / 10000.0,
            print (data[5 + i * 22 + 12] | (data[5 + i * 22 + 13] << 8) | (data[5 + i * 22 + 14] << 16)),
            print data[5 + i * 22 + 15],
            print timestamp2string(bytes2float(data[5 + i * 22 + 16:5 + i * 22 + 22]))

    if data[4:5].decode("ascii") == 'g':  # unpack the glass accelerometer data package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        num = (len(data) - 5) / 12
        for i in range(num):
            print trans(data[5 + i * 12 + 1], data[5 + i * 12]) / 10000.0,
            print trans(data[5 + i * 12 + 3], data[5 + i * 12 + 2]) / 10000.0,
            print trans(data[5 + i * 12 + 5], data[5 + i * 12 + 4]) / 10000.0,
            print timestamp2string(bytes2float(data[5 + i * 12 + 6:5 + i * 12 + 12]))

    if data[4:5].decode("ascii") == 'b':  # unpack the watch battery package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        print data[5],
        print timestamp2string(bytes2float(data[6:12]))

    if data[4:5].decode("ascii") == 'e':  # unpack the environment package
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        num = (len(data) - 5) / 16
        for i in range(num):
            # because the pressure value is unsigned, so just combine two bytes
            print ((data[5 + i * 16 + 1] << 8 | data[5 + i * 16]) * 860.0 / 65535.0 + 250),
            print (trans(data[5 + i * 16 + 3], data[5 + i * 16 + 2]) - 896) / 64.0,
            print (trans(data[5 + i * 16 + 5], data[5 + i * 16 + 4]) - 2096) / 50.0,
            UV = trans(data[5 + i * 16 + 7], data[5 + i * 16 + 6]) / 38.8
            print UV,
            print (trans(data[5 + i * 16 + 9], data[5 + i * 16 + 8]) / ((0.05 * 0.928 * (0.3102 * UV)) + 0.8525 if (UV < 0.814) else (0.05 * 0.928 * (0.03683 * UV) + 1.075))),
            print timestamp2string(bytes2float(data[5 + i * 16 + 10:5 + i * 16 + 16]))
    print
