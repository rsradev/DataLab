import asyncio

async def main():
    print('hello')
    #task = asyncio.create_task(foo('text'))
    asyncio.create_task(foo('text'))
    #await task
    await asyncio.sleep(0.5)
    print('finished')

async def foo(text):
    print(text)
    await asyncio.sleep(10)

asyncio.run(main())


