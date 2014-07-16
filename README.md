DoorDuino 1.0
=========

###Arduino code for recognizing RFID tag, send it through serial port and receive a response from server to open the room's door.

**This project is composed by:**

- 1 Arduino Uno
- 1 RFID-Shield v2.0 by Seed Studio
- 1 RGB Led
- 1 Robocore Rele Module v2.0 SDR-S-1050 7A ~250V
- 1 Glass Door Electric Strike 90 Degree Swinging Door
- Some RFID Tags


##### This project includes some external libraries for manipulating the RFID-Shield

- SPI.h
- PN532_SPI.h
- PN532.h
- NfcAdapter.h
 
- PN532_SPI interface(SPI, 10);
- NfcAdapter nfc = NfcAdapter(interface);

