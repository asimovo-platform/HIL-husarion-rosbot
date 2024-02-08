FROM docker.io/osrf/ros:foxy-desktop
ENV ROS_DISTRO=foxy
RUN echo "ROS_DISTRO=foxy" >> /etc/bash.bashrc
RUN echo "source /opt/ros/foxy/setup.bash" >> /etc/bash.bashrc
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 4B63CF8FDE49746E98FA01DDAD19BAB3CBF125EA

# Install Apt packages
RUN apt-get update -y && apt-get install -y emacs less nano vim python3-pip && apt-get -y clean
RUN python3 -m pip install --upgrade pip && python3 -m pip cache purge

# Install Gazebo Citadel
RUN apt-get update -y && apt-get install -y lsb-release wget gnupg && apt-get -y clean
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN apt-get update -y && apt-get install -y ignition-citadel  && apt-get -y clean
COPY ./gazebo-websocket/websocket.ign /opt/gazebo-websocket/websocket.ign

# Install Foxglove websocket
#RUN apt-get update -y && apt-get install -y ros-foxy-foxglove-bridge
RUN python3 -m pip install foxglove-websocket   && python3 -m pip cache purge

# Install necessary ROS2 Foxy packages
RUN apt-get update -y && apt-get install -y ros-foxy-foxglove-msgs ros-foxy-rosbridge-server  && apt-get -y clean
RUN apt-get update -y && apt-get install -y ros-foxy-rmw-cyclonedds-cpp ros-foxy-cyclonedds && apt-get -y clean #cyclonedds-tools
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp 
RUN echo "RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /etc/bash.bashrc
 #Dynamic Add-Ons

    # Necessary ROS2 packages 
    RUN apt-get update -y && apt-get install -y ros-foxy-ros-ign ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-xacro ros-foxy-robot-localization ros-foxy-joint-state-publisher ros-foxy-ros2-control ros-foxy-ros2-controllers && apt-get -y clean
    
    #Install gz_ros2_control Add-On
    ENV IGNITION_VERSION=citadel
    WORKDIR /opt/addons/ros/gz_ros2_control_ws/src
    RUN git clone -b foxy https://github.com/ros-controls/gz_ros2_control
    RUN rosdep install -r --from-paths . --ignore-src --rosdistro foxy -y
    WORKDIR /opt/addons/ros/gz_ros2_control_ws
    RUN . /opt/ros/foxy/setup.sh && \
    	colcon build
    RUN echo "source /opt/addons/ros/gz_ros2_control_ws/install/setup.bash" >> /etc/bash.bashrc
    
    #Data Science Add-Ons
    RUN python3 -m pip --default-timeout=600 install aesara scipy numpy  pandas matplotlib opencv-python && python3 -m pip cache purge
    
     #Machine learning Add-Ons
    #RUN python3 -m pip --default-timeout=600 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu  && python3 -m pip cache purge
    #RUN python3 -m pip --default-timeout=600 install tensorflow scikit-learn && python3 -m pip cache purge
    #RUN apt-get update && apt-get install -y swig  && apt-get -y clean
    #RUN python3 -m pip --default-timeout=600 install gymnasium[all] && python3 -m pip cache purge 
    
    #Open-CV c++ (Data science add-ons)
    #RUN apt-get update && apt-get install -y g++ cmake make git libgtk2.0-dev pkg-config  && apt-get -y clean
    #RUN apt-get update && apt-get install -y libopencv-dev && apt-get -y clean
    #RUN apt-get install libcanberra-gtk-module libcanberra-gtk3-module -y && apt-get -y clean #For avoiding error: Failed to load module "canberra-gtk-module"

# Add asimovo user
RUN adduser asimovo --uid 1000 --disabled-password --gecos "User account for the user of the Asimovo Platform"
RUN echo asimovo:p@ssw0rd | chpasswd
RUN usermod -aG sudo asimovo
COPY ./etc/sudoers /etc/sudoers
RUN chown root:root /etc/sudoers
RUN chmod 440 /etc/sudoers
 
# Install OpenSSH
RUN apt-get -y install openssh-server  && apt-get -y clean
COPY ./etc/sshd_config /etc/ssh/sshd_config
RUN mkdir /run/sshd

RUN python3 -m pip install setuptools==58.2.0 && python3 -m pip cache purge

RUN apt-get update && apt-get install software-properties-common -y
RUN echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-get install -y curl
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt-get update
RUN apt-get update && apt-get install -y ros-noetic-desktop-full
RUN apt-get install -y git
RUN apt-get install -y net-tools
RUN apt-get install -y vim
RUN apt-get install -y netcat
RUN apt-get install -y iputils-ping
WORKDIR /
WORKDIR /
RUN git clone https://github.com/libuvc/libuvc -b v0.0.6 
WORKDIR /libuvc/build
RUN cmake ..
RUN make && make install
WORKDIR /

RUN apt-get remove -y ros-noetic-controller-manager-msgs
RUN apt-get remove -y ros-foxy-controller-manager-msgs
RUN apt-get purge ros-noetic-controller-manager-msgs
RUN apt-get purge ros-foxy-controller-manager-msgs
#RUN . /opt/ros/foxy/setup.bash && apt-get update
WORKDIR /ros2_ws/src
RUN git clone -b foxy https://github.com/ros2/ros1_bridge.git
WORKDIR /ros2_ws
RUN . /opt/ros/noetic/setup.sh && . /opt/ros/foxy/setup.sh && colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure
RUN apt-get install -y ros-noetic-controller-manager-msgs
RUN apt-get install -y ros-foxy-controller-manager-msgs
RUN apt-get update -y && apt-get install -y lsb-release wget gnupg && apt-get -y clean
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN apt-get update -y && apt-get install -y ignition-citadel  && apt-get -y clean
RUN apt-get update -y && apt-get install -y ros-foxy-ros-ign ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-xacro ros-foxy-robot-localization ros-foxy-joint-state-publisher ros-foxy-ros2-control ros-foxy-ros2-controllers && apt-get -y clean
RUN apt-get update -y && apt-get install -y ignition-fortress


# Configure launch
WORKDIR /
RUN apt-get -y install tini && apt-get -y clean
RUN python3 -m pip install honcho && python3 -m pip cache purge
COPY ./Procfile /Procfile
ENTRYPOINT [ "/usr/bin/tini", "--","honcho", "start" ]
