#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
# import ipdb as pdb
from LogManager import LogManager
from IssueReportAnalyser import IssueReportAnalyser
from GithubRepoPool import GithubRepoPool
from time import sleep


class IssueQuality(object):

    """Docstring for RMQuality. """

    def __init__(self):
        """Classe que representa o programa RMQuality."""
        try:
            self._TIME_TO_WAIT = 3
            self._SECOND_TO_NEW_EXECUTION = 60
            # Define a data padrão da última execução da extensão
            self._logger = LogManager(log_path="./log/",
                                      file_name="issuequality"
                                      )
            self._report_analiser = IssueReportAnalyser()
        except Exception as e:
            raise e

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        try:
            gh_pool = GithubRepoPool()
            while True:
                # pdb.set_trace()
                for full_name in self.get_all_repo_fullname():
                    gh_repo_cli = gh_pool.create_github_repo_client(full_name)
                    repo_name = gh_repo_cli.get_repo_name()
                    self._logger.log_info(("Analisando as issues do "
                                           "repositório {0}".format(repo_name)
                                           )
                                          )
                    issue_counter = 0
                    for issue in gh_repo_cli.get_issues():
                        issue_counter = issue_counter + 1
                        self._logger.log_info(("Analisando a issue "
                                               "de nº {0}. Título: '{1}'"
                                               ).format(issue.number,
                                                        issue.title)
                                              )
                        gh_repo_cli.set_last_issue(issue.number)
                        # Gerando um comentário na issue com base no
                        # que foi reportado inicial
                        comment = self._report_analiser.analyse(issue)
                        if comment is not None:
                            issue.create_comment(comment)
                    if issue_counter == 0:
                        self._logger.log_info("Nenhuma issue para ser tratada")
                    else:
                        gh_repo_cli.set_last_execution(datetime.now())
                    self._logger.log_info(("Finalizada análise das issues do"
                                           " repositório {0}".format(repo_name)
                                           )
                                          )
                    self._logger.log_info(("Aguardando {0} segundos para"
                                           " uma nova execução."
                                           ).format(self._TIME_TO_WAIT)
                                          )
                    sleep(self._TIME_TO_WAIT)
                self._logger.log_info("Execução efetuada com sucesso.")
                sleep(self._SECOND_TO_NEW_EXECUTION)
        except Exception as e:
            self._logger.log_error(e)

    def get_all_repo_fullname(self):
        """TODO: Docstring for get_all_repo_fullname.
        :returns: TODO

        """
        repo_fullname_list = ['vagnerclementino/flask',
                              'vagnerclementino/GitScraper'
                              ]
        return iter(repo_fullname_list)
