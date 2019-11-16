from collections import namedtuple
import time
import asyncio
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'this-is-not-an-attr'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service, session):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    try:
        async with session.get(service.url) as response:
            response = response
    except:
        return f'{service.name} is unresponsive'
    else:
        json_response = await response.json()
        ip = json_response[service.ip_attr]
        return f'{service.name} finished with result: {ip},' \
            f' took: {time.time() - start:.2f} seconds'

async def asynchronous():
    async with aiohttp.ClientSession() as session:
        futures = [fetch_ip(service, session) for service in SERVICES]
        await asyncio.wait(futures)  # intentionally ignore results


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
