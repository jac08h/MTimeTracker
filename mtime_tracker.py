from app.parse_cl_args import get_args, process_date_args
from app.LogsProcessor import LogsProcessor
import sys
import logging


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()]
                        )
    args = get_args(sys.argv[1:])
    date_range = process_date_args(args)
    logs_processor = LogsProcessor(date_range, args.directory)
    logs = logs_processor.get_timelogs()
    print(logs)


if __name__ == '__main__':
    main()
