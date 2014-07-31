#!/usr/bin/python

import serial
import glob
import os
import sqlite3
#
#  file paths
#
db_filename = 'db/portal.db'
schema_filename = 'db/portal_schema.sql'
#
#  keywords
#
MASTER_KEY = '0a 14 68 a1'
ALLOWED, DENIED, CHECKER, PORT, BAUD_RATE = 'a', 'b', 'c', '/dev/ttyACM1', 9600
#
#  variables
#
updating_list = False
authorized_uids = []
#
#  functions
#
def list_update():                              # Alternates Boolean global variable
    global updating_list
    updating_list = not updating_list

def update_list(uid):
    if not MASTER_KEY in uid:                   # ignores updating if master key is present
        if uid in authorized_uids:              # check if uid is on the list
            rm_uid(uid)                         # remove it if it's there
            print(uid + ' removed')
            arduino.write(DENIED)
        elif not MASTER_KEY in uid:
            authorized_uids.append(uid)
            print(uid + ' added')
            add_uid(uid)                        # saves the new uid into database
            arduino.write(ALLOWED)
        list_update()

def load_uids():                                # checks database and loads all uids that are already there

    sql = 'select uid from card'                # selects uid column
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute(sql)
    for record in cursor.fetchall():
        print(record[0])
        authorized_uids.append(record[0])

def add_uid(uid):                               # add it if it isn't        # UPDATE PASSED PARAMETRS
    sql = 'insert into card values (?,?,?)'
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(sql, (uid, 'card_name', 'card_mail'))
    conn.commit()
    authorized_uids.append(uid)

def rm_uid(uid):                                # REMOVES UID
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    conn.text_factory = str    
    query = "delete from card where uid = '%s';" % uid
    print(query)
    mydata = cursor.execute(query)
    conn.commit()
    authorized_uids.remove(uid)

def scan_ports():                               # gets all ttyACM accessible ports (Linux)
    return glob.glob('/dev/ttyACM*')
#
#   DATABASE CONFIG
#
db_is_new = not os.path.exists(db_filename).    # checks if database file is there

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print 'Creating schema'
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

        print 'Inserting initial data'
        
        conn.execute("""
        insert into card (uid, name, mail)
        values ('93 3e ba 83', 'Ivanilson Junior', 'ivanilson.junior@ifrn.edu.br')
        """)
        conn.execute("""
        insert into card (uid, name, mail)
        values ('ba f5 e0 17', 'Adolfo Farias', 'adf.melo@gmail.com')
        """)

    else:
        print 'Database exists, assume schema does, too.'
#
#  Arduino conection
#
print "available ttyACM ports:"
print scan_ports()
print '---\n---'

for port in scan_ports():
    try:
        arduino = serial.Serial(port, BAUD_RATE)
        print "conected to port " + port
    except:
        print "failed to conect on " + port

print "authorized uids:"
load_uids()                                   # loads already registered uids on memory
print '---\n---'

time.sleep(2)                                 # waiting arduino's initialization...
print(" Portal ready.\n---")
#
#  loop
#
while 1:                                      # main loop
    if arduino.inWaiting() > 0:
        uid = arduino.readline().strip()      # reads what arduino has written
        if '<' in uid and '>' in uid :        # verifies if a UID was readden

            uid = uid[2:-2]                   # remove < > simbols

            if updating_list:
                update_list(uid)

            elif MASTER_KEY in uid:           # MASTER_KEY CHECKER
                arduino.write(CHECKER)        # master_key signal on arduino
                print("MASTER_KEY mode")
                list_update()

            elif uid in authorized_uids:      # check if uid is in the list here
                arduino.write(ALLOWED)        # is there
                print("UID " + uid + " allowed")

            else:                             # is not there
                arduino.write(DENIED)
                print("UID " + uid + " denied")
