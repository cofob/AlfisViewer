from peewee import *
from time import time
from os import environ


DB_FILE = environ.get("ALFIS_DB", "blockchain.db")
db = SqliteDatabase(DB_FILE)


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
    return Blocks.select().count()


def get_domain_count():
    global DOMAIN_COUNT
    t = time()
    if DOMAIN_COUNT[1] + 30 < t:
        DOMAIN_COUNT = [len(list(set([i.identity for i in Domains.select()]))), t]
    return DOMAIN_COUNT[0]


def get_latest_block():
    return Blocks.select().order_by(-Blocks.id)[0]
