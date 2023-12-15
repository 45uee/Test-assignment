# Test-assignment
Solution for test assignment
## Run script
1) Clone repository.
2) Install dronekit:
   ```bash
   pip install dronekit
   ```
3) Run main.py
   ```bash
   py main.py
   ```
Main Functionality
The script defines three main functions to control the drone:

1. `takeoff(target_relative_altitude, mode="GUIDED")`
This function sets the vehicle mode to "GUIDED", initiates arming and takeoff. The function run until the drone reaches defined altitude.

2. `goto(target_point, mode="GUIDED")`
This function directs the drone to a specified global location (target_point). It sets the vehicle mode to "GUIDED". Holding previous altitude.

3. `yaw_rotation(yaw)`
This function performs a yaw rotation by sending a MAVLink command.
