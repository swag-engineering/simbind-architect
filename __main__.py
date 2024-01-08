import os
import argparse
import logging


from app.architect.Collector import Collector

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--zip_path',
        dest='zip_path',
        help='path to zip archive',
        required=True
    )
    parser.add_argument(
        '--out_path',
        dest='out_path',
        help='path to output folder',
        required=True
    )
    parser.add_argument(
        '--overwrite',
        dest='overwrite',
        help='flag to overwrite outpu folder if it is not empty',
        action='store_true'
    )
    parser.add_argument(
        '--no_tests',
        dest='no_tests',
        help='disables integrity tests of resulting packages',
        action='store_true'
    )
    parser.add_argument(
        '--tmp_dir',
        dest='tmp_dir',
        help='Output to temporary folder. Should be used for debug only'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v',
        dest='verbosity',
        default=1,
        help='Specifies the level of verbosity. Example: -vvv',
        action='count'
    )
    group.add_argument(
        '--quiet',
        '-q',
        dest='no_logs',
        help='Do not print logs to stdout',
        action='store_true'
    )

    args = parser.parse_args()

    verbosity2lvl = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    args.verbosity = 3 if args.verbosity > 3 else args.verbosity
    logger = logging.getLogger()
    logger.setLevel(level=verbosity2lvl[args.verbosity])
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(levelname)-8s :: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    architect = Collector(args.zip_path,
                          tmp_dir=None if args.tmp_dir == None else os.path.abspath(args.tmp_dir))
    architect.compose_packages(args.out_path, True)
