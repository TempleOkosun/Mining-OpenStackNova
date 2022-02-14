import json

from utils import extract_commits, commit_contents, prepare_data

data_row = (
    prepare_data(commit_contents(extract_commits("TempleOkosun/EVChargerReg", 12), "TempleOkosun/EVChargerReg")))

if __name__ == '__main__':
    with open('data10.json', 'w') as outfile:
        for record in data_row:
            outfile.write(str(record))

    print("Done writing JSON data into .json file")






    # with open('data8.json', 'w') as outfile:
    #     for record in data_row:
    #         json.dump(record, outfile, indent=-1)
    #     print("Done writing JSON data into .json file")


    # with open('data.json', 'w') as outputfile:
    #     outputfile.write("[")
    #     for record in data_row:
    #         outputfile.write(str(record) + "," + "\n")
    #     outputfile.write("]")

    # json.dump(record, outputfile, indent=" ")
