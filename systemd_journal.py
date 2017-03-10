from os import O_RDWR, O_CREAT
import time
from ctypes import byref, c_ulonglong, c_void_p, cast
# import journal_file
from journal_file import (
    POINTER, String,
    JournalFile, dual_timestamp, Object, struct_iovec,
    DIRECTION_UP, DIRECTION_DOWN,
    journal_file_open, journal_file_append_entry, journal_file_dump,
    journal_file_next_entry, journal_file_find_data_object,
    journal_file_next_entry_for_data, journal_file_move_to_entry_by_seqnum,
    journal_file_rotate, journal_file_close,
)


def get_dual_timestamp():
    t = int(1e6 * time.time()) % (2**64)
    return dual_timestamp(t, t)


def make_iovec(s):
    s = String(s)
    return struct_iovec(cast(s.data, c_void_p), len(s))


def main():
    ts: dual_timestamp
    f = POINTER(JournalFile)()
    test = 'TEST1=1'
    test2 = 'TEST2=2'
    o = POINTER(Object)()
    p = c_ulonglong()

    assert not journal_file_open(-1, String("test.journal"), O_RDWR | O_CREAT, 0o666, True, True, None, None, None, None, byref(f))

    ts = get_dual_timestamp()

    iovec = make_iovec('TEST1=1')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)

    iovec = make_iovec('TEST2=2')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)

    iovec = make_iovec('TEST1=1')
    assert not journal_file_append_entry(f, byref(ts), byref(iovec), 1, None, None, None)

    # if HAVE_GCRYPT: journal_file_append_tag(f)
    journal_file_dump(f)

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

    assert 1 == journal_file_find_data_object(f, test2, len(test2), None, byref(p))
    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_UP, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert 1 == journal_file_next_entry_for_data(f, None, 0, p, DIRECTION_DOWN, byref(o), None)
    assert 2 == o.contents.entry.seqnum

    assert not journal_file_find_data_object(f, "quux", 4, None, byref(p))

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
