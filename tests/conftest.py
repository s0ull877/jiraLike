import pytest
import asyncio

pytest_plugins = [
    "tests.fixtures.auth.services",
    "tests.fixtures.auth.repositories",
    "tests.fixtures.auth.models",
    "tests.fixtures.infrastructure",
    "src.core"
]

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()