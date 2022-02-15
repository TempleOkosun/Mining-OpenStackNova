# Required imports
import json
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from github import Github  # PyGitHub library to use GitHub API v3


# This function will help extract all commits sha's & returns a tuple (access_token, repo_name : str, commits_shas: []
def extract_commits(access_token: str, repo_name: str, no_of_months: int) -> tuple:
    # Authentication and connection to GitHub API
    client = Github(access_token, per_page=100)

    # Retrieve data from n: no_of_months months ago i.e. subtract n months from current date
    period = no_of_months
    current_date = datetime.today()
    past_date = current_date - relativedelta(months=period)

    # GitHub Api responses are paginated & we already set to 100 items per page
    paginated_commits = client.get_repo(repo_name).get_commits(since=past_date, until=current_date)

    # PyGithub generally provides a lazy iterator, so we need to exhaust the lazy iterator with a list comprehension.
    commits = [commit.sha for commit in paginated_commits]

    print("The provided access token is: {token}".format(token=access_token))
    print("The target repo is: {repo}".format(repo=repo_name))
    print("The total no of commits in this repo is: {commit_count}".format(commit_count=paginated_commits.totalCount))
    print("Commits for: {duration} months will be collected".format(duration=no_of_months))
    print("Successfully collected all required commits shas")
    print("The total no of commits collected is: {commit_count}".format(commit_count=len(commits)))

    return access_token, repo_name, commits


# This function will use request library to get content of each commit.
# PyGitHub provides a friendly interface to the GitHub API but abstracts away most file attributes for each commit.
# Using request we can have access to all data attributes on files per commit which are important for the analysis.
def commit_content(access_token: str, username: str, commit_sha: str, repo_name: str):
    print("status: retrieving commit: sha - {sha}".format(sha=commit_sha))
    # Prepare Requests data
    head = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),  # Provide GitHub authorization token due to rate limits
        'User-Agent': username  # The GitHub API recommends using GitHub username as user-agent
    }
    url = 'https://api.github.com/repos/{repo_name}/commits/{sha}'.format(repo_name=repo_name, sha=commit_sha)
    response = requests.get(url, headers=head)
    commit = response.json()
    return commit


# This function receives a tuple of repo_name str and commits_shas []
# Loops through each sha in commits_shas [] and retrieves the full commit
# Extracts the required data points from each commit to form a row of data.
def prepare_data(target_commits: tuple, username) -> list:
    access_token, repo_name, shas = target_commits  # unpack token, repo, shas

    commits = []
    # Get each commit object and store in the commit list
    for sha in shas:
        record = commit_content(access_token, username, sha, repo_name)
        commits.append(record)
    rows = []
    # For each commit object in commits [], extract the data attributes into row & store the objects(row) in rows.
    for commit in commits:
        print("processing record for commit: sha - {sha}".format(sha=commit["sha"]))
        row = {"commit_sha": commit["sha"], "commit_node_id": commit["node_id"], "commit_html_url": commit["html_url"],
               "commit_date": commit["commit"]["author"]["date"], "files": commit["files"]}
        rows.append(row)
    print("All record have been successfully processed")
    return rows


# This function creates a json file to store collected data.
def export_data(data: list):
    with open('data.json', 'w', encoding="utf8") as outfile:
        json.dump(data, outfile, indent=0, separators=(',', ':'))
    print("Done writing JSON data into data.json file")
