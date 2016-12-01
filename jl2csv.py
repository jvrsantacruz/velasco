import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    headers = set()
    with open(args.input) as stream:
        for line in stream:
            headers.update(json.loads(line).keys())

    headers = sorted(headers)
    print(','.join(h.replace(',', '') for h in headers))
    with open(args.input) as stream:
        for line in stream:
            data = json.loads(line)
            print(','.join(str(data.get(k, '')).replace(',', '')
                           for k in headers))


if __name__ == '__main__':
    main()
