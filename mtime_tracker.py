from app.parse_cl_args import get_args, process_date_args
import sys


def main():
    args = get_args(sys.argv[1:])
    date_range = process_date_args(args)
    print(date_range.title)
    print(list(date_range.daterange))


if __name__ == '__main__':
    main()
