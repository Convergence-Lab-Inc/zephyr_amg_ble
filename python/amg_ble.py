import platform
import sys
import asyncio
import logging
import struct
import time
import matplotlib.pyplot as plt
import numpy as np

from bleak import BleakClient


async def run(address, debug=False):
    log = logging.getLogger(__name__)
    async with BleakClient(address) as client:
        log.info(f"Connected: {client.is_connected}")

        plt.ion()
        graph = plt.imshow(np.reshape(np.repeat(0,64),(8,8)),cmap=plt.cm.hot,interpolation='lanczos')
        plt.draw()
        while True:
            value = bytes(await client.read_gatt_char("12345678-1234-5678-1234-56789abcdef1"))
            print(len(value))
            print(value)
            value_ints = struct.unpack('<HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH', value)
            value_ints = np.array(value_ints).reshape(8, 8)
            graph = plt.imshow(value_ints,cmap=plt.cm.hot,interpolation='lanczos')
            plt.pause(0.01)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python amg88xx_ble.py [MAC ADDRESS]")

    print(sys.argv)
    address = (
        sys.argv[1]
    )
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address, True))
