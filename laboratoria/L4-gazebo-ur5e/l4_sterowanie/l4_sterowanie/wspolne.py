"""Wspólne definicje dla węzłów L4: nazwy przegubów UR5e i sekwencja „pick & place”."""

PRZEGUBY = [
    'shoulder_pan_joint',
    'shoulder_lift_joint',
    'elbow_joint',
    'wrist_1_joint',
    'wrist_2_joint',
    'wrist_3_joint',
]

# Sekwencja w przestrzeni przegubów [rad]. Chwytak (tool0) skierowany w dół.
# Wartości wyznaczono kinematyką odwrotną MoveIt (/compute_ik) dla punktów
# kartezjańskich z PUNKTY_KARTEZJANSKIE (patrz ik_trajektoria.py).
SEKWENCJA = [
    ('dom',            [0.0, -1.5708, 1.5708, -1.5708, -1.5708, 0.0]),
    ('nad_obiektem',   None),   # uzupełniane z KONFIGURACJE_IK
    ('chwyt',          None),
    ('nad_obiektem',   None),
    ('nad_celem',      None),
    ('odlozenie',      None),
    ('nad_celem',      None),
    ('dom',            [0.0, -1.5708, 1.5708, -1.5708, -1.5708, 0.0]),
]

# Punkty kartezjańskie (x, y, z) [m] w układzie base_link dla narzędzia tool0.
PUNKTY_KARTEZJANSKIE = {
    'nad_obiektem': (0.45, 0.20, 0.30),
    'chwyt':        (0.45, 0.20, 0.12),
    'nad_celem':    (0.30, -0.35, 0.30),
    'odlozenie':    (0.30, -0.35, 0.15),
}

# Wynik /compute_ik dla powyższych punktów (ur5e, orientacja "narzędzie w dół", start z "dom").
# Wyznaczone węzłem: ros2 run l4_sterowanie ik_trajektoria --ros-args -p tylko_ik:=true
KONFIGURACJE_IK = {
    'nad_obiektem': [0.1441, -1.5012, 1.9979, -2.0674, -1.5708, -1.4267],
    'chwyt':        [0.1441, -1.1650, 2.1810, -2.5868, -1.5708, -1.4267],
    'nad_celem':    [-1.1555, -1.5771, 2.0767, -2.0704, -1.5708, -2.7263],
    'odlozenie':    [-1.1555, -1.2921, 2.2530, -2.5317, -1.5708, -2.7263],
}


def sekwencja_przegubowa():
    """Zwraca listę (nazwa, q) z uzupełnionymi konfiguracjami."""
    wynik = []
    for nazwa, q in SEKWENCJA:
        q = q if q is not None else KONFIGURACJE_IK[nazwa]
        wynik.append((nazwa, list(q)))
    return wynik
