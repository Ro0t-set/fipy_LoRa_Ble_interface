from loRaMashInterface.LoRaMeshInterface import PyMeshInterface
import pycom
from sensors import sensors
import time
from ble import bleInteface
from machine import Timer
import machine
from machine import WDT


wdt = WDT(timeout=120000)  # enable it with a timeout of 120 seconds


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

    global wdt
    wdt.feed()


"""initialize mesh net"""
mesh = PyMeshInterface(json_from_data)
"""initialize ble service"""
ble = bleInteface.BleInterface("FiPy",
                               lambda x: mesh.send_broadcast_message(str(x[1])))


def lora_send_data(allarm):
    global mesh
    mesh.send_broadcast_message(str({"node_info": str(mesh.pymesh.mesh.get_mesh_pairs())}))
    mesh.send_broadcast_message(str(sensors.get_temperature()))
    mesh.send_broadcast_message(str(sensors.get_battery_percentage()))


update_alarm = Timer.Alarm(lora_send_data, 20.0, periodic=True)
