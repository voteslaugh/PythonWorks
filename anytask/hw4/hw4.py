import re
import argparse
from collections import Counter


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_name',
                        help='file with logs for parse')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--resource',
                       action='store_const',
                       const=r', (/.+?),',
                       dest='regex',
                       help='get the most popular resource from log')
    group.add_argument('-c', '--client',
                       action='store_const',
                       const=r'^(.+?),',
                       dest='regex',
                       help='get the most active client from log')
    return parser


def get_stat(regex, log_name):
    regex = re.compile(regex)
    data = []
    with open(log_name, errors='ignore') as logs:
        for line in logs:
            res = re.search(regex, line)
            if res:
                data.append(res.group(1))
    return Counter(data).most_common()[0][0]


if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    print(get_stat(args.regex, args.log_name))