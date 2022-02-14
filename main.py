import os
from utils import export_data
from dotenv import load_dotenv  # to manage environment variables

load_dotenv()
# XXX: Specify your own access token here
token = os.environ.get("ACCESS_TOKEN")
username = os.environ.get("GITHUB_USERNAME")



if __name__ == '__main__':
    export_data(data)
