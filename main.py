from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
from pymavlink import mavutil

"""Solution for test assignment"""

"""Connect to TCP port"""
vehicle = connect('tcp:127.0.0.1:5762')

vehicle_params = {
    "Mode": vehicle.mode.name,
    "Air speed": vehicle.airspeed,
    "Velocity:": vehicle.velocity,
    "Is Armed": vehicle.armed,
}


print("Connection check:", vehicle_params)

"""Point A"""
home_point = LocationGlobal(50.450739, 30.461242, 0.0)
second_point = LocationGlobal(50.443326, 30.448078, 260.0)
home_point.alt = 0.0
vehicle.home_location = home_point

vehicle.airspeed = 11
target_yaw = 350


# Arm and take off to a specified altitude
def arm_and_takeoff(target_altitude):
    target_altitude += 160
    vehicle.armed = True

    while not vehicle.armed:
        print("Arming")
        time.sleep(1)

    vehicle.simple_takeoff(target_altitude)

    while True:
        if vehicle.location.global_relative_frame.alt >= target_altitude:
            break
        time.sleep(1)


def goto(target_point):
    while True:
        vehicle.simple_goto(target_point)
        if round(vehicle.location.global_frame.lat, 5) == round(target_point.lat, 5):
            break


def yaw_rotation(yaw):
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        yaw,  # param 1, yaw in degrees
        0,  # param 2, pitch
        0,  # param 3, roll
        0,  # param 4, relative offset
        0,  # param 5, absolute offset
        0,  # param 6, speed
        0   # param 7, auto continue
    )
    vehicle.send_mavlink(msg)


if __name__ == "__main__":
    vehicle.mode = VehicleMode("GUIDED")

    arm_and_takeoff(100)
    goto(second_point)
    yaw_rotation(target_yaw)

    #time.sleep(10)
    #print("Returning to launch")
    #vehicle.mode("RTL")
    vehicle.close()
