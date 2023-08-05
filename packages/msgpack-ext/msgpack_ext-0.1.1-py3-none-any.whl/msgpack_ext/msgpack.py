import enum
import struct
import uuid
from datetime import datetime, timezone
from functools import partial

import msgpack


class code(enum.IntEnum):
    uuid = 1
    datetime = 2


def default(obj):
    if isinstance(obj, uuid.UUID):
        return msgpack.ExtType(code.uuid, obj.bytes)
    if isinstance(obj, datetime):
        ts = struct.pack('!d', obj.timestamp())
        return msgpack.ExtType(code.datetime, ts)

    raise TypeError("Unknown type: %r" % (obj,))


def ext_hook(_code, data):
    if _code == code.uuid:
        return uuid.UUID(bytes=data)
    if _code == code.datetime:
        timestamp, = struct.unpack('!d', data)
        dt = datetime.utcfromtimestamp(timestamp)
        return dt.replace(tzinfo=timezone.utc)

    return msgpack.ExtType(_code, data)


packb = partial(msgpack.packb, use_bin_type=True, default=default)
unpackb = partial(msgpack.unpackb, encoding='utf-8', ext_hook=ext_hook)

Packer = partial(msgpack.Packer, use_bin_type=True, default=default)
Unpacker = partial(msgpack.Unpacker, encoding='utf-8', ext_hook=ext_hook)
