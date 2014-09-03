
from Adafruit_I2C import Adafruit_I2C
import smbus
import time

MCP9808_I2CADDR_DEFAULT =       0x18

MCP9808_REG_CONFIG_SHUTDOWN =   0x0100
MCP9808_REG_CONFIG_CRITLOCKED = 0x0080
MCP9808_REG_CONFIG_WINLOCKED =  0x0040
MCP9808_REG_CONFIG_INTCLR =     0x0020
MCP9808_REG_CONFIG_ALERTSTAT =  0x0010
MCP9808_REG_CONFIG_ALERTCTRL =  0x0008
MCP9808_REG_CONFIG_ALERTSEL =   0x0002
MCP9808_REG_CONFIG_ALERTPOL =   0x0002
MCP9808_REG_CONFIG_ALERTMODE =  0x0001

MCP9808_REG_CONFIG =            0x01
MCP9808_REG_UPPER_TEMP =        0x02
MCP9808_REG_LOWER_TEMP =        0x03
MCP9808_REG_CRIT_TEMP =         0x04
MCP9808_REG_AMBIENT_TEMP =      0x05
MCP9808_REG_MANUF_ID =          0x06
MCP9808_REG_DEVICE_ID =         0x07

class MCP9808(object):

    def __init__(self, address = MCP9808_I2CADDR_DEFAULT, busnum=-1):
        self.i2c = Adafruit_I2C(address=address, busnum=busnum)
        self.address = address
        if self._readU16(MCP9808_REG_MANUF_ID) != 0x0054: raise Exception()
        if self._readU16(MCP9808_REG_DEVICE_ID) != 0x0400: raise Exception()

    def _readU16(self, reg):
        ret = self.i2c.readList(reg, 2)
        return (ret[0] << 8) + ret[1]

    def readTempC(self):
        t = self._readU16(MCP9808_REG_AMBIENT_TEMP)
        temp = t & 0x0FFF
        temp /= 16.0
        if t & 0x1000: temp -= 256
        return temp

if __name__ == '__main__':
    mcp = MCP9808()

    print "Reading temperature (CTRL+C to quit)"
    while (True):
        c = mcp.readTempC()
        f = c * 9.0 / 5.0 + 32
        print "Temperature = %.3f C %.3f F" % (c, f)
        time.sleep(1);

