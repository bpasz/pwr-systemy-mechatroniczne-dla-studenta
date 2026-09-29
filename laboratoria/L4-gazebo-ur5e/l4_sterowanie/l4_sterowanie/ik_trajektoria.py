"""Sposób 3: punkty kartezjańskie -> kinematyka odwrotna MoveIt (/compute_ik) -> trajektoria.

Wymaga uruchomionego MoveIt: ros2 launch ur_simulation_gz ur_sim_moveit.launch.py
Dla każdego punktu (x, y, z) z wspolne.PUNKTY_KARTEZJANSKIE wyznacza konfigurację przegubów
(narzędzie tool0 skierowane w dół, sprawdzanie kolizji), startując z poprzedniego rozwiązania,
a następnie wysyła całą sekwencję do kontrolera trajektorii (jak węzeł `trajektoria`).
Parametry:
  tylko_ik    true: tylko wypisz konfiguracje (np. do uzupełnienia wspolne.KONFIGURACJE_IK)
  grupa       grupa planowania MoveIt (ur_manipulator)
"""
import math

import rclpy
from geometry_msgs.msg import PoseStamped
from moveit_msgs.srv import GetPositionIK
from rclpy.node import Node
from sensor_msgs.msg import JointState

from l4_sterowanie import wspolne
from l4_sterowanie.trajektoria import Trajektoria


def najblizszy_odpowiednik(q, odniesienie):
    """Zamienia każdy kąt na równoważny (q + 2*pi*k) najbliższy odniesieniu.

    Przeguby UR mają zakres ±2π, więc IK może zwrócić np. 4,2 rad zamiast -2,08 rad.
    Bez tej poprawki robot wykonywałby niepotrzebne obroty o prawie pełny kąt.
    """
    return [x + 2 * math.pi * round((r - x) / (2 * math.pi)) for x, r in zip(q, odniesienie)]


class KinematykaOdwrotna(Node):

    def __init__(self):
        super().__init__('ik_trajektoria')
        self.declare_parameter('tylko_ik', False)
        self.declare_parameter('grupa', 'ur_manipulator')
        self.stan = None
        self.create_subscription(JointState, '/joint_states', self.na_stan, 10)
        self.klient = self.create_client(GetPositionIK, '/compute_ik')

    def na_stan(self, msg: JointState):
        self.stan = msg

    def oblicz_ik(self, xyz, ziarno: JointState):
        zadanie = GetPositionIK.Request()
        zadanie.ik_request.group_name = self.get_parameter('grupa').value
        zadanie.ik_request.robot_state.joint_state = ziarno
        zadanie.ik_request.avoid_collisions = True
        zadanie.ik_request.ik_link_name = 'tool0'
        poza = PoseStamped()
        poza.header.frame_id = 'base_link'
        poza.pose.position.x, poza.pose.position.y, poza.pose.position.z = xyz
        # Obrót o 180° wokół osi x: oś z narzędzia skierowana w dół.
        poza.pose.orientation.x, poza.pose.orientation.y = 1.0, 0.0
        poza.pose.orientation.z, poza.pose.orientation.w = 0.0, 0.0
        zadanie.ik_request.pose_stamped = poza
        zadanie.ik_request.timeout.sec = 1
        przyszly = self.klient.call_async(zadanie)
        rclpy.spin_until_future_complete(self, przyszly)
        odp = przyszly.result()
        if odp.error_code.val != 1:                       # 1 = SUCCESS
            raise RuntimeError(f'IK nie znalazła rozwiązania dla {xyz} (kod {odp.error_code.val})')
        return odp.solution.joint_state

    def wyznacz_konfiguracje(self):
        while self.stan is None or not self.klient.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Czekam na /joint_states i usługę /compute_ik (MoveIt)...')
            rclpy.spin_once(self, timeout_sec=1.0)
        # Start z konfiguracji "dom": deterministyczny wybór gałęzi rozwiązania IK.
        q_poprz = dict(wspolne.SEKWENCJA)['dom']
        wynik = {}
        for nazwa, xyz in wspolne.PUNKTY_KARTEZJANSKIE.items():
            ziarno = JointState(name=wspolne.PRZEGUBY, position=q_poprz)
            rozw = self.oblicz_ik(xyz, ziarno)
            q = [rozw.position[rozw.name.index(p)] for p in wspolne.PRZEGUBY]
            q = najblizszy_odpowiednik(q, q_poprz)
            wynik[nazwa] = [round(v, 4) for v in q]
            self.get_logger().info(f'{nazwa:13s} {xyz} -> q = {wynik[nazwa]}')
            q_poprz = q                                    # ciągłość gałęzi rozwiązania
        return wynik


def main(args=None):
    rclpy.init(args=args)
    ik = KinematykaOdwrotna()
    wspolne.KONFIGURACJE_IK.update(ik.wyznacz_konfiguracje())
    tylko_ik = ik.get_parameter('tylko_ik').value
    ik.destroy_node()
    if not tylko_ik:
        wezel = Trajektoria()
        przyszly = wezel.wyslij()
        if przyszly is not None:
            rclpy.spin_until_future_complete(wezel, przyszly)
            uchwyt = przyszly.result()
            if uchwyt.accepted:
                wynik = uchwyt.get_result_async()
                rclpy.spin_until_future_complete(wezel, wynik)
                wezel.get_logger().info(f'Koniec, error_code = {wynik.result().result.error_code}')
        wezel.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
