import asyncio

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

        # set sphero red
        await my_sphero.setFrontLEDColor(255, 0, 0)
        await my_sphero.setBackLEDColor(255, 0, 0)
        await asyncio.sleep(3)
        # set sphero white
        await my_sphero.setFrontLEDColor(255, 255, 255)
        await my_sphero.setBackLEDColor(255, 255, 255)
        await asyncio.sleep(3)
        # set sphero blue
        await my_sphero.setFrontLEDColor(0, 0, 255)
        await my_sphero.setBackLEDColor(0, 0, 255)
        await asyncio.sleep(3)

    finally:
        await my_sphero.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
