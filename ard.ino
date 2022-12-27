#include <Wire.h>


const int RELAY_1 = 11;
const int RELAY_2 = 10;
const int RELAY_3 = 9;
const int RELAY_4 = 82


const int mixer_1=0;

const int drink_1=1;

bool r1 = false;
bool r2 = false;
bool r3 = false;
bool r4= false;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(0x8);
  
  Wire.onReceive(rec);
  
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  pinMode(RELAY_4, OUTPUT);
  digitalWrite(RELAY_2, 0);
  digitalWrite(RELAY_1, 0);
  digitalWrite(RELAY_3, 0);
  digitalWrite(RELAY_4, 0);
  r1=false;
  r2=false;
  r3=false;
  r4=false;
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void rec(){
  while (Wire.available()){
    char c = Wire.read();
    turn_on(c);
    
  }
}

void turn_on(char c){
   if(c == 0){
    if(r1 == false){
      digitalWrite(RELAY_1,HIGH);
      r1 = true;
    }
    else{
      digitalWrite(RELAY_1, LOW);
      r1 = false;
    }
 
   }
   else if(c == 1){
    if(r2 == false){
      digitalWrite(RELAY_2,HIGH);
      r2 = true;
    }
    else{
      digitalWrite(RELAY_2, LOW);
      r2 = false;
    }
   }
   else if(c == 2){
    if(r3 == false){
      digitalWrite(RELAY_3, HIGH);
      r3 = true;
    }
    else{
      digitalWrite(RELAY_3, LOW);
      r3 = false;
    }
   }
   else if(c == 3){
    if(r4 == false){
      digitalWrite(RELAY_4, HIGH);
      r4 = true;
    }
    else{
      digitalWrite(RELAY_4, LOW);
      r4 = false;
    }
   }
}
