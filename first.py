import asyncio


async def foo():
    print("Running in foo")
    await asyncio.sleep(1)
    print("Explicit context switch to foo again")

    print(1)
    return 1


async def bar(arg):
    print("Explicit context to bar")
    await asyncio.sleep(2)
    print("Implicit context switch back to bar")
    print(arg+10)


async def main():
    print("Set tasks to list")
    foo_res = await foo()
    res_bar = await bar(foo_res)

print("Create ioloop")
ioloop = asyncio.get_event_loop()
print('Run untill complete end')
ioloop.run_until_complete(main())
print('Close ioloop')
ioloop.close()
