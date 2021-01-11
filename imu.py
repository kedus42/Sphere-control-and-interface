from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()
xpos=0
ypos=0
zpos=0
calibration_values=[244, 255, 15, 0, 238, 255, 213, 0, 168, 254, 161, 252, 0, 0, 253, 255, 0, 0, 232, 3, 114, 3]
bno.set_calibration(calibration_values)
while True:
    sys, gyro, acc, mag = bno.get_calibration_status()
    print("sys calibration:", sys)
    print("gyro calibration:", gyro)
    print("acceleration calibration:", acc)
    print("magnetometer calibration:", mag)
    print(calibration_values)
    yaw, roll, pitch = bno.read_euler()
    xacc, yacc, zacc = bno.read_linear_acceleration()
    print("\n\nLatest readings:")
    print("Linear acceleration:", xacc, yacc, zacc)
    if xacc<0.2 and xacc>-0.2:
        xacc=0
    if yacc<0.2 and yacc>-0.2:
        yacc=0
    if zacc<0.2 and zacc>-0.2:
        zacc=0
    xpos+=xacc*.1*.1
    ypos+=yacc*.1*.1
    zpos+=zacc*.1*.1
    print("rpy:", roll, pitch, yaw)
    print("xyz position:", xpos, ypos, zpos)
    time.sleep(.1)