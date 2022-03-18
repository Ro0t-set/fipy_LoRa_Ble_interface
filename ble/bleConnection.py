from network import Bluetooth
from machine import Timer

update_alarm = Timer
update = False
value = "test"


def update_value(txt_value):
    global value
    value = txt_value


## TODO:  conndition in this function
def write(txt_value):
    global value
    try:
        value = txt_value
        chr.value(value)
    except:
        pass


def chr_handler(chr, data):
    global value
    global update
    events = chr.events()
    print(events)
    if events & (Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT):
        chr.value(value)
        if events & Bluetooth.CHAR_SUBSCRIBE_EVENT:
            update = True
    elif events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request with value = {}".format(data))


def conn_cb(chr):
    global update_alarm
    global update
    events = chr.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        # update_alarm = Timer.Alarm(update_handler, 1, periodic=True)
        print('BLE client connected')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        # update_alarm.cancel()
        print('BLE client disconnected')
        update = False


def update_handler(update_alarm):
    global update
    global value
    if update:
        chr.value(value)


bluetooth = Bluetooth()
bluetooth.set_advertisement(name="FiPy1", manufacturer_data="Pycom", service_uuid=0xec00)
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED,
                   handler=conn_cb)
bluetooth.advertise(True)
srv = bluetooth.service(uuid=0xec00, isprimary=True, nbr_chars=1)
chr = srv.characteristic(uuid=0xec0e, value='read_from_here')  # client reads from here
chr.callback(trigger=(Bluetooth.CHAR_WRITE_EVENT |
                      Bluetooth.CHAR_READ_EVENT |
                      Bluetooth.CHAR_SUBSCRIBE_EVENT),
             handler=chr_handler)
