from loRaMashInterface.LoRaMeshInterface import PyMeshInterface
import pycom
from sensors import sensors
import time
def jsono_from_data(rcv_ip, rcv_port, rcv_data):
    data = str(rcv_data, 'utf-8')
    print(data)

    # user code to be inserted, to send packet to the designated Mesh-external interface
    for _ in range(3):
        pycom.rgbled(0x888888)
        time.sleep(.2)
        pycom.rgbled(0)
        time.sleep(.1)
    return

mesh = PyMeshInterface(jsono_from_data)

while True:
    mesh.send_brodcast_message(str(sensors.get_temperature()))
    mesh.send_brodcast_message(str(sensors.get_humidity()))
    time.sleep(5)
