"""Migracja starszych polityk LeRobot (np. lerobot/diffusion_pusht) do formatu z procesorami.

Modele opublikowane przed LeRobot 0.4 nie mają plików policy_preprocessor.json
i nowe `lerobot-eval` odmawia ich wczytania (ProcessorMigrationError). LeRobot zawiera
skrypt migracji, ale w wersji 0.6.x wywraca się on przy zapisie konfiguracji
Diffusion Policy (listy liczb z config.json, np. crop_shape, nie są zamieniane
na krotki). Ten skrypt uruchamia oryginalną migrację z tą jedną poprawką.

Użycie (Colab lub terminal):
    python migruj_polityke.py --pretrained-path lerobot/diffusion_pusht --output-dir diffusion_pusht_migrated
"""
import lerobot.processor.migrate_policy_normalization as migracja

_oryginalna = migracja.make_policy_config


def _z_krotkami(policy_type, **pola):
    pola = {
        k: tuple(v) if isinstance(v, list) and all(isinstance(x, (int, float)) for x in v) else v
        for k, v in pola.items()
    }
    return _oryginalna(policy_type, **pola)


migracja.make_policy_config = _z_krotkami

if __name__ == "__main__":
    migracja.main()
