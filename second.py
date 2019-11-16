import time
import asyncio

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


async def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('gr1 started work: {}'.format(tic()))
    await asyncio.sleep(3)
    print('gr1 ended work: {}'.format(tic()))


async def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('gr2 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


async def gr3():
    print("Let's do some stuff while the coroutines are blocked, {}".format(tic()))
    await asyncio.sleep(1)
    print("Done!")


async def gr4():
    print('execute gr4')
    return 2


async def gr5(x):
    print('execute gr5')
    return x + 2

async def main():
    print('Execute main')
    gr4_res = await gr4()
    lol = await gr5(gr4_res)


ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(gr1()),
    ioloop.create_task(gr2()),
    ioloop.create_task(gr3())
]
print('start tasks')
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.run_until_complete(main())

ioloop.close()
