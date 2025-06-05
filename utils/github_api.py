#get the pull request from the repo
import requests

def get_pull_requests(github_owner, repo, github_token, api_base):
    url = f"{api_base}/repos/Huzzzaif/testrepo/pulls"
    headers={
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    #if requets is successfull
    if response.status_code == 200:
        return response.json()
    else:
        print("request failed")
        return []
    
def get_pr_diff(github_owner, pull_number,repo, github_token,api_base):

    prs = get_pull_requests(github_owner, repo, github_token, api_base)

    for pr in prs:
        pr_number = pr["number"]
        title = pr["title"]
        author = pr["user"]["login"]
        url = f"{api_base}/repos/Huzzzaif/testrepo/pulls/{pr_number}/files"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch PR diff: {response.status_code} - {response.text}")
            return []
    