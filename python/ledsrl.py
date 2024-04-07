 #!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Created By  : Venture M - venturemuk@gmail.com
# Created Date: 7th April in the Year of Our Lord 2024 
# version ='1.0'
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
__author__ = "Venture Misquitta"
__copyright__ = "Copyright 2024, The S1 TFT Project"
__credits__ = ["Venture Misquitta", "@tjaworski" ]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Venture M"
__email__ = "venturemuk@gmail.com"
__status__ = "Released"
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
import serial
from time import sleep
from serial.tools import list_ports
from enum import Enum
import datetime
import logging
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
date_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'led_srl_{date_stamp}.log', encoding='utf-8', level=logging.INFO)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
class LEDOperation(Enum):
    RAINBOW = 1
    BREATHING = 2
    CYCLE = 3
    OFF = 4
    AUTO = 5
   
    @classmethod
    def __contains__(cls, item): 
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

class LEDIntensity(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5

    @classmethod
    def __contains__(cls, item): 
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True 

class LEDSpeed(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5

    @classmethod
    def __contains__(cls, item): 
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


# ---------------------------------------------------------------------------
def probe_led_interface():
    '''
    Probes for a CH341 based serail interface on the machine.
            Parameters: None                    
            Returns:
                    device name as identified by underlying system
    '''
    VID = 0x1a86
    PID = 0x7523
    dev_name = None
    device_list = list_ports.comports()
    for device in device_list:
        if (device.vid != None and  device.pid != None and device.vid == VID and device.pid== PID ):
            logger.debug(f"Detected device at {device.name}")
            dev_name = device.name
        else:
            logger.error(f"Device not Detected")
    return (dev_name)

# ---------------------------------------------------------------------------
def rest_of_the_process():
    '''
    Intial test code that is no longer used . Deprecated !
    '''
    s = serial.Serial('/dev/ttyUSB0', timeout=10,baudrate=10000)
    data_to_write = b"\xfa\x04\x01\x01\x00"

    logger.debug(s)
    try:
        s.open()    
    except:
        pass

    logger.debug(s.writable())

    data_off   = [b'\xfa', b'\x04' , b'\x03' , b'\x03' , b'\x04']
    data_auto  = [b'\xfa', b'\x05' , b'\x03' , b'\x03' , b'\x05']
    data_auto43  = [b'\xfa', b'\x05' , b'\x03' , b'\x02' , b'\x04']
    data_auto53  = [b'\xfa', b'\x05' , b'\x03' , b'\x01' , b'\x03']
    data_auto54  = [b'\xfa', b'\x05' , b'\x02' , b'\x01' , b'\x02']
    data_auto55  = [b'\xfa', b'\x05' , b'\x01' , b'\x01' , b'\x01']

    data_auto11  = [b'\xfa', b'\x05' , b'\x05' , b'\x05' , b'\x09']
    data_auto52  = [b'\xfa', b'\x05' , b'\x04' , b'\x05' , b'\x08']

    data_rainbow  = [b'\xfa', b'\x01' , b'\x03' , b'\x03' , b'\x01']
    data_breath  = [b'\xfa', b'\x02' , b'\x03' , b'\x03' , b'\x02']
    data_cycle  = [b'\xfa', b'\x03' , b'\x03' , b'\x03' , b'\x03']

    data = data_off

    for i in range(0,100):
        sleep(5)
        match(i%4):
            case 0 :
                logger.info("OFF")
                data = data_off
            case 1 :
                logger.info("Rainbow")
                data = data_rainbow
            case 2 :
                logger.info("Breath")
                data = data_breath
            case 3 :
                logger.info("Cycle")
                
                data = data_cycle
        for d in data:
            res = s.write(d)    
            sleep(0.005)

    s.flush()
    s.close()

# ---------------------------------------------------------------------------
def connect_device(name):
    '''
    Connects to the serial device as identified by name param
            Parameters: 
                    Name : String name of the device - usually /dev/{name}
            Returns:
                    Instance of serial device
    '''
    s = serial.Serial(f'/dev/{name}', timeout=10,baudrate=10000)
    logger.debug(s)
    try:
        if (not s.is_open):
            s.open()    
    except Exception as e:
        print(e)
        exit(-1)
    logger.info(f"Device writable : {s.writable()}")
    return s

# ---------------------------------------------------------------------------
def setup_data(operation: LEDOperation , brightness: LEDIntensity , speed : LEDSpeed ): # type: ignore
    '''
    Create the data payload based on ENUM param passed. 
    Refer to enums on top for param values permissible.
    Default  return on invalid input is AUTO
            Parameters: 
                    operation  : Operation / theme as identified by LEDOperation enum
                    brightness : Intensity / brightness as identified by LEDIntensity enum
                                 LEVEL1 is highest intensity
                    speed      : Speed / interval as identified by LEDSpeed enum
                                 LEVEL1 is fastest speed
            Returns:
                    Payload of data with CRC to be sent to serial device
    '''    
    data_auto  = [b'\xfa', b'\x05' , b'\x03' , b'\x03' , b'\x05']
    logger.debug(f"INPUTS {operation} {brightness}  {speed}")
    if operation in LEDOperation  and brightness in LEDIntensity and  speed in LEDSpeed :   
        
        data_packet=[b'\xfa']
        data_packet.append(operation.value.to_bytes(1,"big"))
        data_packet.append(brightness.value.to_bytes(1,"big"))
        data_packet.append(speed.value.to_bytes(1,"big"))
        crc = (( 0xFA + operation.value+ brightness.value+speed.value )) & 0x0F
        logger.debug(f"CRC = {crc}")
        data_packet.append(crc.to_bytes(1,"big"))
        logger.info (f"DATA PACKET {data_packet}")
        return (data_packet)

    else:
        logger.warn("Invalid inputs. Setting default AUTO")
        return (data_auto)
 
# ---------------------------------------------------------------------------
def send_command(sDev, data):
    '''
    Send the data passed to serial device
            Parameters: 
                    sDev  : Serial device to send the data to
                    data  : Payload data to be sent to the device
            Returns:
                    None
    '''   
    for d in data:
        res = sDev.write(d)    
        sleep(0.005)

# ---------------------------------------------------------------------------
def cleanup(sDev):
    '''
    Flush and close the serial device
            Parameters: 
                    sDev  : Serial device to cleanup and close
            Returns:
                    None
    '''   
    sDev.flush()
    sDev.close()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def main():
    deviceHandle = probe_led_interface()
    logger.debug (f"Device handle : {deviceHandle} ")

    sDev = connect_device(deviceHandle)
    data = setup_data(LEDOperation.BREATHING,LEDIntensity.LEVEL_1,LEDSpeed.LEVEL_1)

    logger.debug(data)
    send_command(sDev, data)

    cleanup(sDev)
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
if  __name__ == "__main__":
    main()
# ---------------------------------------------------------------------------