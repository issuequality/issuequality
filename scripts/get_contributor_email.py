#!/usr/bin/env python
# -*- coding: utf-8 -*-


from github import Github
from time import sleep
import configparser

try:
    repo_list = ['redmine/redmine',
                 'bugzilla/bugzilla',
                 'mantisbt/mantisbt'
                 ]
    config = configparser.ConfigParser()
    config.readfp(open('../conf/rmquality.ini'))
    api_token = config.get('API_TOKEN', 'token')
    git_api = Github(login_or_token=api_token)
    contrib_counter = 0
    email_counter = 0
    seconds_to_wait = 2
    user_message = str()
    for repo in repo_list:
        user_message = 'Analisando o repositório {0}'.format(repo)
        print(user_message)
        repo_git = git_api.get_repo(repo)
        for contrib in repo_git.get_contributors():
            contrib_counter = contrib_counter + 1
            if contrib.email is not None:
                # print(contrib.email)
                email_counter = email_counter + 1
            user_message = ('Esperando {0} para uma nova '
                            'consulta'
                            ).format(seconds_to_wait)
            print(user_message)
            sleep(seconds_to_wait)

        user_message = ('Fim da análise do projeto {0}. '
                        'Total de contribuidores: {1}. '
                        'Total com e-mail {2}').format(repo,
                                                       contrib_counter,
                                                       email_counter)
        print(user_message)
except Exception as e:
    print(e)
