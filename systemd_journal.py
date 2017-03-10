from os import O_RDWR, O_CREAT, O_RDONLY
import time
import collections
import ctypes
from ctypes import byref, c_ulonglong, c_void_p, cast
import journal_file
from journal_file import (
    POINTER, String,
    JournalFile, dual_timestamp, Object, struct_iovec, EntryObject,
    DIRECTION_UP, DIRECTION_DOWN,
    journal_file_open, journal_file_append_entry, journal_file_dump,
    journal_file_next_entry, journal_file_find_data_object,
    journal_file_next_entry_for_data, journal_file_move_to_entry_by_seqnum,
    journal_file_rotate, journal_file_close,
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
    return dual_timestamp(realtime, monotonic)


def make_iovec(s):
    s = String(s)
    return struct_iovec(cast(s.data, c_void_p), len(s))


EntryBase = collections.namedtuple(
    'Entry', 'object seqnum realtime monotonic boot_id xor_hash items'.split())
assert EntryObject.__slots__ == EntryBase._fields


FieldBase = collections.namedtuple(
    'Field', 'object hash next_hash_offset head_data_offset payload'.split())
assert FieldObject.__slots__ == FieldBase._fields


class LazyEntryItem(LazyEntryItemBase):
    def __init__(self, journal, structure):
        self._journal = journal
        self.offset = structure.object_offset
        self.hash = structure.hash

    @classmethod
    def convert(cls, journal, structure):
        return cls(journal, structure.object_offset, structure.hash)

    def _load(self):
        self._object = self._journal.read(self.offset)

    def _get(self):
        try:
            return self._object
        except AttributeError:
            self._load()
        return self._object

    def __getattr__(self, k):
        return getattr(self._get(), k)


class Entry(EntryBase):
    @classmethod
    def convert_object_ptr(cls, journal, obj_ptr):
        n = journal_file_entry_n_items(obj_ptr)
        assert obj_ptr.contents.object.type == OBJECT_ENTRY
        obj = obj_ptr.contents.entry
        values = [getattr(obj, k) for k in cls._fields[:-1]]
        items_ptr = cast(obj_ptr.items, POINTER(EntryItem))
        items = [LazyEntryItem(journal, items_ptr[i]) for i in range(n)]
        values.append(items)
        return cls(*values)


class Field(FieldBase):
    @classmethod
    def convert_object_ptr(cls, journal, obj_ptr):
        n = journal_file_entry_n_items(obj_ptr)
        assert obj_ptr.contents.object.type == OBJECT_ENTRY
        obj = obj_ptr.contents.entry
        values = [getattr(obj, k) for k in cls._fields[:-1]]
        items_ptr = cast(obj_ptr.items, POINTER(EntryItem))
        items = [LazyEntryItem(journal, items_ptr[i]) for i in range(n)]
        values.append(items)
        return cls(*values)


class Object:
    @classmethod
    def convert_object_ptr(cls, journal, obj_ptr):
        header = obj_ptr.contents.object
        object_type = header.type
        if object_type == OBJECT_ENTRY:
            return Entry.convert_object_ptr(journal, obj_ptr)
        elif object_type == OBJECT_FIELD:
            return Field.convert_object_ptr(journal, obj_ptr)
        elif object_type == OBJECT_DATA:
            return Data.convert_object_ptr(journal, obj_ptr)
        raise TypeError(object_type)


class JournalHandle:
    def __init__(self, fp):
        self._fp = fp
        self._entry_position = c_ulonglong(0)

    def append(self, s, timestamp=None):
        if timestamp is None:
            timestamp = get_timestamp()
        iovec = make_iovec(s)
        r = journal_file_append_entry(
            self._fp, byref(timestamp), byref(iovec), 1, None, None,
            byref(self._entry_position))
        if r != 0:
            raise OSError('journal_file_append_entry returned %r' % r)

    def dump(self):
        journal_file_dump(self._fp)

    def seek(self, to):
        if to != 0:
            raise ValueError('invalid position')
        self._entry_position = c_ulonglong(to)

    def read_object(self, offset, type=OBJECT_UNUSED):
        o = POINTER(journal_file.Object)()
        r = journal_file_move_to_object(self._fp, type, offset, byref(o))
        if r != 0:
            raise OSError('journal_file_move_to_object returned %r' % r)
        assert o.object.type == type
        return o

    def read_data(self, offset):
        return self.read_object(offset, OBJECT_DATA).data

    def read_field(self, offset):
        return self.read_object(offset, OBJECT_FIELD).field

    def read_entry(self, offset):
        return self.read_object(offset, OBJECT_ENTRY).entry

    def _next_entry(self, dir):
        o = POINTER(journal_file.Object)()
        r = journal_file_next_entry(self._fp, self._entry_position, dir,
                                    byref(o), byref(self._entry_position))
        if r != 0:
            raise OSError('journal_file_next_entry returned %r' % r)
        n = journal_file_entry_n_items(o)
        entry = o.contents.entry
        items_ptr = cast(entry.items, POINTER(EntryItem))
        for i in range(n):
            entry_item = items_ptr[i]
            data_obj = self.read_data(entry_item.offset)
            payload_ptr = cast(byref(data_obj.payload), ctypes.c_char_p)
            dist = payload_ptr - cast(byref(data_obj), ctypes.c_char_p)
            payload_size = data_obj.object.size - dist
            payload = payload_ptr[0:payload_size].decode()
        return Entry.convert_object_ptr(o)

    def next_entry(self):
        return self._next_entry(DIRECTION_DOWN)

    def prev_entry(self):
        return self._next_entry(DIRECTION_UP)


def open_flags_to_sysflags(flags):
    return {'x+': O_RDWR | O_CREAT,
            'r': O_RDONLY,
            'r+': O_RDWR}[flags]


def journal_open(name, flags='r', umask=0o666):
    f = POINTER(JournalFile)()
    sysflags = open_flags_to_sysflags(flags)
    r = journal_file_open(-1, String(name), sysflags, umask, True, True, None,
                          None, None, None, byref(f))
    if r != 0:
        raise OSError('journal_file_open returned %r' % r)
    return JournalHandle(f)


def main():
    ts: dual_timestamp
    f = POINTER(JournalFile)()
    test = 'TEST1=1'
    test2 = 'TEST2=2'
    o = POINTER(journal_file.Object)()
    p = c_ulonglong()

    journal = journal_open('test.journal', 'x+')
    journal.append(test)
    journal.append(test2)
    journal.append(test)
    # if HAVE_GCRYPT: journal_file_append_tag(f)
    journal.dump()
    journal.seek(0)

    assert 1 == journal_file_next_entry(f, 0, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 1, o.contents.entry.seqnum

    assert 1 == journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 2

    assert 1 == journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 3

    assert not journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))

    assert 1 == journal_file_next_entry(f, 0, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 1

    assert 1 == journal_file_find_data_object(f, String(test), len(test), None, byref(p))
    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_DOWN, byref(o), None)
    assert 1 == o.contents.entry.seqnum

    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_UP, byref(o), None)
    assert 3 == o.contents.entry.seqnum

    assert 1 == journal_file_find_data_object(f, String(test2), len(test2), None, byref(p))
    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_UP, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_DOWN, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert not journal_file_find_data_object(f, String("quux"), 4, None, byref(p))

    assert 1 == journal_file_move_to_entry_by_seqnum(f, 1, DIRECTION_DOWN, byref(o), None)
    assert 1 == o.contents.entry.seqnum

    assert 1 == journal_file_move_to_entry_by_seqnum(f, 3, DIRECTION_DOWN, byref(o), None)
    assert 3 == o.contents.entry.seqnum

    assert 1 == journal_file_move_to_entry_by_seqnum(f, 2, DIRECTION_DOWN, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert not journal_file_move_to_entry_by_seqnum(f, 10, DIRECTION_DOWN, byref(o), None)

    journal_file_rotate(byref(f), True, True, None)
    journal_file_rotate(byref(f), True, True, None)

    journal_file_close(f)


if __name__ == '__main__':
    main()
