from network import Bluetooth


def conn_cb(chr):
    events = chr.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print('BLE client connected')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print('BLE client disconnected')


class BleInterface:

    def __init__(self, name, on_message_callback):
        self.value = ""
        self.on_message_callback = on_message_callback
        self.bluetooth = Bluetooth()
        self.bluetooth.set_advertisement(name=name, manufacturer_data="Pycom", service_uuid=0xec00)
        self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED,
                                handler=conn_cb)
        self.bluetooth.advertise(True)
        self.srv = self.bluetooth.service(uuid=0xec00, isprimary=True, nbr_chars=1)
        self.chr = self.srv.characteristic(uuid=0xec0e, value='read_from_here')  # client reads from here
        self.chr.callback(trigger=(Bluetooth.CHAR_WRITE_EVENT |
                                   Bluetooth.CHAR_READ_EVENT |
                                   Bluetooth.CHAR_SUBSCRIBE_EVENT),
                          handler=self.chr_handler)

    def chr_handler(self, chr, data):
        events = chr.events()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            self.on_message_callback(data)

    def write(self, txt_value):
        try:
            self.value = txt_value
            self.chr.value(self.value)
        except:
            pass
