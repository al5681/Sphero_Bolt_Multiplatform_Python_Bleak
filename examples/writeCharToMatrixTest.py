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

        # Display 'U'
        await my_sphero.setMatrixLEDChar("U", 255, 0 ,0)
        await my_sphero.setBothLEDColors(255, 0 ,0)
        await asyncio.sleep(1)
        # Display 'S'
        await my_sphero.setMatrixLEDChar("S", 255, 255, 255)
        await my_sphero.setBothLEDColors(255, 255, 255)
        await asyncio.sleep(1)
        # Display 'A'
        await my_sphero.setMatrixLEDChar("A", 0, 0, 255)
        await my_sphero.setBothLEDColors(0, 0, 255)
        await asyncio.sleep(1)

    finally:
        await my_sphero.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
