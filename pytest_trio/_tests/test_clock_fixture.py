import pytest
import trio

async def handle_client(stream):
    while True:
        buff = await stream.receive_some(100)
        await stream.send_all(buff)


@pytest.fixture
async def server(nursery):
    nursery.start_soon(trio.serve_tcp, handle_client)


@trio._util.acontextmanager
async def do():
    async with trio.open_nursery() as nursery:
        await trio.sleep(1)
        yield nursery
        await trio.sleep(1)
        nursery


@pytest.mark.trio
async def test_sleep_with_autojump_clock(autojump_clock, do_it):
    assert trio.current_time() == 0

    for i in range(10):
        start_time = trio.current_time()
        await trio.sleep(i)
        end_time = trio.current_time()

        assert end_time - start_time == i
