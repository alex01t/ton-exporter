from pytoniq import LiteClient
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import asyncio
import os

def create_app():
    app = FastAPI()
    clients = {
        os.getenv('LITE_LABEL', 'local'): LiteClient(
            os.getenv('LITE_HOST'),
            int(os.getenv('LITE_PORT')),
            server_pub_key=os.getenv('LITE_PUB'),
            trust_level=2,
            timeout=5
        ),
        'global': LiteClient.from_mainnet_config(
            ls_i=0,
            trust_level=2,
            timeout=5
        ),
    }

    @app.on_event("startup")
    async def startup():
        for k in clients.keys():
            print(f'startup .. {k}')
            t = clients[k]
            while not t.inited:
                try:
                    await t.connect()
                except Exception as e:
                    print(f'failed to start: {e}')
                    await asyncio.sleep(1)
            print(f'{t}, inited = {t.inited}')

    @app.on_event("shutdown")
    async def shutdown():
        for k in clients.keys():
            print(f'shutdown .. {k}')
            t = clients[k]
            await t.close()

    @app.get("/metrics", response_class=PlainTextResponse)
    async def root():
        res = []
        for k in clients.keys():
            # print(f'metrics for {k}')
            ton = clients[k]
            try:
                x = await ton.get_masterchain_info()
                h = x['last']['seqno']
            except Exception as e:
                print(f'Oups: {e}, reconnecting ..')
                try:
                    await ton.close()
                except Exception as e:
                    print(f'cannot close(): {e}')
                try:
                    await ton.connect()
                except Exception as e:
                    print(f'cannot connect(): {e}')
                h = 'NaN'

            res.append('ton_masterchain_last_seqno{node="' + str(k) + '"} ' + str(h))

        return '\n'.join(res)

    return app

app = create_app()



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

