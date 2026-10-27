# Banc de test automatisé pour firmware embarqué

Banc de test en Python (PySerial + Pytest) qui valide, par le port série, le comportement d'un firmware Arduino : une machine à états `ARRETE → PRET → ACTIF → DEFAUT` pilotée par un protocole texte. Les mêmes 15 tests tournent sur une **carte réelle** ou sur un **simulateur logiciel**, et la cible utilisée est toujours affichée.

![tests](../../actions/workflows/ci.yml/badge.svg)

## Résultats

| Cible | Statut |
|---|---|
| Simulateur (CI GitHub Actions) | 15 tests, voir l'onglet *Actions* |
| Carte ELEGOO MEGA2560 R3 | **À compléter après essai sur la carte** (nombre de tests réussis, date) |

Un test réussi sur le simulateur ne prouve rien sur le firmware réel : seule la ligne « carte » le démontre.

## Architecture

```
PC (Pytest) ── bench/transport.py ──┬─ SerialDevice ── USB ── Arduino (bench_fsm.ino)
                                    └─ SimDevice ──── bench/simulator.py
```

## Arborescence

```
firmware/bench_fsm/bench_fsm.ino   firmware Arduino
bench/simulator.py                 simulateur du firmware
bench/transport.py                 accès série ou simulateur
tests/test_protocol.py             tests T01 à T15
tests/conftest.py                  option --port, remise à zéro avant chaque test
.github/workflows/ci.yml           tests automatiques
```

## Protocole série (115200 bauds, lignes terminées par `\n`)

| Commande | Effet | Réponse |
|---|---|---|
| `PING` | test de liaison | `OK PONG` |
| `VERSION` | version du firmware | `OK VERSION x.y.z` |
| `STATE` | état courant | `OK STATE <état>` |
| `ARM` | ARRETE → PRET | `OK STATE PRET` |
| `START` | PRET → ACTIF | `OK STATE ACTIF` |
| `STOP` | PRET ou ACTIF → ARRETE | `OK STATE ARRETE` |
| `FAULT` | injecte un défaut, → DEFAUT | `OK STATE DEFAUT` |
| `RESET` | DEFAUT → ARRETE | `OK STATE ARRETE` |
| `LED 0\|1` | LED de la carte (état ACTIF seulement) | `OK LED n` |
| `ADC` | lecture de A0 (0 à 1023) | `OK ADC n` |

Erreurs : `ERR BAD_STATE` (commande interdite dans l'état courant), `ERR BAD_ARG`, `ERR UNKNOWN`, `ERR OVERFLOW` (ligne de plus de 31 caractères).

## Utilisation

```bash
git clone https://github.com/<ton-pseudo>/firmware-test-bench.git
cd firmware-test-bench
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

python -m pytest -v                      # simulateur, aucune carte nécessaire
python -m pytest -v --port COM3          # carte réelle (Linux : /dev/ttyACM0)
```

Pour la carte : ouvrir `firmware/bench_fsm/bench_fsm.ino` dans l'Arduino IDE, choisir *Arduino Mega or Mega 2560*, téléverser, fermer le moniteur série, puis lancer Pytest avec `--port`.

## Limites

- Le simulateur et le firmware sont écrits séparément : ils peuvent diverger, c'est ce que les essais sur carte permettent de détecter.
- Pas d'instrumentation externe (oscilloscope, analyseur logique) : seul le comportement visible par le port série est testé.

## Auteure

Laurette Seri, Master 2 CSEC, Université de Lorraine. Licence MIT.
