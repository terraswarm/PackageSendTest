import socket
# the example of receiving data and unpack them


# convert the 2 bytes data to a integer
def trans(a, b):
    c = a * (2 ** 8)
    c = c + b
    if c > 2 ** 15:
        c = (2 ** 16 - c) * -1
    return c

# the ip address of the server
UDP_IP = '10.202.61.186'
# UDP_IP = '192.168.0.106'

# tge socket port number
UDP_PORT = 4567

# initialize the socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# receive the data and parse them and print
while True:
    data, addr = sock.recvfrom(96000)
    data = bytearray(data)
    if data[4:5].decode("ascii") == 'w':
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        for i in range(10):
            print trans(data[5 + i * 20 + 1], data[5 + i * 20]) / 10000.0,
            print trans(data[5 + i * 20 + 3], data[5 + i * 20 + 2]) / 10000.0,
            print trans(data[5 + i * 20 + 5], data[5 + i * 20 + 4]) / 10000.0,
            print trans(data[5 + i * 20 + 7], data[5 + i * 20 + 6]) / 10000.0,
            print trans(data[5 + i * 20 + 9], data[5 + i * 20 + 8]) / 10000.0,
            print trans(data[5 + i * 20 + 11], data[5 + i * 20 + 10]) / 10000.0,
            print (data[5 + i * 20 + 12] | (data[5 + i * 20 + 13] << 8) | (data[5 + i * 20 + 14] << 16)),
            print data[5 + i * 20 + 15],
            print (data[5 + i * 20 + 16] | (data[5 + i * 20 + 17] << 8) | (data[5 + i * 20 + 18] << 18) | (data[5 + i * 20 + 19] << 24))
    if data[4:5].decode("ascii") == 'g':
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        for i in range(10):
            print trans(data[5 + i * 10 + 1], data[5 + i * 10]) / 10000.0,
            print trans(data[5 + i * 10 + 3], data[5 + i * 10 + 2]) / 10000.0,
            print trans(data[5 + i * 10 + 5], data[5 + i * 10 + 4]) / 10000.0,
            print (data[5 + i * 10 + 6] | (data[5 + i * 10 + 7] << 8) | (data[5 + i * 10 + 8] << 16) | (data[5 + i * 10 + 9] << 24))
    if data[4:5].decode("ascii") == 'b':
        print data[0:4].decode("ascii"),
        print data[4:5].decode("ascii")
        print data[5]
    print


