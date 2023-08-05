import serial
from .chip_mode import *
from sys import version_info

class SPI_rack(serial.Serial):
    """SPI rack interface class

    The SPI rack class is used to interface with the SPI rack controller unit.
    It implements the protocol used to read and write data and set an active
    module. Use the writeData/readData functions instead of the read/write
    functions of the serial library.

    An instance of SPI rack needs to be passed to every module.

    Attributes:
        activeModule: keeps track of which module is currently active
        activeChip: keeps track of which chip in a module is currently active
        refFrequency: the current reference frequency (in Hz)
    """

    def __init__(self, port, baud, timeout, ref_frequency=10e6):
        """Inits SPI_rack class

        Args:
            port: serial port used by SPI rack controller unit (string)
            baud: baud rate value (int)
            timeout: data receive timout in seconds (float)
            refFrequency: backplane reference frequency in Hz (int)

        Raises:
            ValueError: if parameters (baud rate) are out of range
            SerialException: in case serial device cannot be found or configured

        Example:
            SPI_Rack_1 = SPI_rack("COM1", 1000000, 1)
        """
        try:
            super(SPI_rack, self).__init__(port, baud, timeout = timeout)
        except ValueError:
            print("Timout value out of bound.")
        except serial.SerialException:
            print("Cannot open serial port: " + port)

        self.active_module = None
        self.active_chip = None
        self.ref_frequency = ref_frequency

    def set_ref_frequency(self, frequency):
        """Set the reference frequency present on the backplane (Hz)

        The reference frequency is shared between all modules. This info
        can be used by other modules for calculation, for example the
        s5i RF generator module needs to know the frequency.

        Args:
            frequency: the reference frequency on the backplane (in Hz)
        """
        self.ref_frequency = frequency

    def set_active(self, module, chip, SPI_mode):
        """Set the current module/chip to active on controller unit

        By writing 'c' and then chip/module combination, this chip will
        be set active in the SPI rack controller. This means that all the data
        send after this will go to that chip.

        Args:
            module: module number to set active (int)
            chip: chip in module to set active (int)
            SPI_mode: SPI mode of the chip to be activated (int)
        """

        s_data = bytearray([ord('c'), (chip<<4) | module, SPI_mode])
        self.write(s_data)

        self.active_module = module
        self.active_chip = chip

    def write_data(self, module, chip, SPI_mode, data):
        """Write data to selected module/chip combination

        Args:
            module: number of the module to send data to (int)
            chip: chip in module to send data to (int)
            SPI_mode: SPI mode of the chip to be activated (int)
            data: array of data to be send (bytearray)
        """

        if self.active_module != module or self.active_chip != chip:
            self.set_active(module, chip, SPI_mode)

        data = bytearray([ord('w')]) + data
        self.write(data)

    def read_data(self, module, chip, SPI_mode, data):
        """Read data from selected module/chip combination

        Args:
            module: number of the module to send data to (int)
            chip: chip in module to send data to (int)
            SPI_mode: SPI mode of the chip to be activated (int)
            data: data to be send to chip for reading (bytearray)

        Returns:
            Bytes received from module/chip (int list)
        """
        if self.active_module != module or self.active_chip != chip:
            self.set_active(module, chip, SPI_mode)

        read_length = len(data)
        data = bytearray([ord('r')]) + data
        self.write(data)
        r_data = self.read(read_length)

        if len(r_data) < read_length:
            print("Received less bytes than expected")

        if version_info[0] < 3:
            return [ord(c) for c in r_data]
        else:
            return r_data

    def get_battery(self):
        """Returns battery voltages

        Calculates the battery voltages from the ADC channel values.

        Returns:
            Voltages (float): [VbatPlus, VbatMin]
        """
        self.read_adc(1)
        Vbatplus = 2.171*3.3*self.read_adc(1)/4096.0
        self.read_adc(0)
        Vbatmin = -2.148*3.3*self.read_adc(0)/4096.0
        return [Vbatplus, Vbatmin]

    def read_adc(self, channel):
        """Reads the ADC for battery voltage

        Reads the given ADC channel. These channels are connected to the raw
        of battery. Output needs to calculated due to voltage divider. Function
        used internally.

        Args:
            channel (int: 0-1): the ADC channel to be read
        Returns:
            12-bit ADC data (int)
        """
        s_data = bytearray([1, 160|(channel<<6), 0])
        r_data = self.read_data(0, 0, MCP320x_MODE, s_data)
        return (r_data[1]&0xF)<<8 | r_data[2]
