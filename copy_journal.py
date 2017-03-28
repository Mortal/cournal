import argparse
from systemd_journal import journal_open


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--remove-unit')
    parser.add_argument('--remove-boot')
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    fin = journal_open(args.input, 'r')
    fout = journal_open(args.output, 'x+')
    remove_items = []
    if args.remove_unit:
        remove_items.append('_SYSTEMD_UNIT=%s' % args.remove_unit)
    if args.remove_boot:
        remove_items.append('_BOOT_ID=%s' % args.remove_boot)
    remove_items = [i.encode() for i in remove_items]
    skipped = written = 0
    for e in fin:
        if any(i in e.raw_items for i in remove_items):
            skipped += 1
            continue
        written += 1
        fout.append_entry(e)
    fout.close()
    print("Wrote %s entries and skipped %s entries" % (written, skipped))


if __name__ == '__main__':
    main()
