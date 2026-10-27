"""Simulateur logiciel du firmware (mêmes règles que bench_fsm.ino).

Attention : un test qui passe sur le simulateur ne prouve rien sur la carte.
Les résultats « simulateur » et « matériel » sont toujours distingués.
"""

VERSION = "1.0.0"
MAX_LEN = 31


class FirmwareSimulator:
    def __init__(self):
        self.state = "ARRETE"
        self.led = 0

    def _ok_state(self):
        return f"OK STATE {self.state}"

    def _set(self, state):
        self.state = state
        if state != "ACTIF":
            self.led = 0

    def handle(self, line: str) -> str:
        if len(line) > MAX_LEN:
            return "ERR OVERFLOW"
        cmd, _, arg = line.partition(" ")
        has_arg = " " in line
        bad = "ERR BAD_STATE"

        if cmd == "PING":
            return "OK PONG"
        if cmd == "VERSION":
            return f"OK VERSION {VERSION}"
        if cmd == "STATE":
            return self._ok_state()
        if cmd == "ARM":
            if self.state != "ARRETE":
                return bad
            self._set("PRET")
            return self._ok_state()
        if cmd == "START":
            if self.state != "PRET":
                return bad
            self._set("ACTIF")
            return self._ok_state()
        if cmd == "STOP":
            if self.state == "DEFAUT":
                return bad
            self._set("ARRETE")
            return self._ok_state()
        if cmd == "FAULT":
            self._set("DEFAUT")
            return self._ok_state()
        if cmd == "RESET":
            if self.state != "DEFAUT":
                return bad
            self._set("ARRETE")
            return self._ok_state()
        if cmd == "LED":
            if self.state != "ACTIF":
                return bad
            if has_arg and arg in ("0", "1"):
                self.led = int(arg)
                return f"OK LED {arg}"
            return "ERR BAD_ARG"
        if cmd == "ADC":
            return "OK ADC 512"
        return "ERR UNKNOWN"
