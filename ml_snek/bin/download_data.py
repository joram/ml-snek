#!/usr/bin/env python3
import json
import boto3
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURR_DIR, "../../data/")


def _existing_files():
    files = []
    for r, d, f in os.walk(DATA_DIR):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
    return files


def main():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    existing_files = _existing_files()
    bucket = boto3.resource('s3').Bucket("jsnek")
    i = 0
    for obj in bucket.objects.all():
        i += 1
        filename = obj.key
        filepath = os.path.join(DATA_DIR, f"{filename}")
        if filepath in existing_files:
            continue
        if filepath[-1] == "/":
            continue
        print(filename)

        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(filepath, "w") as f:
            content = obj.get()['Body'].read()
            data = json.loads(content)
            pretty = json.dumps(data, indent=4, sort_keys=True)
            f.write(pretty)
    print(f"have {i} games")


if __name__ == '__main__':
    main()
