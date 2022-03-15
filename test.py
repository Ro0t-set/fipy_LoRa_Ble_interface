import ubinascii
import pycom


try:
    from pymesh_config import PymeshConfig
except:
    from _pymesh_config import PymeshConfig

try:
    from pymesh import Pymesh
except:
    from _pymesh import Pymesh

def new_message_cb(rcv_ip, rcv_port, rcv_data):
    ''' callback triggered when a new packet arrived '''
    print('Incoming %d bytes from %s (port %d):' %
            (len(rcv_data), rcv_ip, rcv_port))
    print(rcv_data)

    # user code to be inserted, to send packet to the designated Mesh-external interface
    for _ in range(3):
        pycom.rgbled(0x888888)
        time.sleep(.2)
        pycom.rgbled(0)
        time.sleep(.1)
    return

try: pymesh
except:
    try:
        pymesh = pybytes.__pymesh.__pymesh
    except:
        pycom.heartbeat(False)
        # read config file, or set default values
        pymesh_config = PymeshConfig.read_config()
        #initialize Pymesh
        pymesh = Pymesh(pymesh_config, new_message_cb)






class PyMeshInterface:
    """docstring forPyMeshInterface."""

    def __init__(self):
        global pymesh
        self.pymesh = pymesh




    """send a message at all node of pymesh net, ts = 1, id = 0 """
    def send_brodcast_message(self, data):
        node = self.pymesh.mesh.get_mesh_mac_list()
        node_mac = node.values()
        my_mac = self.pymesh.mac()
        for node in node_mac:
            for mac in node:
                if(my_mac != mac):
                    self.pymesh.mesh.send_message({"to" : mac, "b" : data, "ts": 1, "id":0})


mesh = PyMeshInterface()

mesh.send_brodcast_message("testo")
