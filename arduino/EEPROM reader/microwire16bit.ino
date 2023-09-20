//16 bit eeprom

#define CS 6
#define CLK 7
#define DI 5
#define DO 4

#define SR_SER 7
#define SR_RCLK 6 //latch
#define SR_SRCLK 5

#define button 0
#define analogPin A0


int z = 0;
volatile byte buttonPressed = false;
const byte decPoint = 0x10;
const byte displayOutput[17] {


  0x3f, //0 - 0x00
  0x06, //1 - 0x01
  0x5b, //2 - 0x02
  0x4f, //3 - 0x03
  0x66, //4 - 0x04
  0x6d, //5 - 0x05
  0x7d, //6 - 0x06
  0x07, //7 - 0x07
  0x7f, //8 - 0x08
  0x6f, //9 - 0x09
  0x77, //A - 0x0A
  0x7c, //b - 0x0B
  0x39, //C - 0x0C
  0x5e, //d - 0x0D
  0x79, //E - 0x0E
  0x71, //F - 0x0F
  0x01, //. - 0x10
};

void clearDisplay() {

  digitalWrite(SR_RCLK, LOW);
  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, 0x00);
  digitalWrite(SR_RCLK, HIGH);
  digitalWrite(SR_RCLK, LOW);
}

void sendDisplaybyte(byte ibyte) {
  digitalWrite(SR_RCLK, LOW);

  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, displayOutput[(ibyte & 0xf0) >> 4]);
  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, displayOutput[ibyte & 0x0f]);
  digitalWrite(SR_RCLK, HIGH);
  digitalWrite(SR_RCLK, LOW);
}

void makebyte(word iword, int &hi, int &lo) {

  hi = highByte(iword);
  lo = lowByte(iword);


}

int READ(int address) {

  digitalWrite(CS, HIGH);

  if (address > 0x1ff) {
    shiftOut(DI, CLK, MSBFIRST, 0x1b);
  }
  else if (address > 0xff) {
    shiftOut(DI, CLK, MSBFIRST, 0x19);
  }
  else {
    shiftOut(DI, CLK, MSBFIRST, 0x18); //00110000

  }



  shiftOut(DI, CLK, MSBFIRST, address);
  byte HiByte = shiftIn(DO, CLK, MSBFIRST);
  byte LoByte = shiftIn(DO, CLK, MSBFIRST);

  digitalWrite(CS, LOW);
  digitalWrite(DI, LOW);

  word data = word(HiByte, LoByte);

  return (data);

}

void READALL() {

  for (int base = 0; base <= 1023; base += 8) {
    word data[8];
    for (int offset = 0; offset <= 7; offset += 1) {
      data[offset] = READ(base + offset);
    }
    char buf[80];
    sprintf(buf, "%03x: %04x %04x %04x %04x %04x %04x %04x %04x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]);

    Serial.println(buf);
  }
}

void WRITE(int address, word data) {

  byte hibyte = highByte(data);
  byte lobyte = lowByte(data);

  EWEN();
  delay(1);
  digitalWrite(CS, HIGH);

  if (address > 0x2ff) {
    shiftOut(DI, CLK, MSBFIRST, 0x17);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, hibyte);
    shiftOut(DI, CLK, MSBFIRST, lobyte);
  }
  else if (address > 0x1ff) {
    shiftOut(DI, CLK, MSBFIRST, 0x16);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, hibyte);
    shiftOut(DI, CLK, MSBFIRST, lobyte);
  }
  else if (address > 0xff) {
    shiftOut(DI, CLK, MSBFIRST, 0x15);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, hibyte);
    shiftOut(DI, CLK, MSBFIRST, lobyte);
  }
  else {
    shiftOut(DI, CLK, MSBFIRST, 0x14);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, hibyte);
    shiftOut(DI, CLK, MSBFIRST, lobyte);
  }
  delay(5);

  digitalWrite(DI, LOW);
  digitalWrite(CS, LOW);
}

void EWEN() {

  digitalWrite(CS, HIGH);
  shiftOut(DI, CLK, MSBFIRST, 0x13);
  digitalWrite(DI, LOW);
  CLKpulse(8);
  digitalWrite(CS, LOW);
}

void EWDS() {

  digitalWrite(CS, HIGH);
  shiftOut(DI, CLK, MSBFIRST, 0x10); //5 clk
  shiftOut(DI, CLK, MSBFIRST, 0x00); //8 clk
  digitalWrite(CS, LOW);             //13 clk for ewds

}

void CLKpulse(int num) {

  for (int i = 0; i < num; i++) {
    digitalWrite(CLK, HIGH);
    digitalWrite(CLK, LOW);
  }
}

void buttonPress() {
  buttonPressed = !buttonPressed;
}

void setup() {
  pinMode(CS,  OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(DI,  OUTPUT);
  pinMode(DO,  INPUT);

  pinMode(SR_SER,    OUTPUT);
  pinMode(SR_RCLK,   OUTPUT);
  pinMode(SR_SRCLK,  OUTPUT);

  pinMode(analogPin, INPUT);

  digitalWrite(DI, LOW);
  clearDisplay();

  attachInterrupt(digitalPinToInterrupt(button), buttonPress, RISING);
  Serial.begin(9600);
  randomSeed(analogRead(analogPin));
  delay(10000);
}

void loop() {

  while (z == 0) {

    Serial.println("Before WRITE");
    READALL();

    for (int i = 0x000; i < 0x400; i++) {

      word data = random(0x0000, 0xFFFF);

      WRITE(i, data);

    }
    Serial.println("After WRITE");
    READALL();
    z++;
  }

}
