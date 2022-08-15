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

        await my_sphero.resetYaw()
        await asyncio.sleep(2)

        # roll in a square
        for i in range(4):
            await my_sphero.roll(50, 90 * i)
            await asyncio.sleep(2)

    finally:
        await my_sphero.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
