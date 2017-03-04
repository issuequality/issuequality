#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GithubRepoClient import GithubRepoClient


class GithubRepoPool(object):

    """Docstring for GithubRepoPool. """

    def __init__(self):
        """TODO: to be defined1. """
        self._github_repo_pool = list()

    def create_github_repo_client(self, full_name):
        """TODO: Docstring for create_github_repo_client.

        :full_name: TODO
        :returns: TODO

        """

        for repo in self._github_repo_pool:
            if repo.get_repo_name() == full_name:
                return repo
        new_repo = GithubRepoClient(full_name)
        self.add_repo_to_pool(new_repo)
        return new_repo

    def add_repo_to_pool(self, github_repo_client):
        """TODO: Docstring for add_repo_to_pool.
        :returns: TODO

        """
        try:
            self._github_repo_pool.append(github_repo_client)
        except Exception as e:
            raise e
