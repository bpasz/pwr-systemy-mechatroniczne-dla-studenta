"""Uruchamia turtlesim + wirtualny czujnik + regulator z parametrami.

Użycie:  ros2 launch l3_regulator uklad.launch.py zadana:=3.0 Kp:=1.5
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    zadana = LaunchConfiguration('zadana')
    kp = LaunchConfiguration('Kp')
    ki = LaunchConfiguration('Ki')
    return LaunchDescription([
        DeclareLaunchArgument('zadana', default_value='2.0', description='Zadana odległość od ściany [m]'),
        DeclareLaunchArgument('Kp', default_value='1.0', description='Wzmocnienie proporcjonalne'),
        DeclareLaunchArgument('Ki', default_value='0.0', description='Wzmocnienie całkujące'),
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='l3_regulator', executable='czujnik', name='czujnik',
             parameters=[{'szum': 0.02}]),
        Node(package='l3_regulator', executable='regulator', name='regulator',
             parameters=[{'zadana': zadana, 'Kp': kp, 'Ki': ki}]),
    ])
