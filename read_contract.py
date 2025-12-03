import os
import asyncio
from tools.contract_read_file import get_tool
from dotenv import load_dotenv

load_dotenv()  # loads RPC_URL

print("DEBUG: cwd:", os.getcwd())
print("DEBUG: WEB3_PROVIDER_URL set?", bool(os.getenv("WEB3_PROVIDER_URL")))


async def main():
    tool = get_tool()
    run = tool["run"]

    res = await run({
        "contractAddress": "0x4F333c49B820013e5E6Fe86634DC4Da88039CE50",
        "abiFile": "./abi/SimpleStorage.json",
        "method": "name"
    })

    print(res)

asyncio.run(main())
