import json
import os

import github

from src.add_reviewers import add_reviewers
from src.block_offensive_lanague import block_offensive_lanague
from src.labels_by_user_input import labels_by_user_input, remove_verified_label
from src.size_label_prs import size_label_prs


if __name__ == "__main__":
    token = os.environ["INPUT_TOKEN"]
    reviewers = os.environ["INPUT_REVIEWERS"]
    action = os.environ["INPUT_ACTION"]
    with open(os.environ["GITHUB_EVENT_PATH"], "r") as fd:
        data = json.load(fd)

    github = github.Github(token)
    repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
    commit = repo.get_commit(os.environ["GITHUB_SHA"])
    try:
        pull = repo.get_pull(data["number"])
    except KeyError:
        pull = repo.get_pull(data["issue"]["number"])

    if action == "remove_verified_label":
        remove_verified_label(pull=pull)

    if action == "labels_by_user_input":
        labels_by_user_input(data=data, pull=pull)

    elif action == "add_reviewers":
        add_reviewers(data=data, pull=pull, reviewers=reviewers)

    elif action == "size_label_prs":
        size_label_prs(data=data, pull=pull)
        add_reviewers(data=data, pull=pull, reviewers=reviewers)

    elif action == "block_offensive_lanague":
        block_offensive_lanague(pull=pull)
