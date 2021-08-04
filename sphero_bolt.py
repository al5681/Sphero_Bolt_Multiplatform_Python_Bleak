import struct
from sphero_constants import *
from bleak import BleakClient


class SpheroBolt:
    def __init__(self, address):
        self.sequence = 0
        self.address = address
        self.notificationPacket = []

    async def connect(self):
        """
        Connects to a Sphero Bolt of a specified MAC address if it can find it.
        """
        self.client = BleakClient(self.address)
        await self.client.connect()
        print("Connected: {0}".format(self.client.is_connected))

        # cancel if not connected
        if not self.client.is_connected:
            return False

        # get device name
        try:
            DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805f9b34fb"
            device_name = await self.client.read_gatt_char(DEVICE_NAME_UUID)
            print("Device Name: {0}".format("".join(map(chr, device_name))))
        except Exception:
            pass

        self.API_V2_characteristic = "00010002-574f-4f20-5370-6865726f2121"
        AntiDOS_characteristic = "00020005-574f-4f20-5370-6865726f2121"

        # Unlock code: prevent the sphero mini from going to sleep again after 10 seconds
        print("[INIT] Writing AntiDOS characteristic unlock code")
        await self.client.write_gatt_char(AntiDOS_characteristic, b"usetheforce...band", response=True)

        print("[INIT] Initialization complete\n")

        return True

    async def disconnect(self):
        """
        Disconnects the Sphero Bolt
        """
        return await self.client.disconnect()

    async def send(self, characteristic=None, devID=None, commID=None, targetId=None, data=[]):
        """
        Generate databytes of command using input dictionary
        This protocol copied completely from JS library
        Messages are represented as:
        [start flags targetID sourceID deviceID commandID seqNum data
        checksum end]
        The flags byte indicates which fields are populated.
        The checksum is the ~sum(message[1:-2]) | 0xff.
        """
        self.sequence = (self.sequence + 1) % 256
        running_sum = 0
        command = []
        command.append(SendPacketConstants["StartOfPacket"])
        if targetId is None:
            cmdflg = Flags["requestsResponse"] | \
                     Flags["resetsInactivityTimeout"] | 0
            command.append(cmdflg)
            running_sum += cmdflg
        else:
            cmdflg = Flags["requestsResponse"] | \
                     Flags["resetsInactivityTimeout"] | targetId
            command.append(cmdflg)
            running_sum += cmdflg
            command.append(targetId)
            running_sum += targetId

        command.append(devID)
        running_sum += devID
        command.append(commID)
        running_sum += commID
        command.append(self.sequence)
        running_sum += self.sequence

        if data is not None:
            for datum in data:
                command.append(datum)
                running_sum += datum
        checksum = (~running_sum) & 0xff
        command.append(checksum)
        command.append(SendPacketConstants["EndOfPacket"])
        await self.client.write_gatt_char(characteristic, command)

    async def wake(self):
        """
        Bring device out of sleep mode (can only be done if device was in sleep, not deep sleep).
        If in deep sleep, the device should be connected to USB power to wake.
        """
        print("[SEND {}] Waking".format(self.sequence))

        await self.send(
            characteristic=self.API_V2_characteristic,
            devID=DeviceID["powerInfo"],
            commID=PowerCommandIDs["wake"],
            data=[])  # empty payload

    async def setBothLEDColors(self, red=None, green=None, blue=None):
        """
        Set device LED color based on RGB vales (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting front LED colour to [{}, {}, {}]".format(self.sequence, red, green, blue))

        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["userIO"],
                        commID=UserIOCommandIDs["allLEDs"],
                        data=[0x3f, red, green, blue, red, green, blue])

    async def setFrontLEDColor(self, red=None, green=None, blue=None):
        """
        Set device front LED color based on RGB vales (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting front LED colour to [{}, {}, {}]".format(self.sequence, red, green, blue))

        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["userIO"],
                        commID=UserIOCommandIDs["allLEDs"],
                        data=[0x07, red, green, blue])

    async def setBackLEDColor(self, red=None, green=None, blue=None):
        """
        Set device back LED color based on RGB vales (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting back LED colour to [{}, {}, {}]".format(self.sequence, red, green, blue))

        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["userIO"],
                        commID=UserIOCommandIDs["allLEDs"],
                        data=[0x38, red, green, blue])

    async def setMatrixLED(self, red=None, green=None, blue=None):
        """
        Set the LED matrix based on RBG values.
        """
        print("[SEND {}] Setting matrix LED colour to [{}, {}, {}]".format(self.sequence, red, green, blue))
        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["userIO"],
                        commID=UserIOCommandIDs["matrixColor"],
                        targetId=0x012,
                        data=[red, green, blue])

    async def setMatrixLEDChar(self, char=None, red=None, green=None, blue=None):
        """
        Write a character to the LED matrix, with a colour based on RGB values.
        """
        print("[SEND {}] Setting matrix char to ' {} ' LED colour to [{}, {}, {}]".format(self.sequence, char, red, green, blue))
        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["userIO"],
                        commID=UserIOCommandIDs["printChar"],
                        targetId=0x012,
                        data=[red, green, blue, ord(char)])

    async def roll(self, speed=None, heading=None):
        """
        Rolls the device at a specified speed (int between 0 and 255)
        and heading (int between 0 and 359).
        Data is format [speed, heading byte 1, heading byte 2, direction (0-forward, 1-back)].
        """
        print("[SEND {}] Rolling with speed {} and heading {}".format(self.sequence, speed, heading))
        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["driving"],
                        commID=DrivingCommands["driveWithHeading"],
                        targetId=0x012,
                        data=[speed, (heading >> 8) & 0xff, heading & 0xff, 0])

    async def resetYaw(self):
        print("[SEND {}] Resetting yaw".format(self.sequence))

        await self.send(characteristic=self.API_V2_characteristic,
                        devID=DeviceID["driving"],
                        commID=DrivingCommands["resetYaw"],
                        data=[])

    def bitsToNum(self, bits):
        """
        This helper function decodes bytes from sensor packets into single precision floats. Encoding follows the
        the IEEE-754 standard.
        """
        num = int(bits, 2).to_bytes(len(bits) // 8, byteorder='little')
        num = struct.unpack('f', num)[0]
        return num
