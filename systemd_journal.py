import time
from ctypes import byref, c_ulonglong, c_void_p, cast
import journal_file
from journal_file import (
    POINTER, String,
    JournalFile, dual_timestamp, Object, struct_iovec,
    DIRECTION_DOWN,
    journal_file_open, journal_file_append_entry, journal_file_dump,
    journal_file_next_entry,
)


def get_dual_timestamp():
    t = int(1e6 * time.time()) % (2**64)
    return dual_timestamp(t, t)


def make_iovec(s):
    s = String(s)
    return struct_iovec(cast(s.data, c_void_p), len(s))


def main():
    from os import O_RDWR, O_CREAT

    f = POINTER(JournalFile)()
    assert not journal_file_open(-1, String("test.journal"), O_RDWR|O_CREAT, 0o666, True, True, None, None, None, None, byref(f))
    ts = get_dual_timestamp()
    iovec = make_iovec('TEST1=1')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)
    iovec = make_iovec('TEST2=2')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)
    iovec = make_iovec('TEST1=1')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)
    journal_file_dump(f)

    o = POINTER(Object)()
    p = c_ulonglong()
    assert 1 == journal_file_next_entry(f, 0, DIRECTION_DOWN, byref(o), byref(p))
    entry = o.contents.entry  # type: journal_file.struct_EntryObject
    print([(k, getattr(entry, k)) for k in entry.__slots__])
    assert o.contents.entry.seqnum == 1, o.contents.entry.seqnum
    assert 1 == journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 2
    assert 1 == journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 3
    assert not journal_file_next_entry(f, p, DIRECTION_DOWN, byref(o), byref(p))
    assert 1 == journal_file_next_entry(f, 0, DIRECTION_DOWN, byref(o), byref(p))
    assert o.contents.entry.seqnum == 1


if __name__ == '__main__':
    main()
