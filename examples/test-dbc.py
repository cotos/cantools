#!/usr/bin/env python3
#
# > python3 test-dbc.py
# Message: {'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 'Enabled'}
# Encoded: c001400000000000
# Decoded: {'Enable': 'Enabled', 'AverageRadius': 3.2, 'Temperature': 250.1}
#

from __future__ import print_function
import os, sys, getopt
from binascii import hexlify
import cantools, can
from time import sleep

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:"', str(sys.argv))

can_bus = can.interface.Bus('can0', bustype='socketcan')

def readdbc( dbcfile ):
    print("readdbc function")
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    MOTOHAWK_PATH = dbcfile
    db = cantools.db.load_file(MOTOHAWK_PATH)
    # Note:  magic # needs to be 0x05CC (1372),  These bits get reversed by OSCC
    #        magic # to send is 0xCC05 (52229)
    message = {
      'brake_enable_magic': 52229
    }
    # message = {
    #     'Temperature': 250.1,
    #     'AverageRadius': 3.2,
    #     'Enable': 'Enabled'
    # }
    # encoded = database.encode_message('ExampleMessage', message)
    # decoded = database.decode_message('ExampleMessage', encoded)
    encoded = db.encode_message('BRAKE_ENABLE', message)
    decoded = db.decode_message('BRAKE_ENABLE', encoded)
    print('Message:', message)
    print('Encoded:', hexlify(encoded).decode('ascii'))
    print('Decoded:', decoded)
    # data = example_message.encode({'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 1})
    brake_enable = db.get_message_by_name('BRAKE_ENABLE')
    data = brake_enable.encode({'brake_enable_magic': 52229})
    message = can.Message(arbitration_id=brake_enable.frame_id, data=data)
    can_bus.send(message)
    sleep(10)
    brake_disable = db.get_message_by_name('BRAKE_DISABLE')
    data = brake_disable.encode({'brake_disable_magic': 52229})
    message = can.Message(arbitration_id=brake_disable.frame_id, data=data)
    can_bus.send(message)

def load_dbc_file():
    db = cantools.database.load_file('../tests/files/dbc/drivekit-new.dbc')
    db.messages

def enable_can():
    print ("enable_can")
    # can_bus = can.interface.Bus('can0', bustype='socketcan')

def enable_modules():
    print ("enable_modules")

def disable_modules():
   print ("disable_modules")
    


def main(argv):
    dbcfile = "../tests/files/dbc/kia-niro-v1_5_5_validation-syntax-and-chassis-fix.dbc"
    valfile = ''
    try:
        opts, args = getopt.getopt(argv,"hf:v:",["dfile=","vfile"])
    except getopt.GetoptError:
        print ('test-dbc.py -f <dbcfile> -v <valfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ('test-dbc.py -f <dbcfile> -v <valfile>')
            sys.exit()
        elif opt in ("-f", "--dbcfile"):
            dbcfile = arg
        elif opt in ("-o", "--valfile"):
            valfile = arg
    print ('DBC file is "', dbcfile)
    print ('Value file is "', valfile)
    readdbc( dbcfile )
    enable_can()
    enable_modules()
    disable_modules()

if __name__ == "__main__":
    main(sys.argv[1:])





# message = {
#      'brake_enable_magic': 1372
# }

#data=[0x05, 0xcc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# encoded = database.encode_message('BRAKE_ENABLE', message + data)
# encoded = database.encode_message('BRAKE_ENABLE', data)
# decoded = database.decode_message('BRAKE_ENABLE', encoded)

# print('Message:', data)
# print('Encoded:', hexlify(encoded).decode('ascii'))
# print('Decoded:', decoded)
