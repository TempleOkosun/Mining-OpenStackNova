import json
import pandas as pd

import requests
from utils import extract_commits, commit_contents, prepare_data

data_row = (
    prepare_data(commit_contents(extract_commits("TempleOkosun/EVChargerReg", 12), "TempleOkosun/EVChargerReg")))

if __name__ == '__main__':
    records = [record for record in data_row]
    print("at this point oprint record: " + "\n")
    print(records)
    with open('data.json', 'w') as outputfile:
        json.dump(records, outputfile)
        # for record in data_row:
        #     json.dump(record, outputfile)




    # with open('data.json', 'w') as outputfile:
    #     outputfile.write("[")
    #     for record in data_row:
    #         outputfile.write(str(record) + "," + "\n")
    #     outputfile.write("]")



            # json.dump(record, outputfile, indent=" ")


