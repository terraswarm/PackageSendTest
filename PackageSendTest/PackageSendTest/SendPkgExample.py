import socket
import time
import datetime


# convert short int to 2 bytes array
def short_to_bytes(n):
    n = int(n)
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


# convert int to 6 bytes array
def timestamp_2_bytes(n):
    b = bytearray([0, 0, 0, 0, 0, 0])   # init
    milisce = n % 1000
    n /= 1000
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    n >>= 8
    b[2] = n & 0xFF
    n >>= 8
    b[3] = n & 0xFF
    b[4] = milisce & 0xFF
    milisce >>= 8
    b[5] = milisce & 0xFF
    return b


# convert string date time to long int timestamp
def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000
        return int(timeStamp)
    except ValueError as e:
        print e
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000
        return timeStamp

# the ip address of the server
UDP_IP = '128.32.38.101'
# tge socket port number
UDP_PORT = 4567

# package head info -- Device data and Package type
DEV_ID = "9096"
WATCH_TYPE = 'w'
GLASS_TYPE = 'g'
ENVIRONMENT_TYPE = 'e'
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
PRESSURE = 999.7
HUMIDITY = 56.1
TEMPARATURE = 24.5
UV = 0.0
AMBIENT_LIGHT = 86.2
BATTERY_LIFE = 90

# convert the original data to the format the data body requires
accx = int(ACCx * 10000)
accy = int(ACCy * 10000)
accz = int(ACCz * 10000)
gyrx = int(GYRx * 10000)
gyry = int(GYRy * 10000)
gyrz = int(GYRz * 10000)

# pack the watch IMU and PPG data package, assuming that every package contains 10 data samples
watch_p = bytearray(22 * 10 + 4 + 1)
watch_p[0] = DEV_ID[0]
watch_p[1] = DEV_ID[1]
watch_p[2] = DEV_ID[2]
watch_p[3] = DEV_ID[3]
watch_p[4] = WATCH_TYPE
for i in range(10):
    now = string2timestamp(str(datetime.datetime.now()))
    watch_p[5 + i * 22] = short_to_bytes(accx)[0]
    watch_p[5 + i * 22 + 1] = short_to_bytes(accx)[1]
    watch_p[5 + i * 22 + 2] = short_to_bytes(accy)[0]
    watch_p[5 + i * 22 + 3] = short_to_bytes(accy)[1]
    watch_p[5 + i * 22 + 4] = short_to_bytes(accz)[0]
    watch_p[5 + i * 22 + 5] = short_to_bytes(accz)[1]
    watch_p[5 + i * 22 + 6] = short_to_bytes(gyrx)[0]
    watch_p[5 + i * 22 + 7] = short_to_bytes(gyrx)[1]
    watch_p[5 + i * 22 + 8] = short_to_bytes(gyry)[0]
    watch_p[5 + i * 22 + 9] = short_to_bytes(gyry)[1]
    watch_p[5 + i * 22 + 10] = short_to_bytes(gyrz)[0]
    watch_p[5 + i * 22 + 11] = short_to_bytes(gyrz)[1]
    watch_p[5 + i * 22 + 12] = int_to_3bytes(PPG)[0]
    watch_p[5 + i * 22 + 13] = int_to_3bytes(PPG)[1]
    watch_p[5 + i * 22 + 14] = int_to_3bytes(PPG)[2]
    watch_p[5 + i * 22 + 15] = (HR & 0xFF)
    watch_p[5 + i * 22 + 16] = timestamp_2_bytes(now)[0]
    watch_p[5 + i * 22 + 17] = timestamp_2_bytes(now)[1]
    watch_p[5 + i * 22 + 18] = timestamp_2_bytes(now)[2]
    watch_p[5 + i * 22 + 19] = timestamp_2_bytes(now)[3]
    watch_p[5 + i * 22 + 20] = timestamp_2_bytes(now)[4]
    watch_p[5 + i * 22 + 21] = timestamp_2_bytes(now)[5]
    # import binascii
    # print "watch_p: ", watch_p[5+i*22+16:5+i*22+21]
    # print binascii.hexlify(watch_p[5+i*22+16:5+i*22+18])
    # print binascii.hexlify(watch_p[5+i*22+16:5+i*22+23])

# pack the glasses acceleration package, assuming that every package contains 10 data samples
glass_p = bytearray(12 * 10 + 4 + 1)
glass_p[0] = DEV_ID[0]
glass_p[1] = DEV_ID[1]
glass_p[2] = DEV_ID[2]
glass_p[3] = DEV_ID[3]
glass_p[4] = GLASS_TYPE
for i in range(10):
    now = string2timestamp(str(datetime.datetime.now()))
    # print datetime.datetime.now(), time.clock(), now
    glass_p[5 + i * 12] = short_to_bytes(accx)[0]
    glass_p[5 + i * 12 + 1] = short_to_bytes(accx)[1]
    glass_p[5 + i * 12 + 2] = short_to_bytes(accy)[0]
    glass_p[5 + i * 12 + 3] = short_to_bytes(accy)[1]
    glass_p[5 + i * 12 + 4] = short_to_bytes(accz)[0]
    glass_p[5 + i * 12 + 5] = short_to_bytes(accz)[1]
    glass_p[5 + i * 12 + 6] = timestamp_2_bytes(now)[0]
    glass_p[5 + i * 12 + 7] = timestamp_2_bytes(now)[1]
    glass_p[5 + i * 12 + 8] = timestamp_2_bytes(now)[2]
    glass_p[5 + i * 12 + 9] = timestamp_2_bytes(now)[3]
    glass_p[5 + i * 12 + 10] = timestamp_2_bytes(now)[4]
    glass_p[5 + i * 12 + 11] = timestamp_2_bytes(now)[5]

# pack the glasses environment package, assuming that every package contains 10 data samples
environment_p = bytearray(16 * 10 + 4 + 1)
environment_p[0] = DEV_ID[0]
environment_p[1] = DEV_ID[1]
environment_p[2] = DEV_ID[2]
environment_p[3] = DEV_ID[3]
environment_p[4] = ENVIRONMENT_TYPE
for i in range(10):
    now = string2timestamp(str(datetime.datetime.now()))
    environment_p[5 + i * 16] = short_to_bytes((PRESSURE - 250) * 65535 / 860)[0]
    environment_p[5 + i * 16 + 1] = short_to_bytes((PRESSURE - 250) * 65535 / 860)[1]
    environment_p[5 + i * 16 + 2] = short_to_bytes(HUMIDITY * 64 + 896)[0]
    environment_p[5 + i * 16 + 3] = short_to_bytes(HUMIDITY * 64 + 896)[1]
    environment_p[5 + i * 16 + 4] = short_to_bytes(TEMPARATURE * 50 + 2096)[0]
    environment_p[5 + i * 16 + 5] = short_to_bytes(TEMPARATURE * 50 + 2096)[1]
    environment_p[5 + i * 16 + 6] = short_to_bytes(UV * 38.8)[0]
    environment_p[5 + i * 16 + 7] = short_to_bytes(UV * 38.8)[1]
    environment_p[5 + i * 16 + 8] = short_to_bytes(AMBIENT_LIGHT * 0.8525)[0]
    environment_p[5 + i * 16 + 9] = short_to_bytes(AMBIENT_LIGHT * 0.8525)[1]
    environment_p[5 + i * 16 + 10] = timestamp_2_bytes(now)[0]
    environment_p[5 + i * 16 + 11] = timestamp_2_bytes(now)[1]
    environment_p[5 + i * 16 + 12] = timestamp_2_bytes(now)[2]
    environment_p[5 + i * 16 + 13] = timestamp_2_bytes(now)[3]
    environment_p[5 + i * 16 + 14] = timestamp_2_bytes(now)[4]
    environment_p[5 + i * 16 + 15] = timestamp_2_bytes(now)[5]

# pack the watch battery life package
battery_p = bytearray(12)
now = string2timestamp(str(datetime.datetime.now()))
battery_p[0] = DEV_ID[0]
battery_p[1] = DEV_ID[1]
battery_p[2] = DEV_ID[2]
battery_p[3] = DEV_ID[3]
battery_p[4] = BATTERY_TYPE
battery_p[5] = BATTERY_LIFE
battery_p[6] = timestamp_2_bytes(now)[0]
battery_p[7] = timestamp_2_bytes(now)[1]
battery_p[8] = timestamp_2_bytes(now)[2]
battery_p[9] = timestamp_2_bytes(now)[3]
battery_p[10] = timestamp_2_bytes(now)[4]
battery_p[11] = timestamp_2_bytes(now)[5]

# initialize the socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0

# every second send a watch data package and a glasses package, every 5 minutes send a battery package
while True:
    sock.sendto(watch_p, (UDP_IP, UDP_PORT))  # Send message to UDP port
    time.sleep(0.5)
    sock.sendto(glass_p, (UDP_IP, UDP_PORT))  # Send message to UDP port
    time.sleep(0.5)
    i += 1
    if i % 300 == 0:
        sock.sendto(battery_p, (UDP_IP, UDP_PORT))  # Send watch battery every 5 min
    if i % 60 == 0:
        sock.sendto(environment_p, (UDP_IP, UDP_PORT))  # send environment data every 1 min
