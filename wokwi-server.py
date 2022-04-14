#!/usr/bin/env python

import asyncio
import base64
import json
import sys

import websockets
import webbrowser


PORT = 9012


def base64_file(path: str):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('ascii')


async def hello(websocket, path):
    msg = await websocket.recv()
    print("Client connected! {}".format(msg))

    # Send the simulation payload
    await websocket.send(json.dumps({
        "type": "start",
        "elf": base64_file('blink.elf'),
        "espBin": [
            [0x1000, base64_file('/home/vscode/workspace/config-files/esp32_bootloader.bin')],
            [0x8000, base64_file('/home/vscode/workspace/config-files/esp32_partition-table.bin')],
            [0x10000, base64_file('/home/vscode/workspace/websocket-test/app.bin')],
        ]
    }))

    while True:
        msg = await websocket.recv()
        msgjson = json.loads(msg)
        if msgjson["type"] == "uartData":
            sys.stdout.buffer.write(bytearray(msgjson["bytes"]))
            sys.stdout.flush()
        else:
            print("> {}".format(msg))


start_server = websockets.serve(hello, "127.0.0.1", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
url = "https://wokwi.com/_alpha/wembed/327866241856307794?partner=espressif&port={}&data=demo".format(PORT)
print("Web socket listening on port {}".format(PORT))
print("")
print("Now go to https://wokwi.com/_alpha/wembed/327866241856307794?partner=espressif&port={}&data=demo".format(PORT))
webbrowser.open(url)
asyncio.get_event_loop().run_forever()