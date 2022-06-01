import pycom

try:
    from pymesh_config import PymeshConfig
except:
    from _pymesh_config import PymeshConfig

try:
    from pymesh import Pymesh
except:
    from _pymesh import Pymesh


class PyMeshInterface:
    """docstring forPyMeshInterface."""

    def __init__(self, message_cb):
        global pycom
        self.pycom = pycom

        try:
            global pymesh
            self.pymesh = pymesh
        except:
            try:
                pymesh = pybytes.__pymesh.__pymesh
                self.pymesh = pymesh
                global pymesh
            except:
                self.pycom.heartbeat(False)
                # read config file, or set default values
                self.pymesh_config = PymeshConfig.read_config()
                # initialize Pymesh
                pymesh = Pymesh(self.pymesh_config, message_cb)
                self.pymesh = pymesh
                self.pymesh.resume(20)
                global pymesh

    def send_broadcast_message(self, data):
        node = self.pymesh.mesh.get_mesh_mac_list()
        node_mac = node.values()
        for node in node_mac:
            for mac in node:
                self.pymesh.mesh.send_message(
                    {"to": mac, "b": data, "ts": 1, "id": 0}
                )
