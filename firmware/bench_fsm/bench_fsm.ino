// Firmware de démonstration : machine à états pilotée par le port série.
// Carte visée : ELEGOO MEGA2560 R3 (ATmega2560). Protocole : voir README.
enum State { ARRETE, PRET, ACTIF, DEFAUT };
const char* const NAMES[] = {"ARRETE", "PRET", "ACTIF", "DEFAUT"};
const char* const VERSION_STR = "1.0.0";

State state = ARRETE;
const uint8_t LED_PIN = LED_BUILTIN;
const uint8_t ADC_PIN = A0;

char buf[32];
uint8_t len = 0;
bool overflow = false;

void setState(State s) {
  state = s;
  if (s != ACTIF) digitalWrite(LED_PIN, LOW);
}

void okState() { Serial.print(F("OK STATE ")); Serial.println(NAMES[state]); }
void badState() { Serial.println(F("ERR BAD_STATE")); }

void handle(char* line) {
  char* arg = strchr(line, ' ');
  if (arg) { *arg = 0; arg++; }
  const char* cmd = line;

  if (!strcmp(cmd, "PING")) Serial.println(F("OK PONG"));
  else if (!strcmp(cmd, "VERSION")) { Serial.print(F("OK VERSION ")); Serial.println(VERSION_STR); }
  else if (!strcmp(cmd, "STATE")) okState();
  else if (!strcmp(cmd, "ARM")) { if (state == ARRETE) { setState(PRET); okState(); } else badState(); }
  else if (!strcmp(cmd, "START")) { if (state == PRET) { setState(ACTIF); okState(); } else badState(); }
  else if (!strcmp(cmd, "STOP")) { if (state == DEFAUT) badState(); else { setState(ARRETE); okState(); } }
  else if (!strcmp(cmd, "FAULT")) { setState(DEFAUT); okState(); }
  else if (!strcmp(cmd, "RESET")) { if (state == DEFAUT) { setState(ARRETE); okState(); } else badState(); }
  else if (!strcmp(cmd, "LED")) {
    if (state != ACTIF) badState();
    else if (arg && !strcmp(arg, "1")) { digitalWrite(LED_PIN, HIGH); Serial.println(F("OK LED 1")); }
    else if (arg && !strcmp(arg, "0")) { digitalWrite(LED_PIN, LOW); Serial.println(F("OK LED 0")); }
    else Serial.println(F("ERR BAD_ARG"));
  }
  else if (!strcmp(cmd, "ADC")) { Serial.print(F("OK ADC ")); Serial.println(analogRead(ADC_PIN)); }
  else Serial.println(F("ERR UNKNOWN"));
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\r') continue;
    if (c == '\n') {
      if (overflow) Serial.println(F("ERR OVERFLOW"));
      else { buf[len] = 0; handle(buf); }
      len = 0; overflow = false;
    } else if (len < sizeof(buf) - 1) buf[len++] = c;
    else overflow = true;
  }
}
