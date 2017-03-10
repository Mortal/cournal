from os import O_RDWR, O_CREAT, O_RDONLY
import time
import errno
import collections
import ctypes
from ctypes import byref, c_ulonglong, c_void_p, cast
import journal_file as jf
from journal_file import (
    DIRECTION_UP, DIRECTION_DOWN,
)


(OBJECT_UNUSED,
 OBJECT_DATA,
 OBJECT_FIELD,
 OBJECT_ENTRY,
 OBJECT_DATA_HASH_TABLE,
 OBJECT_FIELD_HASH_TABLE,
 OBJECT_ENTRY_ARRAY,
 OBJECT_TAG) = range(8)


def get_timestamp():
    realtime = int(1e6 * time.time()) % (2**64)
    monotonic = int(1e6 * time.monotonic()) % (2**64)
    return jf.dual_timestamp(realtime, monotonic)


def make_iovec(s):
    assert isinstance(s, jf.String)
    res = jf.struct_iovec()
    res.iov_base = cast(s.raw, c_void_p)
    res.iov_len = ctypes.c_size_t(len(s))
    return res


class Entry:
    def __init__(self, entry_object: jf.EntryObject, items):
        self.entry_object = entry_object
        self._items = items

    header = property(lambda self: self.entry_object.object)
    seqnum = property(lambda self: self.entry_object.seqnum)
    realtime = property(lambda self: self.entry_object.realtime)
    monotonic = property(lambda self: self.entry_object.monotonic)
    # boot_id = property(lambda self: self.entry_object.boot_id)
    xor_hash = property(lambda self: self.entry_object.xor_hash)
    items = property(lambda self: [i.decode() for i in self._items])


class JournalHandle:
    def __init__(self, fp):
        self._fp = fp
        self._entry_position = c_ulonglong(0)

    def append(self, s, timestamp=None):
        if timestamp is None:
            timestamp = get_timestamp()
        s = jf.String(s)
        iovec = make_iovec(s)
        r = jf.journal_file_append_entry(
            self._fp, byref(timestamp), byref(iovec), 1, None, None,
            byref(self._entry_position))
        if r != 0:
            raise OSError('journal_file_append_entry returned %r' % r)

    def dump(self):
        jf.journal_file_dump(self._fp)

    def seek(self, to):
        if to != 0:
            raise ValueError('invalid position')
        self._entry_position = c_ulonglong(to)

    def read_object(self, offset, type=OBJECT_UNUSED):
        o = jf.POINTER(jf.Object)()
        r = jf.journal_file_move_to_object(self._fp, type, offset, byref(o))
        if r != 0:
            raise OSError('journal_file_move_to_object returned %r' % r)
        assert o.contents.object.type == type
        return o

    def read_data(self, offset):
        return self.read_object(offset, OBJECT_DATA).contents.data

    def read_field(self, offset):
        return self.read_object(offset, OBJECT_FIELD).contents.field

    def read_entry(self, offset):
        return self.read_object(offset, OBJECT_ENTRY).contents.entry

    def _next_entry(self, dir):
        o = jf.POINTER(jf.Object)()
        r = jf.journal_file_next_entry(self._fp, self._entry_position, dir,
                                       byref(o), byref(self._entry_position))
        if r == 0:
            return
        if r != 1:
            raise OSError('journal_file_next_entry returned %r' % r)
        return self._parse_entry(o)

    def _parse_entry(self, obj_ptr: jf.POINTER(jf.Object)):
        n = jf.journal_file_entry_n_items(obj_ptr)
        entry = obj_ptr.contents.entry
        items_ptr = ctypes.cast(entry.items, jf.POINTER(jf.EntryItem))
        items = []
        for i in range(n):
            entry_item = items_ptr[i]
            o = entry_item.object_offset
            data_obj = self.read_data(o)
            lp_char = ctypes.POINTER(ctypes.c_char)
            payload_ptr = cast(data_obj.payload, lp_char)
            dist = (cast(payload_ptr, ctypes.c_void_p).value -
                    cast(byref(data_obj), ctypes.c_void_p).value)
            payload_size = data_obj.object.size - dist
            payload = payload_ptr[0:payload_size]
            items.append(payload)
        return Entry(entry, items)

    def next_entry(self):
        return self._next_entry(DIRECTION_DOWN)

    def prev_entry(self):
        return self._next_entry(DIRECTION_UP)


def open_flags_to_sysflags(flags):
    return {'x+': O_RDWR | O_CREAT,
            'r': O_RDONLY,
            'r+': O_RDWR}[flags]


def journal_open(name, flags='r', umask=0o666):
    f = jf.POINTER(jf.JournalFile)()
    sysflags = open_flags_to_sysflags(flags)
    r = jf.journal_file_open(-1, jf.String(name), sysflags, umask, True, True,
                             None, None, None, None, byref(f))
    if r != 0:
        raise OSError('journal_file_open returned %r' % r)
    return JournalHandle(f)


def main():
    ts: jf.dual_timestamp
    f = jf.POINTER(jf.JournalFile)()
    test = 'TEST1=1'
    test2 = 'TEST2=2'
    o = jf.POINTER(jf.Object)()

    journal = journal_open('test.journal', 'x+')
    f = journal._fp
    journal.append(test)
    journal.append(test2)
    journal.append(test)
    # if HAVE_GCRYPT: journal_file_append_tag(f)
    journal.dump()
    journal.seek(0)

    entry = journal.next_entry()
    assert entry.seqnum == 1
    assert entry.items == [test]

    assert journal.next_entry().seqnum == 2

    assert journal.next_entry().seqnum == 3

    assert journal.next_entry() is None

    journal.seek(0)
    assert journal.next_entry().seqnum == 1

    # Output pointer and/or offset to data object
    data_ptr = jf.POINTER(jf.Object)()
    data_pos = c_ulonglong()
    assert 1 == jf.journal_file_find_data_object(f, jf.String(test), len(test), byref(data_ptr), byref(data_pos))
    assert data_ptr.contents.object.type == OBJECT_DATA
    assert data_ptr.contents.data.n_entries == 2
    # Which entry objects contain this data object? Optionally input pointer and offset
    o_pos = c_ulonglong()
    assert 1 == jf.journal_file_next_entry_for_data(f, None, 0, data_pos, DIRECTION_DOWN, byref(o), byref(o_pos))
    assert o.contents.object.type == OBJECT_ENTRY
    assert 1 == o.contents.entry.seqnum
    # Is journal_file_next_entry_for_data broken? How to use it properly?
    # r = jf.journal_file_next_entry_for_data(f, o, o_pos, data_pos, DIRECTION_DOWN, byref(o), byref(o_pos))
    # assert 1 == r, errno.errorcode.get(-r, r)
    # assert 3 == o.contents.entry.seqnum
    # assert 0 == jf.journal_file_next_entry_for_data(f, o, o_pos, data_pos, DIRECTION_DOWN, byref(o), byref(o_pos))

    assert 1 == jf.journal_file_next_entry_for_data(f, None, 0, data_pos, DIRECTION_UP, byref(o), None)
    assert 3 == o.contents.entry.seqnum

    assert 1 == jf.journal_file_find_data_object(f, jf.String(test2), len(test2), None, byref(data_pos))
    assert 1 == jf.journal_file_next_entry_for_data(f, None, 0, data_pos, DIRECTION_UP, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert 1 == jf.journal_file_next_entry_for_data(f, None, 0, data_pos, DIRECTION_DOWN, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert not jf.journal_file_find_data_object(f, jf.String("quux"), 4, None, byref(data_pos))

    assert 1 == jf.journal_file_move_to_entry_by_seqnum(f, 1, DIRECTION_DOWN, byref(o), None)
    assert 1 == o.contents.entry.seqnum

    assert 1 == jf.journal_file_move_to_entry_by_seqnum(f, 3, DIRECTION_DOWN, byref(o), None)
    assert 3 == o.contents.entry.seqnum

    assert 1 == jf.journal_file_move_to_entry_by_seqnum(f, 2, DIRECTION_DOWN, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert not jf.journal_file_move_to_entry_by_seqnum(f, 10, DIRECTION_DOWN, byref(o), None)

    jf.journal_file_rotate(byref(f), True, True, None)
    jf.journal_file_rotate(byref(f), True, True, None)

    jf.journal_file_close(f)


if __name__ == '__main__':
    main()
