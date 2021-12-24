from peewee import *
from time import time


db = SqliteDatabase("blockchain.db")


BLOCK_COUNT = [0, 0]
LATEST_BLOCK = [0, 0]
DOMAIN_COUNT = [0, 0]


class Base(Model):
    class Meta:
        database = db


class Blocks(Base):
    id: int = IntegerField(primary_key=True)
    timestamp: int = IntegerField()
    version: int = IntegerField()
    difficulty: int = IntegerField()
    random: int = IntegerField()
    nonce: int = IntegerField()
    transaction: str = TextField(null=True)
    prev_block_hash: bytes = BlobField(null=True)
    hash: bytes = BlobField()
    pub_key: bytes = BlobField()
    signature: bytes = BlobField()


class Domains(Base):
    id: int = IntegerField(primary_key=True)
    timestamp: int = IntegerField()
    identity: bytes = BlobField()
    confirmation: bytes = BlobField()
    data: str = TextField()
    signing: bytes = BlobField()
    encryption: bytes = BlobField()


class Options(Base):
    pass


db.connect()
db.create_tables([Blocks, Domains, Options])


def get_block_count():
    global BLOCK_COUNT
    t = time()
    if BLOCK_COUNT[1] + 30 < t:
        BLOCK_COUNT = [Blocks.select().count() + 1, t]
    return BLOCK_COUNT[0]


def get_domain_count():
    global DOMAIN_COUNT
    t = time()
    if DOMAIN_COUNT[1] + 30 < t:
        DOMAIN_COUNT = [len(list(set([i.identity for i in Domains.select()]))), t]
    return DOMAIN_COUNT[0]


def get_latest_block():
    global LATEST_BLOCK
    t = time()
    if LATEST_BLOCK[1] + 30 < t:
        LATEST_BLOCK = [Blocks.select().order_by(-Blocks.id)[0], t]
    return LATEST_BLOCK[0]
