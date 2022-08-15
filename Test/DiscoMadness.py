import asyncio

from sphero_bolt import SpheroBolt, BoltScan
from random import randrange

async def spt(address):
    my_sphero = SpheroBolt(address)
    try:
        await my_sphero.connect()

        # wake sphero
        await my_sphero.wake()

        await my_sphero.resetYaw()
        await asyncio.sleep(2)

        # roll in a square
        while True:
            await my_sphero.roll(randrange(256), randrange(359))
            #await asyncio.sleep(2)
            await my_sphero.setFrontLEDColor(red=randrange(255), \
                                             green=randrange(255), blue=randrange(255))
            await my_sphero.setBackLEDColor(red=randrange(255), \
                                            green=randrange(255), blue=randrange(255))
            await my_sphero.setMatrixLED(red=randrange(255), \
                                             green=randrange(255), blue=randrange(255))

    finally:
        await my_sphero.disconnect()

async def run():
    # mac address of sphero bolt
    #address = (
        #"CC:F7:8F:11:BC:51"
    #)
    scan = BoltScan()
    address = await scan.scanAll()
    print('{} Spheros Detected'.format(len(address)))
    tasks = []
    for f in address:
        task = asyncio.ensure_future(spt(f))
        tasks.append(task)
        #await asyncio.create_task(spt(f))
        #await task_1
    # connect to sphero bolt
    responses = await asyncio.gather(*tasks)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
