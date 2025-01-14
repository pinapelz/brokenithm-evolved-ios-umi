import mmap
import ctypes
import time
import key_config
import umi_led
import threading
import keyboard

class SharedMemoryData(ctypes.Structure):
    _fields_ = [
        ("airIoStatus", ctypes.c_uint8 * 6),
        ("sliderIoStatus", ctypes.c_uint8 * 32),
        ("ledRgbData", ctypes.c_uint8 * 96),
        ("reserved", ctypes.c_uint8 * 4)
    ]

# Shared memory details
SHARED_MEMORY_NAME = "Local\\BROKENITHM_SHARED_BUFFER"
SHARED_MEMORY_SIZE = ctypes.sizeof(ctypes.c_uint8) * ctypes.sizeof(SharedMemoryData)


def initialize_shared_mem():
    try:
        shared_memory = mmap.mmap(-1, SHARED_MEMORY_SIZE, tagname=SHARED_MEMORY_NAME, access=mmap.ACCESS_WRITE)
        slider_status = [0] * 32  # Default: All slider zones inactive
        air_status = [0] * 6  # Default: All air zones inactive
        shared_memory.seek(0)
        shared_memory.write(bytearray(air_status))
        print("[Initialization] Resetting Air Note Status")
        shared_memory.seek(6)
        shared_memory.write(bytearray(slider_status))
        print("[Initialization] Resetting Slider Status")
        shared_memory.seek(6 + 32) 
        print("[Initialization] Setting Default Slider LED state")
        shared_memory.write(bytearray(umi_led.DEFAULT_LED_STATE))
        print("[Initialization] Success. Complete")
        return shared_memory
    except Exception:
        print("[Error] A Fatal Error occured while trying to write to the Shared Memory while initializing")
        return None

def monitor_key_presses_and_air(controller: key_config.InputConfig):
    try:
        shared_memory = mmap.mmap(-1, SHARED_MEMORY_SIZE, tagname=SHARED_MEMORY_NAME, access=mmap.ACCESS_READ)
        key_states = {zone: False for zone in controller.get_keyzone_layout().keys()}
        air_states = {zone: False for zone in controller.get_airzone_layout().keys()}
        print("Now Monitoring for Inputs")
        while True:
            shared_memory.seek(0)
            current_air_status = list(shared_memory.read(6))
            shared_memory.seek(6)
            current_slider_status = list(shared_memory.read(32))
            for zone, key in controller.get_keyzone_layout().items():
                is_pressed = current_slider_status[zone] == 128
                if is_pressed != key_states[zone]:
                    if is_pressed:
                        keyboard.press(key)
                        print(f"Key {key} pressed")
                    else:
                        keyboard.release(key)
                        print(f"Key {key} released")
                    key_states[zone] = is_pressed
            for zone, key in controller.get_airzone_layout().items():
                is_active = current_air_status[zone] == 128
                if is_active != air_states[zone]:
                    if is_active:
                        keyboard.press(key)
                        print(f"Air {key} activated")
                    else:
                        keyboard.release(key)
                        print(f"Air {key} deactivated")
                    air_states[zone] = is_active
            time.sleep(0.01)
    except Exception:
        print("[Error] A Fatal Error occured while monitoring and translating inputs")
    except KeyboardInterrupt:
        for key in controller.get_keyzone_layout().values():
            keyboard.release(key)
        for key in controller.get_airzone_layout().values():
            keyboard.release(key)
        print("Stopping monitoring.")


if __name__ == "__main__":
    shared_memory = initialize_shared_mem()
    controller = key_config.Umiguri32KeyZone()
    if shared_memory is not None:
        stop_event = threading.Event()
        server_thread = threading.Thread(target=umi_led.start_umiguri_websocket_server, args=(shared_memory, stop_event))
        server_thread.start()
        monitor_key_presses_and_air(controller)
        print("Shutting down...")
        stop_event.set()
        shared_memory.close()
        exit()

