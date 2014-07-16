#include <SPI.h>
#include <PN532_SPI.h>
#include <PN532.h>
#include <NfcAdapter.h>
 
PN532_SPI interface(SPI, 10);
NfcAdapter nfc = NfcAdapter(interface);

#define PORTA 8

#define BLUE 2
#define RED 3
#define GREEN 4

String leitura = "";

void setup() {
    
    // initialize the LED pins:
    pinMode(PORTA, OUTPUT);
    pinMode(BLUE, OUTPUT); 
    pinMode(GREEN, OUTPUT); 
    pinMode(RED, OUTPUT);  
  
    Serial.begin(9600);
    Serial.println("toc toc\nquem eh?");
    nfc.begin();   
}
 
void loop(void) {
  String tmp;
    while (nfc.tagPresent()) {
        NfcTag tag = nfc.read();
        tmp = tag.getUidString();
        if(leitura != tmp){
          leitura = tmp;
          Serial.println(leitura);
          //tag.print();

        }else{
          autenticar();
        }
    }
    leitura = ""; 
}

void autenticar(){
   while (Serial.available() > 0) {
    int inByte = Serial.read();
    //Serial.write(" mensagem do servidor: " + inByte);
     if(inByte == 'a'){
        digitalWrite(PORTA, HIGH);
        delay(30);
        digitalWrite(PORTA, LOW);
        ledBlink(GREEN);
        
    }else if (inByte == 'b'){
      ledBlink(RED);
          
    }
  }
}

// turn RGB led on according to his colorPin
void ledBlink(int colorPin){
  ledsLOW();  
  switch(colorPin){
     case RED:
        digitalWrite(RED, HIGH);
        break;
     case GREEN:
        digitalWrite(GREEN, HIGH);    
        break;
    // case BLUE:
      //  digitalWrite(BLUE, HIGH);
      //  break;
  }
  delay(1500);
  ledsLOW();  
  digitalWrite(BLUE, HIGH);
}

void ledsLOW(){
  digitalWrite(BLUE, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);  
}
