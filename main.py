import requests


def get_commits(repo, total_no_of_commits):
    #
    all_commits = []

    n = 1
    params = {'page': n, 'per_page': 100}
    r = requests.get(repo, params=params)

    # returned paginated commits
    result = r.json()
    all_commits.extend(result)

    # while len(all_commits) < total_no_of_commits:
    #     n = n + 1
    #     more = requests.get(repo, params=params)
    #     # returned paginated commits
    #     result_more = more.json()
    #     all_commits.extend(result_more)

    for commit in all_commits:
        print(commit)
    print(len(all_commits))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_commits('https://api.github.com/repos/openstack/nova/commits', 200)
