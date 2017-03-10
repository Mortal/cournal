from ctypes import byref
from journal_file import journal_file_open, POINTER, JournalFile


def main():
    from os import O_RDWR, O_CREAT

    ret = POINTER(JournalFile)()
    systemd_shared = ctypes.cdll.LoadLibrary('/usr/lib/systemd/libsystemd-shared-232.so')
    assert not journal_file_open("test.journal", O_RDWR|O_CREAT, 0o666, True, True, None, None, None, byref(ret))
    print(ret)


if __name__ == '__main__':
    main()
