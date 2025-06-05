import json
from utils.github_api import get_pull_requests, get_pr_diff


def load_config():
    with open("config.json") as f:
        config = json.load(f)
        print("loading", config)
        return config


def main():
    config = load_config()
    repo_owner = config["GITHUB_OWNER"]
    repo_name = config["REPO"]
    github_token = config["GITHUB_TOKEN"]
    api_base = config["URL"]

    prs = get_pull_requests(repo_owner, repo_name, github_token, api_base)

    if not prs:
        print("No open pull requests found.")
        return

    print(f"Found {len(prs)} pull request(s):\n")
    for pr in prs:
        print(f"#{pr['number']}: {pr['title']} by {pr['user']['login']}")
        diff = get_pr_diff(repo_owner, repo_name, pr["number"], github_token, api_base)
        for file in diff:
            print(f"\nFile: {file['filename']}")
            print("🔧 Changes:")
            print(file.get('patch', '[binary or too large to display]'))


if __name__ == "__main__":
    main()
