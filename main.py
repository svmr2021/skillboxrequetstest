import logging
import aiohttp
import asyncio
from tqdm import tqdm
import validators


class Request(object):
    async def take_input(self):
        """
        Take url from user
        :return:
        """
        try:
            url = input('Enter url:')
            if validators.url(url):
                await self.load_tasks(count=1000, url=url)
            else:
                print('Incorrect url')
                await self.take_input()
        except Exception as e:
            logging.error(e)

    async def load_tasks(self, count=0, url=None):
        """
        Create task for each request
        :param count: Number of requests
        :param url: Url
        :return:
        """
        try:
            tasks = []
            if url:
                async with aiohttp.ClientSession() as session:
                    web_site = await self.make_request(session=session, url=url)
                    if web_site:
                        # collect tasks in list
                        for _ in tqdm(range(0, count, 1), unit='tasks', desc='Preparing tasks'):
                            task = asyncio.create_task(self.make_request(session=session, url=url))
                            tasks.append(task)
                        for _ in tqdm(range(0, len(tasks), 1), unit='requests', desc=f'Requesting {url}'):
                            await asyncio.gather(*tasks)
                        print(f'Successfully requested {count} times to {url}')
                    else:
                        print('Site is not reachable')
                        await self.take_input()

            else:
                print('Url is not given')
        except Exception as e:
            logging.error(e)

    async def make_request(self, session, url):
        """
        Make request to url with aiohttp session
        :param session: Aiohttp session
        :param url: Desired url
        :return:
        """
        try:
            async with session.get(url) as response:
                # Some logic with response
                return response
        except Exception as e:
            logging.error(e)


r = Request()
asyncio.run(r.take_input())