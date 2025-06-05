import requests


def get_pull_requests(github_owner, repo, github_token, api_base):
    """Return a list of open pull requests for the given repository."""
    url = f"{api_base}/repos/{github_owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    print(f"Failed to fetch pull requests: {response.status_code} - {response.text}")
    return []


def get_pr_diff(github_owner, repo, pull_number, github_token, api_base):
    """Return the list of changed files for a pull request."""
    url = f"{api_base}/repos/{github_owner}/{repo}/pulls/{pull_number}/files"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    print(
        f"Failed to fetch PR diff for #{pull_number}: {response.status_code} - {response.text}"
    )
    return []
