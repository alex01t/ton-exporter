from pytoniq import LiteClient
import asyncio
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2, timeout=15)


@app.get("/", response_class=PlainTextResponse)
async def root(): # client = Depends(get_client)
    async with client:
        x = await client.get_masterchain_info()
        h = x['last']['seqno']
    return 'ton_masterchain_last_seqno{} ' + str(h)


async def main():
    from pprint import pprint as p
    # https://ton.org/global-config.json
    client = LiteClient.from_mainnet_config(  # choose mainnet, testnet or custom config dict
        ls_i=0,  # index of liteserver from config
        trust_level=2,  # trust level to liteserver
        timeout=15  # timeout not includes key blocks synchronization as it works in pytonlib
    )
    await client.connect()
    await client.get_masterchain_info()
    await client.reconnect()  # can reconnect to an exising object if had any errors
    await client.close()
    """ or use it with context manager: """
    async with LiteClient.from_mainnet_config(ls_i=0, trust_level=2, timeout=15) as client:
        x = await client.get_masterchain_info()
        p(type(x))
        p(x)
        h = x['last']['seqno']
        p(h)

if __name__ == '__main__':
    asyncio.run(main())

