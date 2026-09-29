"""Wirtualny czujnik odległości żółwia od prawej ściany turtlesim.

Subskrybuje: /turtle1/pose (turtlesim/msg/Pose)
Publikuje:   /odleglosc   (std_msgs/msg/Float32), z szumem pomiarowym, 20 Hz
Parametry:   szum (odchylenie standardowe [m]), czestotliwosc [Hz]
"""
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from turtlesim.msg import Pose

POLOZENIE_SCIANY = 11.088889  # prawa krawędź okna turtlesim [m]


class Czujnik(Node):

    def __init__(self):
        super().__init__('czujnik')
        self.declare_parameter('szum', 0.02)
        self.declare_parameter('czestotliwosc', 20.0)
        self.x = None
        self.create_subscription(Pose, 'turtle1/pose', self.na_poze, 10)
        self.pub = self.create_publisher(Float32, 'odleglosc', 10)
        okres = 1.0 / self.get_parameter('czestotliwosc').value
        self.create_timer(okres, self.pomiar)
        self.get_logger().info('Czujnik odległości uruchomiony')

    def na_poze(self, msg: Pose):
        self.x = msg.x

    def pomiar(self):
        if self.x is None:          # jeszcze nie znamy położenia żółwia
            return
        szum = self.get_parameter('szum').value
        odleglosc = POLOZENIE_SCIANY - self.x + random.gauss(0.0, szum)
        self.pub.publish(Float32(data=float(odleglosc)))


def main(args=None):
    rclpy.init(args=args)
    wezel = Czujnik()
    try:
        rclpy.spin(wezel)
    except KeyboardInterrupt:
        pass
    finally:
        wezel.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
