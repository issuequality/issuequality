#!/usr/bin/env python
# -*- coding: utf-8 -*-


from github import Github
from time import sleep
import configparser
import codecs
import csv
import sys
from datetime import datetime


def print_message(message):
    """TODO: Docstring for print_message.

    :message: TODO
    :returns: TODO

    """
    str_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S')
    print ('[{0}] {1}'.format(str_date, message))

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    repo_list = ['redmine/redmine',
                 'bugzilla/bugzilla',
                 'mantisbt/mantisbt',
                 'spring-projects/spring-framework',
                 'elastic/elasticsearch',
                 'google/guava'
                 ]
    config = configparser.ConfigParser()
    config.readfp(open('../conf/rmquality.ini'))
    api_token = config.get('API_TOKEN', 'token')
    git_api = Github(login_or_token=api_token)
    contrib_counter = 0
    email_counter = 0
    seconds_to_wait = 2
    user_message = str()
    csv_file_name = 'contributor_email.csv'
    with codecs.open(csv_file_name, 'wb') as f:
        writer_csv = csv.writer(f,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC
                                )
        # Escrevendo o cabeçaho do arquivo CSV
        writer_csv.writerow(('#',
                             'repositorio',
                             'nome_contribuidor',
                             'email_contribuidor'
                             )
                            )
        for repo in repo_list:
            user_message = 'Analisando o repositório {0}.'.format(repo)
            print_message(user_message)
            repo_git = git_api.get_repo(repo)
            for contrib in repo_git.get_contributors():
                contrib_counter = contrib_counter + 1
                if contrib.email is not None:
                    email_counter = email_counter + 1
                    writer_csv.writerow((email_counter,
                                        repo,
                                        contrib.name,
                                        contrib.email)
                                        )
                user_message = ('Esperando {0} segundos para uma nova '
                                'consulta!'
                                ).format(seconds_to_wait)
                print_message(user_message)
                sleep(seconds_to_wait)

            user_message = ('Fim da análise do projeto {0}.'
                            'Total de contribuidores: {1}. '
                            'Total com e-mail {2}').format(repo,
                                                           contrib_counter,
                                                           email_counter)
        print_message(user_message)
except Exception as e:
    print_message(e)
