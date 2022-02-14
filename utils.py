# Required imports
import json
import os
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv  # manage environment variables
from github import Github  # PyGitHub library to use GitHub API v3

load_dotenv()

# XXX: Specify your own access token here
token = os.environ.get("ACCESS_TOKEN")
username = os.environ.get("GITHUB_USERNAME")


def extract_commits(repo_name: str, no_of_months: int) -> list:
    # Authentication and connection to GitHub API
    client = Github(token, per_page=100)

    # Retrieve data from 6 months ago i.e. subtract 6 months from current date
    period = no_of_months
    current_date = datetime.today()
    past_date = current_date - relativedelta(months=period)

    paginated_commits = client.get_repo(repo_name).get_commits(since=past_date, until=current_date)

    # PyGithub generally provides a lazy iterator we need to exhaust the lazy iterator with a list comprehension
    commits = [commit.sha for commit in paginated_commits]

    return commits


def commit_content(commit_sha: str, repo_name: str):
    # Requests data
    # head = {'Authorization': 'token {}'.format(token)}
    head = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token),  # Provide authorization token
        'User-Agent': username  # The API recommends using GitHub username as user-agent
    }
    url = 'https://api.github.com/repos/{repo_name}/commits/{sha}'.format(repo_name=repo_name, sha=commit_sha)
    response = requests.get(url, headers=head)
    commit = response.json()

    return commit


def prepare_data(shas):
    commits = []
    for sha in shas:
        record = commit_content(sha, "TempleOkosun/EVChargerReg")
        commits.append(record)
    rows = []
    for commit in commits:
        row = {"commit_sha": commit["sha"], "commit_node_id": commit["node_id"], "commit_html_url": commit["html_url"],
               "commit_date": commit["commit"]["author"]["date"], "files": commit["files"]}
        rows.append(row)
        # Adding data attributes one at a time
        # row["commit_author"] = commit["author"]["login"]
        # row["committer"] = commit["committer"]["login"]
        # row["filepath"] = file["filename"]
        # row["filename"] = os.path.basename(row["filepath"])
        # row["filetype"] = os.path.splitext(row["filename"])[1]
        # row["directory"] = os.path.dirname(row["filepath"])
        #
        # row["file_sha"] = file["sha"]
        # row["file_status"] = file["status"]
        # row["additions"] = file["additions"]
        # row["deletions"] = file["deletions"]
        # row["changes"] = file["changes"]
        # row["file_blob"] = file["blob_url"]

    return rows


# prepare_data(commit_contents(extract_commits("octocat/hello-world", 133), "octocat/hello-world"))
# prepare_data(commit_contents(extract_commits("openstack/nova", 6), "openstack/nova"))
data = (prepare_data((extract_commits("TempleOkosun/EVChargerReg", 12))))


def export_data(data):
    with open('data.json', 'w', encoding="utf8") as outfile:
        # outfile.write(json.dumps(data))
        # outfile.write(str(data))
        json.dump(data, outfile, indent=0, separators=(',', ':'))

    print("Done writing JSON data into .json file")
