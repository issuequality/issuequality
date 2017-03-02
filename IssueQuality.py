#!/usr/bin/env python
# -*- coding: utf-8 -*-

from github import Github
import configparser
from datetime import datetime
import time
# import ipdb as pdb
from LogManager import LogManager


class IssueQuality(object):

    """Docstring for RMQuality. """

    def __init__(self, full_name, last_issue=-1):
        """Classe que representa o programa RMQuality."""
        try:
            # Constantes
            # Define a situação das issues a serem recuperadas
            self.__ISSUES_STATE = 'open'
            # Define o tempo para esperar até fazer uma nova requisição
            self.__TIME_TO_WAIT = 3
            # Define a data padrão da última execução da extensão
            self.__LAST_EXECUTION = datetime(1970, 1, 1, 0, 0, 0, 0)

            self.__last_issue = last_issue
            self.__config = self.__get_config()
            api_token = self.__get_api_token()
            self.__github_api = Github(login_or_token=api_token)
            self.__repo = self.__github_api.get_repo(full_name)
            self.__last_datetime_execution = self.__LAST_EXECUTION
            self.__logger = LogManager(log_path="./log/",
                                       file_name="rmquality"
                                       )
        except Exception as e:
            raise e

    def __get_config(self):
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

    def __get_api_token(self):
        """TODO: Docstring for __get_api_token.
        :returns: TODO

        """
        try:

            if self.__config is not None:
                return self.__config.get('API_TOKEN', 'token')
        except Exception as e:
            raise e

    def __get_repo_name(self):
        """TODO: Docstring for get_repo_name.
        :returns: TODO

        """
        try:
            return self.__repo.full_name
        except Exception as e:
            raise e

    def __get_issues(self):
        """TODO: Docstring for get_issues.
        :returns: TODO

        """
        last_execution = self.__last_datetime_execution
        return self.__repo.get_issues(state=self.__ISSUES_STATE,
                                      since=last_execution)

    def __set_last_issue(self,  issue_number):
        """TODO: Docstring for set_last_issue.

        :issue_number: TODO
        :returns: TODO

        """
        if issue_number > self.__last_issue:
            self.__last_issue = issue_number

    def __get_last_issue(self):
        """TODO: Docstring for get_last_issue.
        :returns: TODO

        """
        return self.__last_issue

    def __filter_by_issue_number(self, last_issue_num, issues_list):
        """TODO: Docstring for __filter_by_issue_number.

        :issue_number: TODO
        :returns: TODO

        """
        return[issue for issue in issues_list if issue.number > last_issue_num]

    def __build_comment(self, issue):
        """Constroi um comentário com base em uma issue
        criada no repositório

        :issue: Uma issue (github.Issue.Issue) criada no repositório
        :returns: Uma string representando o corpo do comentário

        """
        comment = str()
        if issue.number == 1:
            comment = ("Dear @vagnerclementino,\n"
                       "This issues do not looks great :-1:\n"
                       " Would you like us to help you improve it? :smile:\n"
                       "You could take the following action:\n"
                       "- [ ] To Attach files with a screenshots:paperclip:\n"
                       "- [ ] To mention a user or team on GitHub to "
                       "trigger a notification and bring their attention "
                       "to this issue.\n"
                       "- [ ] Referencing issues."
                       "\n\n\n"
                       "**Did you know:**\n"
                       "* Issues containing *stack traces* get "
                       "fixed sooner.\n"
                       "* Issues that are *easier to read* have lower "
                       "lifetimes.\n"
                       "* Including *code samples* in your issue increases"
                       " the chances of it getting fixed.\n"
                       )
        else:
            comment = None
        return comment

    def __set_last_execution(self, last_execution):
        """TODO: Docstring for __set_last_execution.

        :last_execution: TODO
        :returns: TODO

        """
        self.__last_datetime_execution = last_execution

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        try:
            while True:
                # pdb.set_trace()
                repo_name = self.__get_repo_name()
                self.__logger.log_info(("Analisando as issues do "
                                        " repositório {0}".format(repo_name)
                                        )
                                       )
                while True:
                    counter = 0
                    issues_list = self.__get_issues()
                    # Recuperando o número da última issue analisada
                    # pelo sistema
                    last_issue = self.__get_last_issue()
                    filtered_list = self.__filter_by_issue_number(last_issue,
                                                                  issues_list)
                    for issue in filtered_list:
                        counter = counter + 1
                        self.__set_last_issue(issue.number)
                        self.__logger.log_info(("[{0}] Issue nº {1}. Title "
                                                " {2}".format(counter,
                                                              issue.number,
                                                              issue.title
                                                              )
                                                )
                                               )
                        comment_body = self.__build_comment(issue)
                        if comment_body is not None:
                            issue.create_comment(comment_body)

                    if counter == 0:
                        self.__logger.log_info(("Nenhuma issue para "
                                                "ser tratada"
                                                )
                                               )
                    self.__set_last_execution(datetime.now())
                    self.__logger.log_info(("Esperando {0} segundos "
                                            "para uma nova verificação!"
                                            ).format(self.__TIME_TO_WAIT)
                                           )
                    time.sleep(self.__TIME_TO_WAIT)
        except Exception as e:
            self.__logger.log_error(e)
