//8bit eeprom

#define CS 8
#define CLK 9
#define DI 10
#define DO 11

#define SR_SER 7
#define SR_RCLK 6 //latch
#define SR_SRCLK 5

int z = 0;

const byte displayOutput[17] {

  0xFC,  //0
  0x60,  //1
  0xDA,  //2
  0xF2,  //3
  0x66,  //4
  0xB6,  //5
  0xBE,  //6
  0xE0,  //7
  0xFE,  //8
  0xE6,  //9
  0xEE,  //A
  0x3E,  //b
  0x9C,  //C
  0x7A,  //d
  0x9E,  //E
  0x8E,  //F
  0x10,  //.
};

void clearDisplay() {

  digitalWrite(SR_RCLK, LOW);
  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, 0x00);
  digitalWrite(SR_RCLK, HIGH);
  digitalWrite(SR_RCLK, LOW);
}

void sendDisplaybyte(byte ibyte) {
  digitalWrite(SR_RCLK, LOW);

  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, displayOutput[(ibyte & 0xf0) >> 4] );
  shiftOut(SR_SER, SR_SRCLK, MSBFIRST, displayOutput[ibyte & 0x0f]);
  digitalWrite(SR_RCLK, HIGH);
  digitalWrite(SR_RCLK, LOW);
}

void READALL(){
  
  for (int base = 0; base <= 511; base += 16) {
    int data[16];
    for (int offset = 0; offset <= 15; offset += 1) {
      data[offset] = READ(base + offset);
    }
    char buf[80];
    sprintf(buf, "%03x: %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);

    Serial.println(buf);
    
  }
  
}

byte READ(int address) {
  
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
  digitalWrite(DI, LOW);
  sendDisplaybyte(data);
  //delay(100);
  //Serial.println(data);
  return (data);

}

void WRITE(int address, byte data) {
 
 
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

  digitalWrite(DI, LOW);
  Serial.begin(9600);
  clearDisplay();
  delay(10000);
  Serial.println("Booted");
}

void loop() {
 
  while(z == 0)
  {
    READALL();
   for(int i = 0; i < 512; i++){
     
     READ(i);
     delay(100);
   }
   
   z++;
  }

 
}
