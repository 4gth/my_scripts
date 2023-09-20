#define CS 10    //soic p1    active low
#define MISO 12  //soic p2
#define MOSI 11  //soic p5
#define SCK 13   //coic p6

int z = 0;
void setup(){
  
  pinMode(CS, OUTPUT);
  pinMode(MISO, INPUT);
  pinMode(MOSI, OUTPUT);
  pinMode(SCK, OUTPUT);
  digitalWrite(CS, HIGH);
  
  Serial.begin(9600);
  delay(10000);
  Serial.println("booted");
  
}

void loop(){
  delay(10);
  Serial.println("in main loop");
  while(z == 0){
    delay(10);
    Serial.println("in while");
    digitalWrite(CS, LOW);
    delay(10);
    for(int base = 0; base <= 31; base += 16){
      byte data[16];
      for(int offset = 0; offset <= 15; offset += 1){
    
      shiftOut(MOSI, SCK, MSBFIRST, 0x03);
      shiftOut(MOSI, SCK, MSBFIRST, base + offset);
      data[offset] = shiftIn(MISO, SCK, MSBFIRST);
      delay(10);
    }
    delay(10);
    char buf[20];
      sprintf(buf, "%03x: %02x %02x %02x %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x %02x %02x %02x", base, 
      data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], 
      data[11], data[12], data[13], data[14], data[15]);
      Serial.println(buf);
    }
    digitalWrite(CS, HIGH);
    z++;
    Serial.println("exiting while");
  }
  
}