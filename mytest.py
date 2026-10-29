import asyncio
import httpx

URL = "https://dare-frames-river-modifications.trycloudflare.com"
WORKERS = 10

async def worker(client, worker_id):
    count = 0

    while True:
        count += 1

        try:
            response = await client.post(
                URL,
                headers={"Content-Type": "text/plain"},
                content=f"Hello RELAYSCOPE! Worker={worker_id} Request={count}",
            )

            print(
                f"Worker {worker_id} | Request {count} | "
                f"Status {response.status_code}"
            )

        except httpx.HTTPError as e:
            print(f"Worker {worker_id} | Error: {e}")
            await asyncio.sleep(1)

async def main():
    limits = httpx.Limits(
        max_connections=WORKERS,
        max_keepalive_connections=WORKERS,
    )

    async with httpx.AsyncClient(
        limits=limits,
        timeout=10,
    ) as client:
        await asyncio.gather(
            *(worker(client, i) for i in range(1, WORKERS + 1))
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")