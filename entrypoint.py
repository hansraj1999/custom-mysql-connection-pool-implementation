import uvicorn
import os
import asyncio


async def main():

    uvicorn.run(
        "app:start_server", port=8000, host="0.0.0.0", reload=True, factory=True
    )


if __name__ == "__main__":

    asyncio.run(main())
