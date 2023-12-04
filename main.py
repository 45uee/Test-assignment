from dronekit import connect

"""Connect to TCP port"""
vehicle = connect('tcp:127.0.0.1:5762')

vehicle_params = {
    "Mode": vehicle.mode.name,
    "Air speed": vehicle.airspeed,
    "Velocity:": vehicle.velocity,
    "Is Armed": vehicle.armed,
}

print("Connection check:", vehicle_params)


