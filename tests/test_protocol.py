import re


def to_active(dut):
    assert dut.send("ARM") == "OK STATE PRET"
    assert dut.send("START") == "OK STATE ACTIF"


def test_T01_ping(dut):
    assert dut.send("PING") == "OK PONG"


def test_T02_version_format(dut):
    assert re.fullmatch(r"OK VERSION \d+\.\d+\.\d+", dut.send("VERSION"))


def test_T03_etat_initial_arrete(dut):
    assert dut.send("STATE") == "OK STATE ARRETE"


def test_T04_arm_passe_a_pret(dut):
    assert dut.send("ARM") == "OK STATE PRET"


def test_T05_start_depuis_pret_passe_a_actif(dut):
    dut.send("ARM")
    assert dut.send("START") == "OK STATE ACTIF"


def test_T06_start_depuis_arrete_refuse(dut):
    assert dut.send("START") == "ERR BAD_STATE"
    assert dut.send("STATE") == "OK STATE ARRETE"


def test_T07_stop_depuis_actif_revient_a_arrete(dut):
    to_active(dut)
    assert dut.send("STOP") == "OK STATE ARRETE"


def test_T08_fault_passe_a_defaut(dut):
    assert dut.send("FAULT") == "OK STATE DEFAUT"


def test_T09_arm_refuse_en_defaut(dut):
    dut.send("FAULT")
    assert dut.send("ARM") == "ERR BAD_STATE"
    assert dut.send("STATE") == "OK STATE DEFAUT"


def test_T10_reset_sort_du_defaut(dut):
    dut.send("FAULT")
    assert dut.send("RESET") == "OK STATE ARRETE"


def test_T11_led_commandable_en_actif(dut):
    to_active(dut)
    assert dut.send("LED 1") == "OK LED 1"
    assert dut.send("LED 0") == "OK LED 0"


def test_T12_led_refusee_hors_actif(dut):
    assert dut.send("LED 1") == "ERR BAD_STATE"


def test_T13_led_argument_invalide(dut):
    to_active(dut)
    assert dut.send("LED 7") == "ERR BAD_ARG"
    assert dut.send("LED") == "ERR BAD_ARG"


def test_T14_commande_inconnue(dut):
    assert dut.send("BLABLA") == "ERR UNKNOWN"


def test_T15_adc_dans_la_plage(dut):
    m = re.fullmatch(r"OK ADC (\d+)", dut.send("ADC"))
    assert m and 0 <= int(m.group(1)) <= 1023
