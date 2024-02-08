#!/bin/bash

docker run -it \
    --rm \
    -v /dev/bus/usb:/dev/bus/usb \
    -v <route_to_project>/husarion_ws_two:/husarion_ws_two \
    -v <route_to_project>/ros2_pkgs_ws:/ros2_pkgs_ws \
    -v /dev/input:/dev/input \
    --device-cgroup-rule 'a 13:* rwm' \
    --device-cgroup-rule 'a 189:* rwm' \
    --device="/dev/mem:/dev/mem" \
    -p 46335:46335 \
    -p 13351:13351 \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XAUTHORITY:$XAUTHORITY" \
    --env="XAUTHORITY=$XAUTHORITY" \
    --runtime=nvidia \
    --net=host \
    --env="NVIDIA_DRIVER_CAPABILITIES=all" \
    --gpus all \
    --name="hil_setup_noetic_foxy" \
    hil_setup_noetic_foxy
