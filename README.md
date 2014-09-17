DoorDuino 1.0
=========

###Arduino code for recognizing RFID tag, send it through serial port and receive a response from server to open the room's door.

##### This project includes some external libraries for manipulating the RFID-Shield

### NDEF Library for Arduino
available at: https://github.com/don/NDEF
### RFID Libs for MFRC522 Shield
https://github.com/miguelbalboa/rfid
https://github.com/ljos/MFRC522


#### Objective
Considering the large embedded systems applicability and its current cheap availability, this project intend to assemble small low-setting hardwares and softwares in order to provide people’s access at rooms equipped with the system as well as its management.

#### Goals
Given the problematic and its scope, the system must:
1. Provide authorized people(’s equipment) access to places in which the system is installed;
2. Keep user records considering their entrance date and time;
3. Add and remove authorizations;

#### Solution
The first approach will be to build a piece of software able to permit users’ entrances through doors. A RFID-Shield ridden on an Arduino must recognize RFID’s compatible tags, reading its UID and sending the data to a server over serial port. The same piece of software must, then, get a response from the server and authorize or deny the read UID. In positive case, Arduino’s response is a 5V signal boosted by a 12V relay and sent to an electric strike used to control door’s accesses.
In turn, the Python-coded server must recognize the serial port used by the Arduino, read the UID sent and give a response based on its records. Every successful reading must be recorded containing the tag identification, date, time and the server’s response itself. Python’s choice is based on its simple establishment of serial communication beyond the soft SQLite’s communication applicable (and acceptable) on this project.
Authorizations management can be simply set using a previously registered tag as a Master Key, allowing the system to activate a special mode in which the next read tag can be recorded or discarded.
An RGB led will be used to enhance user’s experience.
Considering the Server pre-requisites, the project can be embedded in any Operational System Python-compatible which requires up to 260 MB including peripheral library and SQLite, providing a concise and adaptable solution for low hardware configuration.
