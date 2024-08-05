import hashlib
import datetime
import json
import threading
import time
from cryptography.fernet import Fernet


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.data_hash = self.hash_data()
        self.hash = self.hash_block()

    def hash_data(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8'))
        return sha.hexdigest()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data_hash).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    @staticmethod
    def next_block(last_block, data):
        this_index = last_block.index + 1
        this_timestamp = datetime.datetime.now()
        this_hash = last_block.hash
        return Block(this_index, this_timestamp, data, this_hash)

    @staticmethod
    def create_genesis():
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")



