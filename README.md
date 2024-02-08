This repository contains the codebase of the Hardware-in-the-loop developer case study project. The documentation is available at https://asimovo.gitbook.io/hardware-in-the-loop/

The packages inside the husarion_ws_two repository were copied from the system of the Husarion ROSbot 2 robot. Information about the creator and the licences of these packages are available in their respective folders. A few small modifications were made consisting of:
   
- Setting the use_sim_time parameter true in the all.launch launchfile of the rosbot_ekf package
- Commenting out the launching of astra camera and rplidar in rosbot_drivers.launch of the husarion_ros package. 
