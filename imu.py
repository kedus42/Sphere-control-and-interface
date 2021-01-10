from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()
xpos=0
ypos=0
zpos=0
while True:
    sys, gyro, acc, mag = bno.get_calibration_status()
    print("sys calibration:", sys)
    print("gyro calibration:", gyro)
    print("acceleration calibration:", acc)
    print("magnetometer calibration:", mag)
    yaw, roll, pitch = bno.read_euler()
    zacc, xacc, yacc = bno.linear_acceleration()
    xpos+=xacc*xacc
    ypos+=yacc*yacc
    zpos+=zacc*zacc
    print("\n\nLatest readings:")
    print("Linear acceleration:", xacc, yacc, zacc)
    print("rpy:", roll, pitch, yaw)
    print("xyz position:", xpos, ypos, zpos)
    calibration_values=bno.get_calibration()
    time.sleep(1)