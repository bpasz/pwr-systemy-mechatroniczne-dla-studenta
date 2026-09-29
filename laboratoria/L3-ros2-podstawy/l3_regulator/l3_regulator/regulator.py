"""Regulator PI utrzymujący zadaną odległość żółwia od ściany.

Subskrybuje: /odleglosc        (std_msgs/msg/Float32)
Publikuje:   /turtle1/cmd_vel  (geometry_msgs/msg/Twist)
Usługa:      /regulator/wlacz  (std_srvs/srv/SetBool): włącza i wyłącza regulację
Parametry:   zadana [m], Kp, Ki, v_max [m/s]  (zmiana w locie: ros2 param set)
"""
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import SetBool


class Regulator(Node):

    def __init__(self):
        super().__init__('regulator')
        self.declare_parameter('zadana', 2.0)
        self.declare_parameter('Kp', 1.0)
        self.declare_parameter('Ki', 0.0)
        self.declare_parameter('v_max', 2.0)
        self.wlaczony = True
        self.calka = 0.0
        self.ostatni_czas = None
        self.create_subscription(Float32, 'odleglosc', self.na_pomiar, 10)
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.create_service(SetBool, '~/wlacz', self.na_wlacz)
        self.get_logger().info('Regulator gotowy')

    def na_wlacz(self, zadanie: SetBool.Request, odpowiedz: SetBool.Response):
        self.wlaczony = zadanie.data
        self.calka = 0.0
        if not self.wlaczony:
            self.pub.publish(Twist())          # zatrzymaj żółwia
        odpowiedz.success = True
        odpowiedz.message = 'regulacja włączona' if self.wlaczony else 'regulacja wyłączona'
        return odpowiedz

    def na_pomiar(self, msg: Float32):
        if not self.wlaczony:
            return
        teraz = self.get_clock().now().nanoseconds * 1e-9
        dt = 0.0 if self.ostatni_czas is None else teraz - self.ostatni_czas
        self.ostatni_czas = teraz

        zadana = self.get_parameter('zadana').value
        kp = self.get_parameter('Kp').value
        ki = self.get_parameter('Ki').value
        v_max = self.get_parameter('v_max').value

        # Uchyb > 0: jesteśmy za daleko od ściany -> jedź do przodu (w stronę ściany).
        uchyb = msg.data - zadana
        u = kp * uchyb + ki * self.calka
        if abs(u) < v_max:                     # anti-windup: całkuj tylko bez nasycenia
            self.calka += uchyb * dt
        u = max(-v_max, min(v_max, u))

        cmd = Twist()
        cmd.linear.x = u
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    wezel = Regulator()
    try:
        rclpy.spin(wezel)
    except KeyboardInterrupt:
        pass
    finally:
        wezel.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
