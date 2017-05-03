#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
# import ipdb as pdb
from LogManager import LogManager
from IssueReportAnalyser import IssueReportAnalyser
from GithubRepoPool import GithubRepoPool
from time import sleep
import codecs
import csv
import sys


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

    def save_comment_as_csv(self, issue_comment, csv_file_name, header=False):
        """TODO: Docstring for save_comment_as_csv.

        :comment: TODO
        :file_name: TODO
        :returns: TODO

        """
        with codecs.open(csv_file_name, 'ab') as f:
            writer_csv = csv.writer(f,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_NONNUMERIC
                                    )
            repo_name = issue_comment.get_repo_name()
            issue_number = issue_comment.get_issue_number()
            row_tuple = (repo_name, issue_number,)
            dict_metrics = issue_comment.get_all_metrics()

            if header:
                header_tuple = ('repo_name',
                                'issue_number',
                                )

            for key in dict_metrics:

                if key == 'keyword_completude' or key == 'readability':
                    dict_key_compl = dict_metrics[key]
                    for key2 in dict_key_compl:
                        row_tuple += (dict_key_compl[key2],)
                        if header:
                            if key == 'keyword_completude':
                                header_tuple += (('keyword completude - ' +
                                                  key2),
                                                 )
                            elif key == 'readability':
                                header_tuple += ('readability - ' + key2,)
                else:
                    row_tuple += (dict_metrics[key],)
                    if header:
                        header_tuple += (key,)

            row_tuple += (issue_comment.get_start_time(),
                          issue_comment.get_finish_time(),
                          issue_comment.get_body(),
                          )
            if header:
                header_tuple += ('start_time',
                                 'finish_time',
                                 'comment',)

            # Escreve no aquivo se tiver o header
            if header:
                writer_csv.writerow(header_tuple)
            writer_csv.writerow(row_tuple)

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            gh_pool = GithubRepoPool()
            # pdb.set_trace()
            header = True
            csv_file_name = ('outputs/' +
                             datetime.now().strftime('%Y%m%d_%H%M%S_') +
                             'comments.csv'
                             )
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
                    comment = self._report_analiser.analyse(repo_name,
                                                            issue)
                    if comment.get_body() is not None:
                        print('Analisado o corpo ' + comment.get_body())
                        issue.create_comment(comment.get_body())
                        comment.set_finish_time(datetime.now())
                        self.save_comment_as_csv(comment,
                                                 csv_file_name,
                                                 header)
                        header = False
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
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
            self._logger.log_error(e)

    def get_all_repo_fullname(self):
        """TODO: Docstring for get_all_repo_fullname.
        :returns: TODO

        """
        repo_fullname_list = ['vagnerclementino/elasticsearch']
        return iter(repo_fullname_list)
