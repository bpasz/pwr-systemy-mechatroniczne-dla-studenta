"""Sposób 1: zadawanie pozycji przegubów wprost (forward_position_controller).

Publikuje std_msgs/Float64MultiArray na /forward_position_controller/commands.
Parametry:
  okres [s]        czas między kolejnymi punktami sekwencji
  interpolacja     false: skok do kolejnego punktu; true: interpolacja liniowa 100 Hz
Wymaga aktywnego forward_position_controller (patrz README).
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

from l4_sterowanie.wspolne import sekwencja_przegubowa

CZESTOTLIWOSC = 100.0  # [Hz] dla trybu z interpolacją


class PozycjaWprost(Node):

    def __init__(self):
        super().__init__('pozycja_wprost')
        self.declare_parameter('okres', 3.0)
        self.declare_parameter('interpolacja', False)
        self.pub = self.create_publisher(Float64MultiArray, '/forward_position_controller/commands', 10)
        self.sekwencja = sekwencja_przegubowa()
        self.indeks = 0
        self.t = 0.0
        self.create_timer(1.0 / CZESTOTLIWOSC, self.krok)
        self.get_logger().info(f'Sekwencja {len(self.sekwencja)} punktów, '
                               f'interpolacja={self.get_parameter("interpolacja").value}')

    def krok(self):
        okres = self.get_parameter('okres').value
        if self.indeks >= len(self.sekwencja):
            return
        nazwa, q_cel = self.sekwencja[self.indeks]
        if self.get_parameter('interpolacja').value and self.indeks > 0:
            _, q_pop = self.sekwencja[self.indeks - 1]
            s = min(1.0, self.t / okres)
            q = [a + s * (b - a) for a, b in zip(q_pop, q_cel)]
        else:
            q = q_cel
        self.pub.publish(Float64MultiArray(data=q))

        if self.t == 0.0:
            self.get_logger().info(f'-> {nazwa}')
        self.t += 1.0 / CZESTOTLIWOSC
        if self.t >= okres:
            self.t = 0.0
            self.indeks += 1
            if self.indeks == len(self.sekwencja):
                self.get_logger().info('Sekwencja zakończona')


def main(args=None):
    rclpy.init(args=args)
    wezel = PozycjaWprost()
    try:
        rclpy.spin(wezel)
    except KeyboardInterrupt:
        pass
    finally:
        wezel.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
