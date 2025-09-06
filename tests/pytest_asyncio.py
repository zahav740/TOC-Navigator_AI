import asyncio
import pytest

fixture = pytest.fixture


def pytest_pyfunc_call(pyfuncitem):  # pragma: no cover - test helper
    if asyncio.iscoroutinefunction(pyfuncitem.function):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(pyfuncitem.obj(**pyfuncitem.funcargs))
        loop.close()
        return True
    return None
