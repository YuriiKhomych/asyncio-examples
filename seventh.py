from collections import namedtuple
import time
import asyncio
import aiohttp
import traceback

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service, session):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    try:
        async with session.get(service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]
            return f'{service.name} finished with result: {ip},' \
                f' took: {time.time() - start:.2f} seconds'
    except:
        return f'{service.name} is unresponsive'


async def asynchronous():
    async with aiohttp.ClientSession() as session:
        futures = [fetch_ip(service, session) for service in SERVICES]
        done, _ = await asyncio.wait(futures)

        for future in done:
            try:
                print(future.result())
            except:
                print(f'Unexpected error: {traceback.format_exc()}')


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
