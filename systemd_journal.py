from ctypes import byref
from journal_file import journal_file_open, POINTER, JournalFile, String


def main():
    from os import O_RDWR, O_CREAT

    ret = POINTER(JournalFile)()
    assert not journal_file_open(-1, String("test.journal"), O_RDWR|O_CREAT, 0o666, True, True, None, None, None, None, byref(ret))
    print(ret)


if __name__ == '__main__':
    main()
