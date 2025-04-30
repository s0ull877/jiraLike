import pytest
import asyncio

pytest_plugins = [
    "tests.fixtures.auth.services",
    "tests.fixtures.auth.repositories",
    "tests.fixtures.auth.models",
    "src.core"
]

