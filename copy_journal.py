import argparse
from systemd_journal import journal_open


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    fin = journal_open(args.input, 'r')
    fout = journal_open(args.output, 'x+')
    for e in fin:
        print(fout.append_entry(e), e.items)
    fout.close()


if __name__ == '__main__':
    main()
