import os

from dotenv import load_dotenv  # to manage environment variables

from utils import prepare_data, extract_commits, export_data

load_dotenv()
# XXX: Specify your own access token here
token = os.environ.get("ACCESS_TOKEN")
username = os.environ.get("GITHUB_USERNAME")

# Test & dev repo details
# repo = 'TempleOkosun/EVChargerReg'
# time_period = 13

# Project Repo details
repo = 'openstack/nova'
time_period = 6

# 1. Extract all commits shas
target_commits = extract_commits(token, repo, time_period)

# 2. Pull together the data. Get each commit and retrieve the desired contents for analysis.
# We pass in username as the prepare_data utilizes the commit_content function which uses requests to get each commit
# The GitHub API recommends requests have username as the user-agent.
data = prepare_data(target_commits, username)

if __name__ == '__main__':
    # 3. Store collected as json file for further use
    export_data(data)
