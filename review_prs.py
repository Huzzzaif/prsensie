import json
from utils.github_api import get_pull_requests, get_pr_diff

try:
    import openai
except ImportError:
    openai = None


def load_config():
    with open("config.json") as f:
        config = json.load(f)
        return config


def review_pull_request(config, pr):
    if openai is None:
        print("openai library is not installed")
        return

    openai.api_key = config["OPENAI_API_KEY"]
    repo_owner = config["GITHUB_OWNER"]
    repo_name = config["REPO"]
    github_token = config["GITHUB_TOKEN"]
    api_base = config["URL"]

    diff_files = get_pr_diff(repo_owner, repo_name, pr["number"], github_token, api_base)
    patches = []
    for f in diff_files:
        filename = f.get("filename")
        patch = f.get("patch", "")
        if patch:
            patches.append(f"File: {filename}\n{patch}")
    if not patches:
        print("No diff available for PR", pr["number"])
        return

    prompt = "\n\n".join(patches)
    system = "You are an automated code reviewer. Provide concise review comments." 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
    )
    review = response.choices[0].message.content.strip()
    print(f"\nReview for PR #{pr['number']} by {pr['user']['login']}:\n{review}\n")


def main():
    config = load_config()
    prs = get_pull_requests(
        config["GITHUB_OWNER"],
        config["REPO"],
        config["GITHUB_TOKEN"],
        config["URL"],
    )

    if not prs:
        print("No open pull requests found.")
        return

    for pr in prs:
        review_pull_request(config, pr)


if __name__ == "__main__":
    main()
