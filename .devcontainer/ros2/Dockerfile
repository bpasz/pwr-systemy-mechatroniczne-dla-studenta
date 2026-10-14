# ROS 2 Jazzy + Gazebo Harmonic + symulacja UR5e (L3, L4) dla GitHub Codespaces.
# Pulpit graficzny (noVNC na porcie 6080) dodaje cecha desktop-lite z devcontainer.json.
FROM osrf/ros:jazzy-desktop

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-jazzy-turtlesim \
        ros-jazzy-rqt-graph \
        ros-jazzy-ros-gz \
        ros-jazzy-ur \
        ros-jazzy-ur-simulation-gz \
        python3-matplotlib python3-numpy \
        python3-colcon-common-extensions \
        mesa-utils sudo git bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Użytkownik „ubuntu” (uid 1000) jest w obrazie Ubuntu 24.04; dajemy mu sudo bez hasła.
RUN echo "ubuntu ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu \
    && echo "source /opt/ros/jazzy/setup.bash" >> /home/ubuntu/.bashrc \
    && echo '[ -f ~/ros2_ws/install/setup.bash ] && source ~/ros2_ws/install/setup.bash' >> /home/ubuntu/.bashrc
