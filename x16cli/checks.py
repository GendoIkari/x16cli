import os
import git
import x16cli.config as cfg

join = os.path.join


class ProjectPresentError(Exception):
    pass


class RepositoryCloneError(Exception):
    pass


class ReleaseNotFoundError(Exception):
    pass


def is_project_present(path):
    return os.path.exists(join(path, cfg.CFG_FILENAME))


def is_main_present(path):
    return os.path.exists(join(path, cfg.MAIN_NAME))


def is_correct_release(path, release):
    repo = git.Git(path)
    try:
        return release in (repo.describe('HEAD', tags=True), repo.rev_parse('HEAD', verify=True))
    except (git.GitCommandError, git.GitCommandNotFound):
        return False
