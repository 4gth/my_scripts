//8bit eeprom

#define CS 11
#define CLK 10
#define DI 9
#define DO 8

#define SR_SER 7 //pin14
#define SR_RCLK 6 //latch pin12
#define SR_SRCLK 5 //pin11

int z = 0;
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

int READ(int address) {
  digitalWrite(CS, HIGH);



  if (address > 0xff) {
    shiftOut(DI, CLK, MSBFIRST, 0x0d);
  }
  else {
    shiftOut(DI, CLK, MSBFIRST, 0x0c);

  }


  shiftOut(DI, CLK, MSBFIRST, address);
  int data = shiftIn(DO, CLK, MSBFIRST);
  digitalWrite(CS, LOW);
  return (data);

}

void WRITE(int address, byte data) {
 
  digitalWrite(CS, HIGH);
  EWEN();
  if (address > 0xff) {
    shiftOut(DI, CLK, MSBFIRST, 0x0b);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, data);
  }
  else {
    shiftOut(DI, CLK, MSBFIRST, 0x0a);
    shiftOut(DI, CLK, MSBFIRST, address);
    shiftOut(DI, CLK, MSBFIRST, data);

  }
  EWDS();
  digitalWrite(CS, LOW);
}

void EWEN() {

  digitalWrite(CS, HIGH);
  shiftOut(DI, CLK, MSBFIRST, 0x09); //4 clk pulses
  shiftOut(DI, CLK, MSBFIRST, 0x80); //8 clk pulses
  //12 clk pulses for EWEN
  digitalWrite(CS, LOW);
}

void EWDS() {

  digitalWrite(CS, HIGH);
  shiftOut(DI, CLK, MSBFIRST, 0x08);
  shiftOut(DI, CLK, MSBFIRST, 0x00);
  digitalWrite(CS, LOW);

}

void setup() {
 
  pinMode(CS,  OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(DI,  OUTPUT);
  pinMode(DO,  INPUT);

  pinMode(SR_SER,    OUTPUT);
  pinMode(SR_RCLK,   OUTPUT);
  pinMode(SR_SRCLK,  OUTPUT);
  Serial.begin(9600);
  digitalWrite(DI, LOW);
  clearDisplay();
  sendDisplaybyte(88);
  delay(1000)
}

void loop() {
 
  while (z == 0) {
    int address = 0x000;
    for (; address < 0x1000; address++) {
      int data = address + 40;
      byte dataRead;

      sendDisplaybyte(address);
      Serial.println(address);
      delay(1000);
      WRITE(address, data);
      dataRead = READ(address);

      if (data == dataRead) {

        sendDisplaybyte(dataRead);
        
      }
      else
      {
        sendDisplaybyte(0xee);
      }
    }

    delay(1000);
  }

  z++;
  clearDisplay();
}
