# Rubik's Cube MIDI
A script that makes a Bluetooth Low Energy Rubik's Cube a MIDI instrument. Made for the McGill MAT Minor class "New Media Production".

To run this code, you will need loopMIDI as a virtual MIDI port to send MIDI messages from your IDE to your digital audio workstation.
The decryption will only work on the GAN i3 Smart Cube, and your own MAC address must be used.

Below is most of the report that was submitted along with the project itself. It summarizes the code and the process well.

## Abstract
A Bluetooth signal from a Rubik’s Cube was used to generate MIDI messages, where turning a certain side in a certain direction was mapped to a note-on message using mido, a Python library. These messages were sent as input to PureData. Two patches were made: a drum kit and an additive synth, both of which use MIDI input to play sounds.


## Summary of Process and Code 

### Connection and Getting Input
I began by trying to connect to the cube using Python. This was fairly straightforward. I used the Bleak library, a Python library used for communicating with bluetooth low energy (BLE) devices like my cube. A BLE device has a unique MAC address that allows another device to connect to it. This was used to connect the cube to my computer. The program must connect to the cube each time it runs, because it automatically disconnects when the program is stopped.

The process of getting input is more sophisticated. A BLE device has many services, each with characteristics. In short (an oversimplification), a service is a general category of the device’s data, and a characteristic is specific data that is sent to the computer. Some of the cube’s characteristics include the device name, version, and state. The name and version are a single message sent to the computer when connected. The state is an ongoing signal that my program “subscribes” to (i.e., reads). Upon subscribing, the computer is notified about the state of the cube several times per second. There is no exact rate, it just depends on when the state changes (i.e., a side is turned or the whole cube is rotated). When I originally printed the incoming data to see if I could interpret it, I was disappointed to find out it was encrypted.
 
### Decrypting the Data
Decrypting the incoming data from the cube was the most difficult part of the project. After countless hours (more than I’d like to admit) of reading online source-codes of scripts that decrypt Rubik’s cube messages and trying to implement my own version, I finally found a reasonably simple script that used the cube I had. It was written in typescript, which is similar to javascript so I could understand it. Translating it into Python wasn’t too bad, I just had to find a library that does AES-128 encryption (which is what the cube uses). I ended up using a library called “cryptography”.

To instantiate a new encrypter (i.e., an object that can encrypt and decrypt messages), you must provide a key and an iv. These I found online. The key must also be salted by the MAC-address of my Rubik’s cube. The MAC-address contains six 256 bit numbers (or six pairs of hexadecimal numbers). The salting algorithm is to reverse the MAC-address, then add the six numbers to the first six numbers of the key respectively (the key is an array of sixteen 256-bit numbers). Once the encrypter is instantiated with the updated key and the iv, messages can be decrypted by calling the decrypt function on the data. I don’t exactly know how the decryption works (it’s all taken care of by the library given the correct input), all I know is that the cube uses the AES-128 encryption algorithm.

### Generating MIDI Messages
The same online code that decrypted the data also parsed the decrypted data. So, I was able to quickly understand what each incoming message meant. I also printed out incoming messages and turned the cube to see how the messages changed. There were three types of messages: The gyro-state of the cube (i.e., the orientation), a move (i.e., a turn), and the permutation of the pieces of the cube (i.e., which colours are where).

The gyro-state messages start with 0x1. I wanted to map the gyro to a filter. For example, tilting the cube one way would act as a knob. However, this proved to be too ambitious. So, I filtered these messages out.

The move messages start with 0x2. Then, the next hex number is the side that was turned. Then, the next bit (not hex) is the direction (clockwise/counterclockwise). Instead of extracting the bit, I just checked if the hex number was less than 8 or not, since the range 0-7 corresponds to 0xxx in binary, and the range 8-15 corresponds to 1xxx in binary. So, the hex number representing the side and the bit representing the direction were mapped to 12 MIDI notes (because there are 6 sides and 2 directions to turn) in the range 60-71.

The permutation messages start with 0x4, followed by a long string of hexadecimal numbers representing the permutation. I saved the string for the solved state and for the checkerboard pattern state. If the messages representing these two states are received, my program generates MIDI notes 80 and 81 respectively.

I used the mido library to generate MIDI note-on messages, each with full velocity. The messages are sent to loopMIDI (a virtual MIDI port), then PureData uses loopMIDI as its MIDI input.

## The PureData Patches
Both patches are fairly straightforward. They start with the notein object, then the select object to get notes 60-71 (and 80-81 in the drumset patch). The drum set maps each note to an audio sample, while the synth uses the mtof object to map MIDI notes to frequencies to be generated by oscillators. Note that I adjusted the MIDI notes in the synth to make the cube easier to play (specifically for Minuet in G), since some combinations of turns are physically easier than others. The synth also has an envelope to make it sound a bit better.


## Sources Accessed
1. https://www.youtube.com/watch?v=8pMaR-WUc6U
2. https://bleak.readthedocs.io/en/latest/api/client.html
3. https://github.com/afedotov/gan-web-bluetooth/tree/main (This one helped the most with
decrypting the data. I basically just translated their decryption code into Python)
4. https://mido.readthedocs.io/en/stable/
5. https://github.com/cs0x7f/cstimer/blob/fc627f0970d8982c758200430bb60d7554f984b0/s
rc/js/bluetooth.js#L175 (Spent a while reading this one, but didn’t end up helping much,
because the relevant parts were buried inside much more complicated code).
6. https://www.youtube.com/watch?v=mvqXk6t7TQ8&t=116s
7. https://www.youtube.com/watch?v=W7Pp-DhMA_E&t=242s
