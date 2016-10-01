import socket
import time


# convert short int to 2 bytes array
def short_to_bytes(n):
    b = bytearray([0, 0])   # init
    if b < 0:
        n = (2 ** 16 + n)

    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    return b


# convert int to 3 bytes array
def int_to_3bytes(n):
    b = bytearray([0, 0, 0])   # init
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    n >>= 8
    b[2] = n & 0xFF
    return b


# convert int to 4 bytes array
def int_to_4bytes(n):
    b = bytearray([0, 0, 0, 0])   # init
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    n >>= 8
    b[2] = n & 0xFF
    n >>= 8
    b[3] = n & 0xFF
    return b

# the ip address of the server
UDP_IP = '10.202.61.186'
# tge socket port number
UDP_PORT = 4567

# package head info -- Device data and Package type
DEV_ID = '9096'
WATCH_TYPE = 'w'
GLASS_TYPE = 'g'
BATTERY_TYPE = 'b'

# original data of the data body for all three kinds of package
ACCx = 0.98
ACCy = 0.01
ACCz = -0.02
GYRx = 0.2
GYRy = -0.3
GYRz = 0.4
PPG = 100000
HR = 70
BATTERY_LIFE = 90

# convert the original data to the format the data body requires
accx = int(ACCx * 10000)
accy = int(ACCy * 10000)
accz = int(ACCz * 10000)
gyrx = int(GYRx * 10000)
gyry = int(GYRy * 10000)
gyrz = int(GYRz * 10000)

# pack the watch IMU and PPG data package, assuming that every package contains 10 data samples
watch_p = bytearray(205)
watch_p[0] = DEV_ID[0]
watch_p[1] = DEV_ID[1]
watch_p[2] = DEV_ID[2]
watch_p[3] = DEV_ID[3]
watch_p[4] = WATCH_TYPE
for i in range(10):
    now = int(time.time())
    watch_p[5 + i * 20] = short_to_bytes(accx)[0]
    watch_p[5 + i * 20 + 1] = short_to_bytes(accx)[1]
    watch_p[5 + i * 20 + 2] = short_to_bytes(accy)[0]
    watch_p[5 + i * 20 + 3] = short_to_bytes(accy)[1]
    watch_p[5 + i * 20 + 4] = short_to_bytes(accz)[0]
    watch_p[5 + i * 20 + 5] = short_to_bytes(accz)[1]
    watch_p[5 + i * 20 + 6] = short_to_bytes(gyrx)[0]
    watch_p[5 + i * 20 + 7] = short_to_bytes(gyrx)[1]
    watch_p[5 + i * 20 + 8] = short_to_bytes(gyry)[0]
    watch_p[5 + i * 20 + 9] = short_to_bytes(gyry)[1]
    watch_p[5 + i * 20 + 10] = short_to_bytes(gyrz)[0]
    watch_p[5 + i * 20 + 11] = short_to_bytes(gyrz)[1]
    watch_p[5 + i * 20 + 12] = int_to_3bytes(PPG)[0]
    watch_p[5 + i * 20 + 13] = int_to_3bytes(PPG)[1]
    watch_p[5 + i * 20 + 14] = int_to_3bytes(PPG)[2]
    watch_p[5 + i * 20 + 15] = (HR & 0xFF)
    watch_p[5 + i * 20 + 16] = int_to_4bytes(now)[0]
    watch_p[5 + i * 20 + 17] = int_to_4bytes(now)[1]
    watch_p[5 + i * 20 + 18] = int_to_4bytes(now)[2]
    watch_p[5 + i * 20 + 19] = int_to_4bytes(now)[3]

# pack the glasses package, assuming that every package contains 10 data samples
glass_p = bytearray(105)
glass_p[0] = DEV_ID[0]
glass_p[1] = DEV_ID[1]
glass_p[2] = DEV_ID[2]
glass_p[3] = DEV_ID[3]
glass_p[4] = GLASS_TYPE
for i in range(10):
    now = int(time.time())
    glass_p[5 + i * 10] = short_to_bytes(accx)[0]
    glass_p[5 + i * 10 + 1] = short_to_bytes(accx)[1]
    glass_p[5 + i * 10 + 2] = short_to_bytes(accy)[0]
    glass_p[5 + i * 10 + 3] = short_to_bytes(accy)[1]
    glass_p[5 + i * 10 + 4] = short_to_bytes(accz)[0]
    glass_p[5 + i * 10 + 5] = short_to_bytes(accz)[1]
    glass_p[5 + i * 10 + 6] = int_to_4bytes(now)[0]
    glass_p[5 + i * 10 + 7] = int_to_4bytes(now)[1]
    glass_p[5 + i * 10 + 8] = int_to_4bytes(now)[2]
    glass_p[5 + i * 10 + 9] = int_to_4bytes(now)[3]

# pack the battery life package
battery_p = bytearray(6)
battery_p[0] = DEV_ID[0]
battery_p[1] = DEV_ID[1]
battery_p[2] = DEV_ID[2]
battery_p[3] = DEV_ID[3]
battery_p[4] = BATTERY_TYPE
battery_p[5] = BATTERY_LIFE

# initialize the socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0

# every second send a watch data package and a glasses package, every 5 minutes send a battery package
while True:
    sock.sendto(watch_p, (UDP_IP, UDP_PORT)) #Send message to UDP port
    time.sleep(0.5)
    sock.sendto(glass_p, (UDP_IP, UDP_PORT)) #Send message to UDP port
    time.sleep(0.5)
    i += 1
    if i % 300 == 0:
        sock.sendto(battery_p, (UDP_IP, UDP_PORT)) #Send message to UDP port
