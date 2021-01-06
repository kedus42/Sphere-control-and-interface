from Adafruit_BNO055 import BNO055
import time

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()
while True:
    sys, gyro, acc, mag = bno.get_calibration_status()
    print("sys calibration:", sys)
    print("gyro calibration:", gyro)
    print("acceleration calibration:", acc)
    print("magnetometer calibration:", mag)
    yaw, roll, pitch = bno.read_euler()
    print("\n\nLatest readings:")
    #print("Linear acceleration (m/s^2): {}".format(bno.linear_acceleration))
    print("rpy:", roll, pitch, yaw)
    time.sleep(1)