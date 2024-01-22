import os
import git

ROOT_DIR = '/home/jovyan/work/'


def get_git_repo(path):
    try:
        repo = git.Repo(path)
        _ = repo.git_dir
        return repo
    except git.exc.InvalidGitRepositoryError:
        return False


def iterate_repos():
    for item in os.listdir(ROOT_DIR):
        if repo := get_git_repo(item):
            yield repo


def on_startup():
    for repo in iterate_repos():
        repo.git.pull('-f')


if __name__ == '__main__':
    on_startup()

