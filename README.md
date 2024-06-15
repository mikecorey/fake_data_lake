# Fake Data Lake w/ Api

This is an example of a fake data lake written in flask.  The data lake uploads binary objects and metadata.  It consists of:

- fake_data_lake.py - this emulates the data lake and stores files and metadata in memory
- app.py - this is a flask server which serves endpoints for interacting with the fake_data_lake.
- fake_data_lake_api.py - this is an api client that can be used to interact with the fake data lake flask server

There are also two test scripts, test_app.py which is for testing the flask app and test_fake_data_lake_api.py which tests the fake_data_lake_api.

## Command Line Interface
The fake data lake includes a command line for uploading files via the command line.  To use it on the included test files, run:

`python fake_data_lake_cli.py test_raw.bin meta.json`
