/*
 * MFRC522 - Library to use ARDUINO RFID MODULE KIT 13.56 MHZ WITH TAGS SPI W AND R BY COOQROBOT.
 * The library file MFRC522.h has a wealth of useful info. Please read it.
 * The functions are documented in MFRC522.cpp.
 *
 * Based on code Dr.Leong   ( WWW.B2CQSHOP.COM )
 * Created by Miguel Balboa (circuitito.com), Jan, 2012.
 * Rewritten by Søren Thing Andersen (access.thing.dk), fall of 2013 (Translation to English, refactored, comments, anti collision, cascade levels.)
 * Released into the public domain.
 *-------------------------------------------------------------------- empty_skull 
 * Aggiunti pin per arduino Mega
 * add pin configuration for arduino mega
 * http://mac86project.altervista.org/
 --------------------------------------------------------------------- Nicola Coppola
 *
 * Following code is an adaptation of the one found in MFRC522 Library, just for testing
 * pouposes. I'm reading Mifare Classic tags, getting its UID and printing it.
 *
 --------------------------------------------------------------------- Adolfo Farias
 * Pin layout should be as follows:
 * Signal     Pin              Pin               Pin
 *            Arduino Uno      Arduino Mega      MFRC522 board
 * ------------------------------------------------------------
 * Reset      9                5                 RST
 * SPI SS     10               53                SDA
 * SPI MOSI   11               51                MOSI
 * SPI MISO   12               50                MISO
 * SPI SCK    13               52                SCK
 *
 * The reader can be found on eBay for around 5 dollars. Search for "mf-rc522" on ebay.com. 
 */

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance.

String content = "";

void setup() {
	Serial.begin(9600);	// Initialize serial communications with the PC
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();	// Init MFRC522 card
	Serial.println("Scan PICC to see UID...");
}

void loop() {
  String tmp;
  while(mfrc522.PICC_IsNewCardPresent()){
    
    tmp = getUIDString(mfrc522); 
    Serial.println(tmp.length());
    if(content != tmp && tmp.length() == 21){ 
      content == tmp;
    Serial.println(content);
    //Serial.println();
    }else{
      //authenticate();
    }
  }
}

String getUIDString(MFRC522 mfrc){
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return  "There's no card present"; 
  } else {
    String uid = "Read UID:";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        uid = uid+(mfrc.uid.uidByte[i] < 0x10 ? " 0" : " ");
        uid = uid+ String(mfrc522.uid.uidByte[i], HEX);
    }
    return uid;
  }
}
