import argparse
import json

from fake_data_lake_api import FakeDataLakeApi

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="file to upload")
parser.add_argument("metadata", type=str, help="json file containing metadata")
args = parser.parse_args()

metadata = json.load(open(args.metadata, 'r'))
bs = open(args.file, 'rb').read()

print(f"uploading {len(bs)} bytes with data {metadata}")

fdla = FakeDataLakeApi('http://127.0.0.1:5000')
id = fdla.create(metadata, bs)
print(f'created {id}')
