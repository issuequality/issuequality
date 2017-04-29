#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from github import Github
import configparser


class GithubRepoClient(object):

    """Classe que representa um cliente para um respositório do Github"""

    def __init__(self, full_name,
                 last_issue=-1,
                 last_execution=datetime(1970, 1, 1, 0, 0, 0, 0)
                 ):
        """TODO: to be defined1.

        :full_name: TODO
        :last_issue: TODO

        """
        # Constantes
        # Define a situação das issues a serem recuperadas
        self._ISSUES_STATE = 'open'
        # Define o tempo para esperar até fazer uma nova requisição
        self._TIME_TO_WAIT = 3
        # Variáveis
        try:
            self._last_issue = last_issue
            self._last_execution = last_execution
            # Obtendo o token da API do Github
            self._config = self._get_config()
            api_token = self._get_api_token()
            # Conectando com a API
            self._github_api = Github(login_or_token=api_token)
            self._repo = self._github_api.get_repo(full_name)
        except Exception as e:
            raise e

    def _get_config(self):
        """Retorna um objeto de configuração do tipo ConfigParser() para
            leitura de uma arquivo .ini
           :returns: Um objeto do tipo ConfigParser()

        """
        try:
            config = configparser.ConfigParser()
            config.readfp(open('conf/rmquality.ini'))
            return config
        except configparser.Error as e:
            raise e

    def _get_api_token(self):
        """TODO: Docstring for __get_api_token.
        :returns: TODO

        """
        try:

            if self._config is not None:
                return self._config.get('API_TOKEN', 'token_issuequality')
        except Exception as e:
            raise e

    def get_repo_name(self):
        """TODO: Docstring for get_repo_name.
        :returns: TODO

        """
        try:
            return self._repo.full_name
        except Exception as e:
            raise e

    def get_issues(self):
        """TODO: Docstring for get_issues.
        :returns: TODO

        """
        last_execution = self._last_execution
        issues_list = self._repo.get_issues(state=self._ISSUES_STATE,
                                            since=last_execution
                                            )
        last_issue_num = self.get_last_issue()
        return[issue for issue in issues_list if issue.number > last_issue_num]

    def set_last_issue(self,  issue_number):
        """TODO: Docstring for set_last_issue.

        :issue_number: TODO
        :returns: TODO

        """
        if issue_number > self._last_issue:
            self._last_issue = issue_number

    def get_last_issue(self):
        """TODO: Docstring for get_last_issue.
        :returns: TODO

        """
        return self._last_issue

    def set_last_execution(self, last_execution):
        """TODO: Docstring for __set_last_execution.

        :last_execution: TODO
        :returns: TODO

        """
        self._last_datetime_execution = last_execution
