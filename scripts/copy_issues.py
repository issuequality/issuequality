#!/usr/bin/env python
# -*- coding: utf-8 -*-

from github import Github, GithubException
import configparser
from LogManager import LogManager


def main():
    """
    Função principal de execução do módulo
    """

    try:

        log = LogManager(log_path="./log/",
                         file_name="copy_issues"
                         )
        repo_orig_fullname = 'pallets/flask'
        repo_dest_fullname = 'vagnerclementino/flask'
        max_item_to_copy = 5
        config = configparser.ConfigParser()
        config.readfp(open('conf/rmquality.ini'))
        api_token = config.get('API_TOKEN', 'token')
        git_api = Github(login_or_token=api_token)
        repo_orig = git_api.get_repo(repo_orig_fullname)
        repo_dest = git_api.get_repo(repo_dest_fullname)
        counter = 0
        for issue in repo_orig.get_issues():
            if counter < max_item_to_copy:
                new_issue = repo_dest.create_issue(title=issue.title,
                                                   body=issue.body,
                                                   labels=issue.get_labels()
                                                   )
                if new_issue.number is not None:
                    log.info(("Issue nº {0} "
                              "com o título '{1}' "
                              "criada com sucesso!".format(new_issue.number,
                                                           new_issue.title
                                                           )
                              )
                             )
                counter = counter + 1
            else:
                break
    except configparser.Error as e:
        log.error(e)
    except GithubException as ghe:
        log.error(ghe.data)
    except Exception as e:
        log.error(e)


if __name__ == "__main__":
    main()
