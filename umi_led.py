"""
Umiguri LED Controller Protocol. Some commands have been stubbed
Thanks inonote for the great resources on the protocol
https://gist.github.com/inonote/00251fed881a82c9df1e505eef1722bc

The implementation below is largely derived from
https://github.com/inonote/UmiguriSampleLedServer/blob/master/src/App.cpp
"""

import asyncio
import websockets

kLedServerPort = 7124
kLedServerName = "BrokenithmLedServer"
kLedServerVersion = (123, 456)
kLedServerHardwareName = "Brokenithm"
kLedServerHardwareVersion = (987, 654)

kLedProtocolVersion = 0x01

ULED_COMMAND_SET_LED             = 0x10
ULED_COMMAND_INITIALIZE          = 0x11
ULED_COMMAND_READY               = ULED_COMMAND_INITIALIZE | 0x08  # 0x19
ULED_COMMAND_PING                = 0x12
ULED_COMMAND_PONG                = ULED_COMMAND_PING | 0x08        # 0x1A
ULED_COMMAND_REQUEST_SERVER_INFO = 0xD0
ULED_COMMAND_REPORT_SERVER_INFO  = ULED_COMMAND_REQUEST_SERVER_INFO | 0x08  # 0xD8

DEFAULT_LED_STATE = [
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0, 
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255, 0, 0, 0,
        255, 255, 255
]

SHOW_LOG = False

def log_message(message: str):
    if not SHOW_LOG:
        return
    print(message)

def validate_message(payload: bytes) -> bool:
    """
    Checks if the incoming payload conforms to the protocol:
      1. At least 3 bytes: [protocolVersion, command, length].
      2. The length byte must match (payload.size() - 3).
      3. For known commands, check expected payload size if needed.
    """
    if len(payload) < 3:
        return False

    if payload[0] != kLedProtocolVersion:
        return False

    length_byte = payload[2]
    if length_byte != (len(payload) - 3):
        return False

    command = payload[1]
    if command == ULED_COMMAND_SET_LED:
        if len(payload) != 106:  # 103 bytes of LED data + 3 header bytes
            return False
    elif command == ULED_COMMAND_PING:
        if len(payload) != 7:  # 4 bytes payload + 3 header bytes
            return False

    return True

def get_brokenithm_led_array(payload):
    led_state = []
    land_colors = []
    border_colors = []
    for i in range(16):
        offset = 1 + i * 3
        land_colors.append(tuple(payload[offset:offset + 3]))

    for i in range(15):
        offset = 49 + i * 3
        border_colors.append(tuple(payload[offset:offset + 3]))
    land_colors = list(reversed(land_colors))
    border_colors = list(reversed(border_colors))
    try:
        for i in range(15):
            led_state.append(land_colors[i][2])
            led_state.append(land_colors[i][0])
            led_state.append(land_colors[i][1])
            led_state.append(border_colors[i][2])
            led_state.append(border_colors[i][0])
            led_state.append(border_colors[i][1])
        led_state.append(land_colors[15][2])
        led_state.append(land_colors[15][0])
        led_state.append(land_colors[15][1])
    except Exception:
        log_message("[LEDServer] Invalid LED State received ignoring")
        return None
    return led_state

# R,G,B  -> B,R,G

async def handle_message(websocket, payload: bytes, shared_memory):
    """
    Process incoming (validated) payload and respond if needed.
    """
    command = payload[1]
    log_message(f"Received raw data ({len(payload)} bytes): {payload}")

    if command == ULED_COMMAND_PING:
        log_message("-> Handling PING command")
        custom_data = payload[3:7]
        response = bytearray([kLedProtocolVersion, ULED_COMMAND_PONG, 6]) + custom_data + bytearray([0x51, 0xED])
        await websocket.send(response)

    elif command == ULED_COMMAND_INITIALIZE:
        log_message("-> Handling INITIALIZE command")
        response = bytearray([kLedProtocolVersion, ULED_COMMAND_READY, 0])
        await websocket.send(response)

    elif command == ULED_COMMAND_REQUEST_SERVER_INFO:
        log_message("-> Handling REQUEST_SERVER_INFO command")
        buf = bytearray(3 + 44)
        buf[0] = kLedProtocolVersion
        buf[1] = ULED_COMMAND_REPORT_SERVER_INFO
        buf[2] = 44

        name_bytes = kLedServerName.encode('ascii')[:16]
        buf[3:3+len(name_bytes)] = name_bytes

        ver0, ver1 = kLedServerVersion
        buf[3+16] = ver0 & 0xFF
        buf[3+17] = (ver0 >> 8) & 0xFF
        buf[3+18] = ver1 & 0xFF
        buf[3+19] = (ver1 >> 8) & 0xFF

        hw_bytes = kLedServerHardwareName.encode('ascii')[:16]
        buf[3+22:3+22+len(hw_bytes)] = hw_bytes

        hwver0, hwver1 = kLedServerHardwareVersion
        buf[3+38] = hwver0 & 0xFF
        buf[3+39] = (hwver0 >> 8) & 0xFF
        buf[3+40] = hwver1 & 0xFF
        buf[3+41] = (hwver1 >> 8) & 0xFF

        await websocket.send(buf)

    elif command == ULED_COMMAND_SET_LED:
        log_message("-> Handling SET_LED command")
        brightness = payload[3]
        led_data = payload[3:]
        log_message(f"   Brightness: {brightness}")
        log_message(f"   LED color data length: {len(led_data)}")
        led_arr = get_brokenithm_led_array(led_data)
        if led_arr is None:
            return
        shared_memory.seek(6 + 32)
        shared_memory.write(bytearray(led_arr))

    else:
        log_message(f"-> Unknown command 0x{command:02X}")

async def handle_client(websocket, shared_memory):
    """
    Main entry point for each connected client.
    Listens for messages, validates them, and calls handle_message.
    """
    print(f"[LEDServer] Client Detected from: {websocket.remote_address}")
    try:
        async for raw_message in websocket:
            if isinstance(raw_message, bytes):
                if validate_message(raw_message):
                    await handle_message(websocket, raw_message, shared_memory)
                else:
                    log_message(f"Invalid message received: {raw_message}")
            else:
                log_message(f"Received text message (ignored): {raw_message}")
    except websockets.exceptions.ConnectionClosed as e:
        log_message(f"Client disconnected: {e.reason}")

async def run_websocket_server(shared_memory, stop_event):
    print(f"[LEDerver] Starting WebSocket server on port {kLedServerPort}...")
    async with websockets.serve(lambda ws: handle_client(ws, shared_memory), "0.0.0.0", kLedServerPort):
        print("[LEDServer] LEDServer started. Awaiting connections...")
        while not stop_event.is_set():
            await asyncio.sleep(0.1)
        print("[LEDServer] Websocket Server Shutting Down")

def start_umiguri_websocket_server(shared_memory, stop_event):
    try:
        asyncio.run(run_websocket_server(shared_memory, stop_event))
    except KeyboardInterrupt:
        log_message("Keyboard Interrupt Received - Server stopped.")
