from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
from pymavlink import mavutil

"""Solution for test assignment"""


def takeoff(target_relative_altitude, mode="GUIDED"):
    vehicle.mode = VehicleMode(mode)

    target_relative_altitude += vehicle.location.global_relative_frame.alt
    vehicle.armed = True

    while not vehicle.armed:
        time.sleep(1)

    print("Take off")
    vehicle.simple_takeoff(target_relative_altitude)
    while True:
        if vehicle.location.global_relative_frame.alt >= target_relative_altitude:
            break
        time.sleep(1)


def goto(target_point, mode="GUIDED"):
    print("Go to second point")
    vehicle.mode = VehicleMode(mode)
    while True:
        vehicle.simple_goto(target_point)
        if round(vehicle.location.global_frame.lat, 5) == round(target_point.lat, 5):
            break


def yaw_rotation(yaw):
    print("Yaw rotation")
    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        yaw,
        0,
        0,
        0,
        0,
        0,
        0
    )
    vehicle.send_mavlink(msg)


if __name__ == "__main__":
    vehicle = connect('tcp:127.0.0.1:5762')
    vehicle.airspeed = 20

    point_a = LocationGlobal(50.450739, 30.461242, 0.0)
    point_b = LocationGlobal(50.443326, 30.448078, 260.0)
    vehicle.home_location = point_a
    target_yaw = 350

    takeoff(100)
    goto(point_b)
    yaw_rotation(target_yaw)

    # vehicle.mode = VehicleMode("RTL")
    vehicle.close()
