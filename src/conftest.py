import logging
import pytest
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session", autouse=False)
def mongodb_container():
    container = MongoDbContainer("mongo:latest")
    container.start()
    connection_url = container.get_connection_url()
    logging.info(f"MongoDB container started at {connection_url}")
    yield container
    container.stop()
    logging.info("MongoDB container stopped")
