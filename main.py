import aiohttp
import asyncio
import multiprocessing

# Target URLs
URL = "http://localhost:8000/image.jpg"

# Number of requests per process
NUM_PROCESSES = 50
REQUESTS_PER_PROCESS = 1000

async def send_requests(session):
    """ Send multiple HTTP methods asynchronously """
    try:
        async with session.get(URL) as resp1:
            print(f"GET Status: {resp1.status}")
        async with session.put(URL, data="test") as resp2:
            print(f"PUT Status: {resp2.status}")
        async with session.delete(URL) as resp3:
            print(f"DELETE Status: {resp3.status}")
    except Exception as e:
        print(f"Request failed: {e}")

async def run_async_requests():
    """ Run async requests in batches """
    async with aiohttp.ClientSession() as session:
        tasks = [send_requests(session) for _ in range(REQUESTS_PER_PROCESS)]
        await asyncio.gather(*tasks)

def process_requests():
    """ Function to run in parallel processes """
    asyncio.run(run_async_requests())

if __name__ == "__main__":
    processes = []
    for _ in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=process_requests)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
