"""Zapisuje /joint_states do pliku CSV: t, q1..q6, v1..v6 (kolejność jak w wspolne.PRZEGUBY).

Użycie: ros2 run l4_sterowanie rejestrator --ros-args -p plik:=trajektoria.csv   (Ctrl+C kończy)
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from l4_sterowanie.wspolne import PRZEGUBY


class Rejestrator(Node):

    def __init__(self):
        super().__init__('rejestrator')
        self.declare_parameter('plik', 'przeguby.csv')
        sciezka = self.get_parameter('plik').value
        self.plik = open(sciezka, 'w', encoding='utf-8')
        naglowek = ['t'] + [f'q{i+1}' for i in range(6)] + [f'v{i+1}' for i in range(6)]
        self.plik.write(','.join(naglowek) + '\n')
        self.t0 = None
        self.create_subscription(JointState, '/joint_states', self.na_stan, 50)
        self.get_logger().info(f'Zapis do {sciezka}')

    def na_stan(self, msg: JointState):
        if not all(p in msg.name for p in PRZEGUBY):
            return
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        self.t0 = t if self.t0 is None else self.t0
        idx = [msg.name.index(p) for p in PRZEGUBY]
        q = [msg.position[i] for i in idx]
        v = [msg.velocity[i] if msg.velocity else 0.0 for i in idx]
        self.plik.write(','.join(f'{x:.5f}' for x in [t - self.t0] + q + v) + '\n')

    def destroy_node(self):
        self.plik.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    wezel = Rejestrator()
    try:
        rclpy.spin(wezel)
    except KeyboardInterrupt:
        pass
    finally:
        wezel.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
