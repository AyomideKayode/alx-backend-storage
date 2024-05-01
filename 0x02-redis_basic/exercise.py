#!/usr/bin/env python3

""" Module that contains the Cache class.
This module demonstrates how to use Redis as a cache.
"""

import redis  # Import the Redis library for interacting with Redis
# Import the uuid module for generating random keys
import uuid
# Import Union from typing module for type annotations
from typing import Union


class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        This method creates an instance of the Redis client
        and flushes the Redis database.
        """
        self._redis = redis.Redis(
            host='localhost', port=6379, db=0)  # Initialize Redis client
        self._redis.flushdb()  # Flush the Redis database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in Redis.
        Returns:
            str: The randomly generated key under which
            the data is stored in Redis.
        """
        key = str(uuid.uuid4())  # Generate a random key using uuid
        # Store the data in Redis with the generated key
        self._redis.set(key, data)
        return key  # Return the generated key
