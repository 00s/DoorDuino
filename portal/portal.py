#!/usr/bin/python

import serial
import glob
import time
import os
import sqlite3
#
#   file paths
#
db_filename = 'db/portal.db'
schema_filename = 'db/portal_schema.sql'
#
#   keywords
#
MASTER_KEY = '0a 14 68 a1'
ALLOWED, DENIED, CHECKING, BAUD_RATE = 'a', 'b', 'c', 9600
#
#   variables
#
updating_list = False
authorized_uids = []
#
#   functions
#
def list_update():                              # Alternates Boolean global variable
    global updating_list
    updating_list = not updating_list

def update_list(uid):
    if not MASTER_KEY in uid:                   # Ignores updating if master key is present
        if uid in authorized_uids:              # Checks if UID is on the list
            rm_uid(uid)                         # Removes UID if it's there
            print(uid + ' removed')
            arduino.write(DENIED)
        else:                               	# Adds the UID if it's not there yet
            add_uid(uid)                        # Saves the new uid into database and in local memory
            arduino.write(ALLOWED)
            print(uid + ' added')
        list_update()
        print ('MASTER KEY mode off ')

def load_uids():                                # Checks database and loads all uids already there

    sql = 'select uid from card'                # Selects uid column
    conn.row_factory = sqlite3.Row
    conn.text_factory = str                     # 
    cursor = conn.cursor()
    cursor.execute(sql)
    for record in cursor.fetchall():			# Iterates over column rows
        print(record[0])
        authorized_uids.append(record[0])

def add_uid(uid):                               # Adds uid from local memory and database      # UPDATE PASSED PARAMETRS
    sql = 'insert into card values (?,?,?)'
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(sql, (uid, 'no_card_name_associated', 'no_card_mail_associated'))
    conn.commit()
    authorized_uids.append(uid)

def rm_uid(uid):                                # Removes uid from local memory and database
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    conn.text_factory = str                     # Converts strings in the database from unicode to UTF-8
    query = "delete from card where uid = '%s';" % uid
    print(query)
    mydata = cursor.execute(query)
    conn.commit()
    authorized_uids.remove(uid)

def scan_ports():                               # Gets all ttyACM accessible ports (Linux)
    return glob.glob('/dev/ttyACM*')
#
#   database configuration
#
db_is_new = not os.path.exists(db_filename)    # Checks if database file is there

with sqlite3.connect(db_filename) as conn:
    print '---'
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
        print ' Database exists, assume schema does, too.'
    print '---'
#
#   arduino conection and main loop
#
if len(scan_ports()) > 0:                           # Verifies if there is any port available
    print " available ttyACM ports:"
    print scan_ports()
    print '---'
    
    for port in scan_ports():                       # Tries to connect on the ports available
        try:
            arduino = serial.Serial(port, BAUD_RATE)
            print " conected to port " + port
            break
        except:
            print " failed to conect on " + port

    print "---\n authorized uids:"
    load_uids()                                   	# Loads already registered uids on memory
    print '---\n Initializing Portal...\n---'

    time.sleep(2)                                   # Waiting arduino's initialization...
    print(" Portal ready.\n---")
    #
    #   main loop
    #
    while 1:
        if arduino.inWaiting() > 0:
            uid = arduino.readline().strip()        # Reads what arduino has written
            if '<' in uid and '>' in uid :          # Verifies if a UID was readden
                uid = uid[2:-2]                     # Remove < > simbols

                if updating_list:
                    update_list(uid)

                elif MASTER_KEY in uid:             # MASTER_KEY CHECKER
                    arduino.write(CHECKING)         # Master_key signal on arduino
                    print("MASTER KEY mode on")
                    list_update()

                elif uid in authorized_uids:        # Check if uid is in the list here
                    arduino.write(ALLOWED)          # Is there
                    print("UID " + uid + " allowed")

                else:                               # is not there
                    arduino.write(DENIED)
                    print("UID " + uid + " denied")
else:                                               # exits the aplication if there are no possible connections
    print "There are no connections available.\nVerify if the Arduino is pluged in and run this script again.\nSee you!"
    exit()