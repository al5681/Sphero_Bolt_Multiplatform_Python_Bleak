import asyncio

from random import randrange
from sphero_bolt import SpheroBolt


async def run():
    # mac address of sphero bolt
    address = (
        "CC:F7:8F:11:BC:51"
    )

    # connect to sphero bolt
    my_sphero = SpheroBolt(address)
    try:
        await my_sphero.connect()

        # wake sphero
        await my_sphero.wake()
        await asyncio.sleep(1)
        await my_sphero.setBothLEDColors(0, 0, 0)

        for _ in range(10):
            await my_sphero.setMatrixLED(red=randrange(255), \
                                             green=randrange(255), blue=randrange(255))

            await asyncio.sleep(0.5)

    finally:
        await my_sphero.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
