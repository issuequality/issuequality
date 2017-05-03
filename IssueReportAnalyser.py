#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf.issue_quality_re_patterns as patterns
import conf.issue_quality_keywords as keywords
import re
from BeautifulSoup import BeautifulSoup
from markdown import markdown
from GithubMarkdown import GithubMarkdown
from IssueComment import IssueComment
import codecs
import nltk
from nltk.corpus import stopwords
from textstat.textstat import textstat
# import ipdb as pdb


class IssueReportAnalyser(object):

    """Docstring for IssueReportAnalyser. """

    def __init__(self):
        """TODO: to be defined1. """
        self._SCORE_FLESCH = 50
        self._SCORE_ARI = 13
        self._SCORE_DALE_CHALL = 13

    def analyse(self, project_name, issue):
        """TODO: Docstring for analyse.

        :issue: TODO
        :returns: Uma string no formato Markdown, ou None caso nenhum
                  comentário seja necessário
        """
        counter = 0
        metric_value = 0
        comment_aux = str()
        comment = IssueComment(project_name, issue)

        # pdb.set_trace()
        metric_value, comment_aux = self.analyse_steps_to_reproduce(issue)
        if comment_aux:
            comment.set_body(comment_aux)
            counter = counter + 1
            comment.set_comment_metric('step_to_reproduce', 0)
        else:
            comment.set_comment_metric('step_to_reproduce', 1)

        metric_value, comment_aux = self.analyse_attached_files(issue)
        if comment_aux:
            comment.set_body(comment_aux)
            counter = counter + 1
            comment.set_comment_metric('attach_file', 0)
        else:
            comment.set_comment_metric('attach_file', 1)

        metric_value, comment_aux = self.analyse_code_block(issue)
        if comment_aux:
            comment.set_body(comment_aux)
            counter = counter + 1
            comment.set_comment_metric('code_fragment', 0)
        else:
            comment.set_comment_metric('code_fragment', 1)

        dict_key_compl, comment_aux = self.analyse_keywork_completude(issue)
        if comment_aux:
            comment.set_body(comment_aux)
            counter = counter + 1
            comment.set_comment_metric('keyword_completude', dict_key_compl)
        else:
            comment.set_comment_metric('keyword_completude', dict_key_compl)

        dic_read_tests, comment_aux = self.analyse_readbility(issue)
        if comment_aux:
            comment.set_body(comment_aux)
            counter = counter + 1
            comment.set_comment_metric('readability', dic_read_tests)
        else:
            comment.set_comment_metric('readability', dic_read_tests)

        # Definindo o envio do comentário
        if counter:
            return comment
        else:
            return None

    def get_match_list(self, text, gfm_key):
        """Retorna a lista de string que match com um dado item do Github
        Formatted Markdown

        :text: TODO
        :gfm_item: TODO
        :returns: TODO

        """
        if gfm_key in patterns.gfm_pat:
            match_list = re.findall(patterns.gfm_pat[gfm_key],
                                    text,
                                    re.MULTILINE)

        return match_list

    def analyse_steps_to_reproduce(self, issue):
        """Analise a existencia de estapas para reproduzir através
           da buscar por listas no relato da issue
        :issue: TODO
        :returns: TODO

        """
        # Não realiza análise para uma issue sem 'body'
        if not issue.body:
            return (1, (" - [ ] Add step to reproduce.\n"))

        match_list = self.get_match_list(issue.body,
                                         'list')

        if len(match_list) == 0:
            return (1, (" - [ ] Add step to reproduce.\n"))
        else:
            return (0, None)

    def analyse_attached_files(self, issue):
        """TODO: Docstring for analyse_attached_files.

        :issue: TODO
        :returns: TODO

        """
        # Não realiza análise para uma issue sem 'body'
        if not issue.body:
            return (1, (" - [ ] To Attach files with a screenshots"
                    " or stacktraces.\n"
                        )
                    )
        match_list = self.get_match_list(issue.body,
                                         'attach')
        if len(match_list) == 0:
            return (1, (" - [ ] To Attach files with a screenshots"
                    " or stacktraces.\n"
                        )
                    )
        else:
            return (0, None)

    def analyse_code_block(self, issue):
        """TODO: Docstring for analyse_code_block.

        :issue: TODO
        :returns: TODO

        """
        # Não realiza análise para uma issue sem 'body'
        if not issue.body:
            return (1, (" - [ ] To include a code block.\n"))

        match_list = self.get_match_list(issue.body,
                                         'code')
        if len(match_list) == 0:
            return (1, (" - [ ] To include a code block.\n"))
        else:
            return (0, None)

    def markdown_to_text(self, markdown_str):
        """Tranforma uma string no formato markdown em uma string

        :markdown_str: TODO
        :returns: TODO

        """
        html = markdown(markdown_str)
        text_str = ''.join(BeautifulSoup(html).findAll(text=True))
        return text_str

    def tokenize_text(self, str_text):
        """TODO: Docstring for tokenize_text.

        :str_text: TODO
        :returns: TODO

        """

        default_stopwords = set(stopwords.words('english'))

        # We're adding some on our own - could be done inline like this...
        # custom_stopwords = set((u'–', u'dass', u'mehr')) ... but let's read
        # them from a file instead (one stopword per line, UTF-8)
        stopwords_file = './data/stopwords.txt'
        custom_stopwords = set(codecs.open(stopwords_file, 'r',
                                           'utf-8').read().splitlines())

        all_stopwords = default_stopwords | custom_stopwords
        words = nltk.word_tokenize(str_text)

        # Remove single-character tokens (mostly punctuation)
        words = [word for word in words if len(word) > 1]

        # Remove numbers
        words = [word for word in words if not word.isnumeric()]

        # Lowercase all words (default_stopwords are lowercase too)
        words = [word.lower() for word in words]

        # Stemming words seems to make matters worse, disabled
        stemmer = nltk.stem.snowball.SnowballStemmer('english')
        words = [stemmer.stem(word) for word in words]

        # Remove stopwords
        words = [word for word in words if word not in all_stopwords]
        return words

    def find_keywords(self, words):
        """TODO: Docstring for find_keywords.

        :words: TODO
        :returns: TODO

        """
        dict_freq_keywords = dict()
        for key in keywords.dict_keywords:
            dict_freq_keywords[key] = 0

        for word in words:
            # Verificando a existencia da palavra entre as keywords
            for key in keywords.dict_keywords:
                if word in keywords.dict_keywords[key]:
                    dict_freq_keywords[key] = dict_freq_keywords[key] + 1

        return dict_freq_keywords

    def analyse_keywork_completude(self, issue):
        """TODO: Docstring for analyse_keywork_completude.

        :issue: TODO
        :returns: TODO

        """
        # Analisando issue sem relato
        if not issue.body:
            message = (" - [ ] To improve the text in issue body.\n")
            dict_freq_keywords = dict()
            for key in keywords.dict_keywords:
                dict_freq_keywords[key] = 0
            return (dict_freq_keywords, message)

        gfm = GithubMarkdown(issue.body)
        str_markdown = gfm.parse(issue.body)
        str_text = self.markdown_to_text(str_markdown)
        words = self.tokenize_text(str_text)
        dict_freq_keywords = self.find_keywords(words)

        counter = 0
        for key in dict_freq_keywords:
            if dict_freq_keywords[key]:
                counter = counter + 1
        if counter <= 2:
            message = (" - [ ] To improve the text in issue body.\n")
        else:
            message = None
        return (dict_freq_keywords, message)

    def _has_low_readbility(self, dic_tests_metrics):
        """TODO: Docstring for _has_low_readbility.

        :dic_tests_metrics: TODO
        :returns: TODO

        """

        if(
            (dic_tests_metrics['flesch'] <= self._SCORE_FLESCH) and
            (dic_tests_metrics['ari'] >= self._SCORE_ARI)
           ):
            return True

        if (
            (dic_tests_metrics['flesch'] <= self._SCORE_FLESCH) and
            (dic_tests_metrics['dale-chall'] >= self._SCORE_DALE_CHALL)
           ):
            return True

        if (
            (dic_tests_metrics['dale-chall'] >= self._SCORE_DALE_CHALL) and
            (dic_tests_metrics['ari'] >= self._SCORE_ARI)
           ):
            return True

        # Todos os teste falharam, retorna Falso
        return False

    def analyse_readbility(self, issue):
        """TODO: Docstring for analyse_readbility.

        :issue: TODO
        :returns: TODO

        """
        # Não realiza análise para uma issue sem 'body'
        # if not issue.body:
        #    message = ' - [ ] To improve the readability of the text.\n'
        #    return (None, message)

        gfm = GithubMarkdown(issue.body)
        str_markdown = gfm.parse(issue.body)
        str_text = self.markdown_to_text(str_markdown)
        dic_test_readbility = dict()

        if not issue.body:
            message = (" - [ ] To improve the text in issue body.\n")
            dic_test_readbility['flesch'] = -1
            dic_test_readbility['ari'] = 100
            dic_test_readbility['dale-chall'] = 100
            return (dic_test_readbility, message)

        # Analisando a métrica Flesch Reading Ease Score
        score_flesch = textstat.flesch_reading_ease(str_text)
        dic_test_readbility['flesch'] = score_flesch

        # Analisando com o teste Automated Readability Index (ARI)
        score_ari = textstat.automated_readability_index(str_text)
        dic_test_readbility['ari'] = score_ari

        # Analisando com o teste Dale-Chall Readbility Score
        score_dale_chal = textstat.dale_chall_readability_score(str_text)
        dic_test_readbility['dale-chall'] = score_dale_chal

        if not issue.body:
            message = (" - [ ] To improve the text in issue body.\n")
            return (dic_test_readbility, message)

        if self._has_low_readbility(dic_test_readbility):
            message = ' - [ ] To improve the readability of the text.\n'
        else:
            message = None

        return (dic_test_readbility, message)
