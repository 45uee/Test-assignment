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
        if vehicle.location.global_relative_frame.alt >= target_relative_altitude * 0.99:
            break
        time.sleep(1)


def goto(target_point):
    print("Go to target point")
    mode_pwm_values = {'ALT_HOLD': 2000}
    vehicle.channels.overrides['5'] = mode_pwm_values['ALT_HOLD']

    targetLat = int(target_point.lat * 1e7)
    targetLon = int(target_point.lon * 1e7)
    targetAlt = int(target_point.alt)

    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,
        targetLat,
        targetLon,
        targetAlt,
        0,
        0,
        0,
        0, 0, 0,
        0, 0)

    while True:
        vehicle.send_mavlink(msg)
        if round(vehicle.location.global_frame.lat, 5) == round(target_point.lat, 5):
            break


def yaw_rotation(yaw, mode="GUIDED"):
    vehicle.mode = VehicleMode(mode)

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

    vehicle.close()
