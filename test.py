from loRaMashInterface.LoRaMeshInterface import PyMeshInterface
import pycom
from sensors import sensors
import time
from ble import bleInteface
from machine import Timer


def json_from_data(rcv_ip, rcv_port, rcv_data):
    data = str(rcv_data, 'utf-8')
    print("Lora: ", data, " from ", rcv_ip)
    ble.write(rcv_ip + "=" + data)
    # user code to be inserted, to send packet to the designated Mesh-external interface
    for _ in range(3):
        pycom.rgbled(0x888888)
        time.sleep(.2)
        pycom.rgbled(0)
        time.sleep(.1)


mesh = PyMeshInterface(json_from_data)
ble = bleInteface.BleInterface("FiPy",
                               lambda x: mesh.send_broadcast_message(str(x[1])))


def lora_send_data(allarm):
    global mesh
    mesh.send_broadcast_message(str(sensors.get_temperature()))
    mesh.send_broadcast_message(str(sensors.get_humidity()))
    mesh.send_broadcast_message(str({"node_info": str(mesh.pymesh.mesh.get_mesh_pairs())}))


update_alarm = Timer.Alarm(lora_send_data, 10, periodic=True)
