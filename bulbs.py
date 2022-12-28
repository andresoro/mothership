import os, time, argparse
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
from dotenv import load_dotenv


load_dotenv()

client = Client(token=os.environ['WYZE_ACCESS_TOKEN'])

LIVING_ROOM_LIGHT = os.environ['LIVING_ROOM_LIGHT']
BED_ROOM_LIGHT = os.environ['BED_ROOM_LIGHT']

bulbs = {
    "living": LIVING_ROOM_LIGHT,
    "bed": BED_ROOM_LIGHT
}

def get_bulb(mac_address):
    try:
        bulb = client.bulbs.info(device_mac=mac_address)
        return bulb
    except WyzeApiError as e:
        print(f"Got an error: {e}")
        return None

def bulb_info(bulb):
    print(f"power: {bulb.is_on}")
    print(f"online: {bulb.is_online}")
    print(f"brightness: {bulb.brightness}")
    print(f"temp: {bulb.color_temp}")
    print(f"color: {bulb.color}")
    
def set_brightness(bulb, level):
    try:
        client.bulbs.set_brightness(device_mac=bulb.mac, device_model=bulb.product.model, brightness=level)
    except WyzeApiError as e:
        print(f"Got an error: {e}")

def set_color(bulb, color):
    try:
        client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=color)
    except WyzeApiError as e:
        print(f"Got an error: {e}")
        
def set_temperature(bulb, level):
    try:
        client.bulbs.set_color_temp(device_mac=bulb.mac, device_model=bulb.product.model, color_temp=level)
    except WyzeApiError as e:
        print(f"Got an error: {e}")

def dim(bulb, duration):
    seconds = float(duration) * 60 * 60
    interval = seconds / float(bulb.brightness)
    
    i = bulb.brightness
    while i > 0:
        set_brightness(bulb, i)
        print(f"lowered brightness to {i}")
        i -= 1
        time.sleep(interval)

def load_args():
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding mandatory device argument
    parser.add_argument("device")
    
    # Adding optional argument
    parser.add_argument("-c", "--color", help = "Set color of desired bulb")
    parser.add_argument("-t", "--temperature", help = "Set temperature of desired bulb")
    parser.add_argument("-b", "--brightness", help = "Set brightness of desired bulb")
    parser.add_argument("-d", "--dim", help = "Dim a desired bulb within specified duration")
    
    # Read arguments from command line
    args = parser.parse_args()
    return args

def main():
    args = load_args()
    mac_address = bulbs[args.device]
    if not mac_address:
        print("requested device is not supported")
        return
    bulb = get_bulb(mac_address)
    
    if args.color:
        set_color(bulb, args.color)
    if args.temperature:
        set_temperature(bulb, args.temperature)
    if args.brightness:
        set_brightness(bulb, args.brightness)
    if args.dim:
        dim(bulb, args.dim)
    
if __name__ == "__main__":
    main()