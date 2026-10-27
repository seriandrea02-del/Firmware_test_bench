"""Accès au système sous test : carte réelle (série) ou simulateur."""
import time

from bench.simulator import FirmwareSimulator


class Device:
    mode = "?"

    def send(self, line: str) -> str:
        raise NotImplementedError

    def close(self):
        pass

    def to_idle(self):
        """Remet le système à l'état ARRETE avant chaque test."""
        if self.send("STOP").startswith("ERR"):
            self.send("RESET")
        assert self.send("STATE") == "OK STATE ARRETE"


class SimDevice(Device):
    mode = "simulateur"

    def __init__(self):
        self.fw = FirmwareSimulator()

    def send(self, line):
        return self.fw.handle(line)


class SerialDevice(Device):
    mode = "matériel"

    def __init__(self, port, baud=115200, timeout=1.0):
        import serial  # importé ici : inutile en mode simulateur

        self.ser = serial.Serial(port, baud, timeout=timeout)
        time.sleep(2.0)  # l'Arduino redémarre à l'ouverture du port
        self.ser.reset_input_buffer()

    def send(self, line):
        self.ser.write((line + "\n").encode())
        raw = self.ser.readline().decode(errors="replace").strip()
        if not raw:
            raise TimeoutError(f"Pas de réponse à « {line} »")
        return raw

    def close(self):
        self.ser.close()
