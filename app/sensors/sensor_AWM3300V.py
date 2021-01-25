from app.sensors.sensor_base import Sensor

import smbus2

ARDUINO_NANO_I2C_ADDRESS = 0x14

class NANO_I2C_CMD():
    CMD_REG_WRITE = 0x00
    A_READ_A0 = 0x10
    A_READ_A1 = 0x11
    A_READ_A2 = 0x12
    A_READ_A3 = 0x13
    A_READ_A4 = 0x14
    A_READ_A5 = 0x15
    SDI12_READ = 0x20
    UART_READ = 0x30

class AWM3300V(Sensor):
    def __init__(self, id):
        type = "MPL3115A2"
        protocol = "ANALOG"
        address = 14
        measurements = [
            "mass_flow"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        return {
            "mass_flow": self.read_mass_flow()
        }

    def read_mass_flow(self) -> float:
        # TODO: Make sure to receive 2 bytes instead of one because the nano is
        # supposed to be sending a 16-bit number!
        value = self.bus.read_byte_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.A_READ_A0)
        return value


