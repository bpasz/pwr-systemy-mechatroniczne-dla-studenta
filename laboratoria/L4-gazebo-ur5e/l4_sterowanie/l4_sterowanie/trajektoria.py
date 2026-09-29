"""Sposób 2: trajektoria w przestrzeni przegubów przez akcję FollowJointTrajectory.

Wysyła całą sekwencję pick & place jako jedną trajektorię z czasami punktów.
Kontroler interpoluje ruch i raportuje postęp (feedback) oraz wynik.
Parametry:
  kontroler   nazwa kontrolera trajektorii (domyślnie scaled_joint_trajectory_controller,
              aktywny po uruchomieniu ur_sim_control.launch.py)
  okres [s]   czas przejazdu między kolejnymi punktami
"""
import rclpy
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectoryPoint

from l4_sterowanie.wspolne import PRZEGUBY, sekwencja_przegubowa


def czas(sekundy: float) -> Duration:
    calkowite = int(sekundy)
    return Duration(sec=calkowite, nanosec=int((sekundy - calkowite) * 1e9))


class Trajektoria(Node):

    def __init__(self):
        super().__init__('trajektoria')
        self.declare_parameter('kontroler', 'scaled_joint_trajectory_controller')
        self.declare_parameter('okres', 3.0)
        kontroler = self.get_parameter('kontroler').value
        self.klient = ActionClient(self, FollowJointTrajectory, f'/{kontroler}/follow_joint_trajectory')
        self.ostatni_log = 0.0

    def wyslij(self):
        okres = self.get_parameter('okres').value
        cel = FollowJointTrajectory.Goal()
        cel.trajectory.joint_names = PRZEGUBY
        for i, (nazwa, q) in enumerate(sekwencja_przegubowa()):
            punkt = JointTrajectoryPoint(positions=q, velocities=[0.0] * len(q))
            punkt.time_from_start = czas((i + 1) * okres)
            cel.trajectory.points.append(punkt)

        self.get_logger().info('Czekam na serwer akcji...')
        if not self.klient.wait_for_server(timeout_sec=20.0):
            self.get_logger().error('Brak serwera akcji: czy kontroler jest aktywny?')
            return None
        self.get_logger().info(f'Wysyłam trajektorię: {len(cel.trajectory.points)} punktów')
        return self.klient.send_goal_async(cel, feedback_callback=self.postep)

    def postep(self, wiadomosc):
        fb = wiadomosc.feedback
        t = fb.actual.time_from_start.sec + fb.actual.time_from_start.nanosec * 1e-9
        if t - self.ostatni_log >= 1.0:           # log co ok. 1 s
            self.ostatni_log = t
            blad = max(abs(e) for e in fb.error.positions) if fb.error.positions else 0.0
            self.get_logger().info(f't = {t:5.1f} s, maks. błąd śledzenia = {blad:.4f} rad')


def main(args=None):
    rclpy.init(args=args)
    wezel = Trajektoria()
    przyszly = wezel.wyslij()
    if przyszly is not None:
        rclpy.spin_until_future_complete(wezel, przyszly)
        uchwyt = przyszly.result()
        if not uchwyt.accepted:
            wezel.get_logger().error('Cel odrzucony')
        else:
            wynik = uchwyt.get_result_async()
            rclpy.spin_until_future_complete(wezel, wynik)
            kod = wynik.result().result.error_code
            wezel.get_logger().info(f'Koniec, error_code = {kod} (0 = SUCCESSFUL)')
    wezel.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
