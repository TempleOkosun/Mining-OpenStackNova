import requests
from utils import extract_commits, commit_contents, commit_contents, prepare_data

data_row = (
    prepare_data(commit_contents(extract_commits("TempleOkosun/EVChargerReg", 12), "TempleOkosun/EVChargerReg")))


if __name__ == '__main__':
    for record in data_row:
        print(record)

