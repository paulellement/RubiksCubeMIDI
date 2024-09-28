import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Decryption import GanGen2CubeEncrypter
import mido


# Services and Characteristics (incoming data from the cube)
ServAccessProfile = '00001800-0000-1000-8000-00805f9b34fb'
CharName = '00002a00-0000-1000-8000-00805f9b34fb'
CharAppearance = '00002a01-0000-1000-8000-00805f9b34fb'
CharPPCP = '00002a04-0000-1000-8000-00805f9b34fb'
CharPrivAddr = '00002ac9-0000-1000-8000-00805f9b34fb'

ServAttrProfile = '00001801-0000-1000-8000-00805f9b34fb'
CharServChanged = '00002a05-0000-1000-8000-00805f9b34fb'

ServUUID2 = 'f95a48e6-a721-11e9-a2a3-022ae2dbcce4'
CharUUID5 = 'f95a4b66-a721-11e9-a2a3-022ae2dbcce4'
CharUUID6 = 'f95a5034-a721-11e9-a2a3-022ae2dbcce4'
CharUUID7 = 'ec4cff6d-81fc-4e5b-91e0-8103885c9ae3'

ServUUID3 = '6e400001-b5a3-f393-e0a9-e50e24dc4179'
CharUUID8 = '28be4a4a-cd67-11e9-a32f-2a2ae2dbcce4'
# This is the one I use (current state, recent moves, orientation, etc.)
CharUUID9 = '28be4cb6-cd67-11e9-a32f-2a2ae2dbcce4' 

MAC = 'AB:12:34:02:3A:06'

prev = "h"
encrypter = None
sides = ["White", "Red", "Green", "Yellow", "Orange", "Blue"]
dirs = ["Clockwise", "Counter-Clockwise"]
port = None

# Callback function to handle incoming data
def callback(sender, data):
    global prev, port
    if data != prev:
        decrypted_data = encrypter.decrypt(data)
        strdata = decrypted_data.hex()
        
        if decrypted_data[0] >= 0x20 and decrypted_data[0] < 0x30: # Message is of type "move"
            side = int(strdata[3])
            # the 128 is just because I want the most significant bit (left bit) of the 4 bits
            dir = decrypted_data[2] >= 128 # 0 clockwise, 1 counter-clockwise
            note_on_msg = mido.Message('note_on', note=(side*2+60+dir), velocity=64, channel=0)
            port.send(note_on_msg)


            #print(sides[side], dirs[dir])
        elif decrypted_data[0] >= 0x40 and decrypted_data[0] < 0x50: # Message is of type "state"
            if strdata[3:26] == "05397000002468acf134000": # This happens when the cube is solved
                note_on_msg = mido.Message('note_on', note=(80), velocity=64, channel=0)
                port.send(note_on_msg)
                #print("Solved! WOOOOO")
            elif strdata[3:26] == "053970000ce8a4603570000": # Checkerboard-like pattern
                note_on_msg = mido.Message('note_on', note=(81), velocity=64, channel=0)
                port.send(note_on_msg)
            
            
        prev = data
 

    

async def scan_and_connect():
    global key, encrypter
    # Start scanning for nearby BLE devices
    found = False
    devices = await BleakScanner.discover()
    key = [0x01, 0x02, 0x42, 0x28, 0x31, 0x91, 0x16, 0x07, 0x20, 0x05, 0x18, 0x54, 0x42, 0x11, 0x12, 0x53]
    iv = [0x11, 0x03, 0x32, 0x28, 0x21, 0x01, 0x76, 0x27, 0x20, 0x95, 0x78, 0x14, 0x32, 0x12, 0x02, 0x43]
    encrypter = GanGen2CubeEncrypter(key, iv)
    
    # Iterate through the discovered devices
    for device in devices:
        # Check if the device's address matches the desired address
        if device.address == MAC:
            found = True
            try:
                # Connect to the device
                async with BleakClient(device) as client:
                    print(f"Connected to {device.name} ({device.address})")
                    
                            
                    print("Pairing with the device...")
                    await client.pair()
                    print("Device paired successfully.")

                    
                    while True:
                        try:                         
                            await client.start_notify(CharUUID9, callback)  
                        except BleakError as e:
                            print("Error after connected: ", e)
                        
            except Exception as e:
                print(f"Failed to connect to {device.name} ({device.address}): {e}")
            break # device found wooo

    if not found:
        print("Device not found")


async def main():
    global port
    try:
        # Open the MIDI port
        output_port_names = mido.get_output_names()

        # Print the list of output port names
        
        for name in output_port_names:
            if name[:8] == "loopMIDI":
                port = mido.open_output(name)
                break
        if port is None:
            print("Could not find MIDI port.")
            raise Exception

        
        await scan_and_connect()

    except KeyboardInterrupt:
        print("Exiting...")
        
    finally:
        # Cleanup
        if port is not None:
            port.close()
            print("MIDI port closed.")
        
asyncio.run(main())
