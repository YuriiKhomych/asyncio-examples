from collections import namedtuple
import time
import asyncio
from concurrent.futures import FIRST_COMPLETED
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service(name='ipify', url='https://api.ipify.org?format=json', ip_attr='ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def fetch_ip(service, session):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    async with session.get(service.url) as response:
        json_response = await response.json()
        ip = json_response[service.ip_attr]

        response.close()
        return '{} finished with result: {}, took: {:.2f} seconds'.format(
            service.name, ip, time.time() - start)


async def asynchronous():
    async with aiohttp.ClientSession() as session:
        futures = [fetch_ip(service, session) for service in SERVICES]
        done, pending = await asyncio.wait(
            futures, return_when=FIRST_COMPLETED)

        print(done.pop().result())
        for future in pending:
            future.cancel()


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()