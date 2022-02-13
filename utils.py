import os
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from github import Github

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


def commit_contents(commits_shas: list, repo_name: str):
    print(commits_shas)

    commits = []

    for commit_sha in commits_shas:
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
        commits.append(commit)

    return commits


def prepare_data(commits):
    row = {}

    for commit in commits:
        for file in commit["files"]:
            # Adding data attributes one at a time
            row["commit_sha"] = commit["sha"]
            row["commit_node_id"] = commit["node_id"]
            # row["commit_author"] = commit["author"]["login"]
            # row["committer"] = commit["committer"]["login"]
            row["commit_html_url"] = commit["html_url"]
            row["commit_date"] = commit["commit"]["author"]["date"]
            row["filepath"] = file["filename"]
            row["filename"] = os.path.basename(row["filepath"])
            row["filetype"] = os.path.splitext(row["filename"])[1]
            row["directory"] = os.path.dirname(row["filepath"])

            row["file_sha"] = file["sha"]
            row["file_status"] = file["status"]
            row["additions"] = file["additions"]
            row["deletions"] = file["deletions"]
            row["changes"] = file["changes"]
            row["file_blob"] = file["blob_url"]

            yield row


# prepare_data(commit_contents(extract_commits("octocat/hello-world", 133), "octocat/hello-world"))
# prepare_data(commit_contents(extract_commits("openstack/nova", 6), "openstack/nova"))
# print(prepare_data(commit_contents(extract_commits("TempleOkosun/EVChargerReg", 12), "TempleOkosun/EVChargerReg")))
