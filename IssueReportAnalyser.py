#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf.issue_quality_re_patterns as patterns
import conf.issue_quality_keywords as keywords
import re
from BeautifulSoup import BeautifulSoup
from markdown import markdown
from GithubMarkdown import GithubMarkdown
import codecs
import nltk
from nltk.corpus import stopwords


class IssueReportAnalyser(object):

    """Docstring for IssueReportAnalyser. """

    def __init__(self):
        """TODO: to be defined1. """
        self._HEAD_COMMENT = ("Dear @{0},\n"
                              "This issues do not looks great :-1:\n"
                              " Would you like us to help you improve it?"
                              " :smile:\n"
                              "You could take the following action:\n"
                              )
        self._FOOT_COMMENT = ("\n\n\n"
                              "**Did you know:**\n"
                              "* Issues containing *stack traces* get"
                              " fixed sooner.\n"
                              "* Issues that are *easier to read* "
                              " have lower lifetimes.\n"
                              "* Including *code samples* in your issue"
                              " increases the chances of it"
                              " getting fixed.\n"
                              )

    def analyse(self, issue):
        """TODO: Docstring for analyse.

        :issue: TODO
        :returns: Uma string no formato Markdown, ou None caso nenhum
                  comentário seja necessário
        """
        dict_metrics = dict()
        comment = str()
        counter = 0
        comment_aux = str()
        comment = (self._HEAD_COMMENT).format(issue.user.login)

        comment_aux = self.analyse_steps_to_reproduce(issue)
        if comment_aux:
            comment = comment + comment_aux
            counter = counter + 1
            dict_metrics['step_to_reproduce'] = 1
        else:
            dict_metrics['step_to_reproduce'] = 0

        comment_aux = self.analyse_attached_files(issue)
        if comment_aux:
            comment = comment + comment_aux
            counter = counter + 1
            dict_metrics['attach'] = 1
        else:
            dict_metrics['attach'] = 0

        comment_aux = self.analyse_code_block(issue)
        if comment_aux:
            comment = comment + comment_aux
            counter = counter + 1
            dict_metrics['code'] = 1
        else:
            dict_metrics['code'] = 0

        self.analyse_keywork_completude(issue)

        # Definindo o envio do comentário
        if counter:
            comment = comment + self._FOOT_COMMENT
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
        match_list = self.get_match_list(issue.body,
                                         'list')

        if len(match_list) == 0:
            return (" - [ ] Add step to reproduce.\n")
        else:
            None

    def analyse_attached_files(self, issue):
        """TODO: Docstring for analyse_attached_files.

        :issue: TODO
        :returns: TODO

        """

        match_list = self.get_match_list(issue.body,
                                         'attach')
        if len(match_list) == 0:
            return ((" - [ ] To Attach files with a screenshots"
                    " or stacktraces.\n"
                     )
                    )
        else:
            None

    def analyse_code_block(self, issue):
        """TODO: Docstring for analyse_code_block.

        :issue: TODO
        :returns: TODO

        """
        match_list = self.get_match_list(issue.body,
                                         'code')
        if len(match_list) == 0:
            return (" - [ ] To include a code block")
        else:
            None

    def markdown_to_text(self, markdown_str):
        """Tranforma uma string no formato markdown em uma string

        :markdown_str: TODO
        :returns: TODO

        """
        pass
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
            dict_freq_keywords [key] = 0

        for word in words:
            print('Analisando palavra: ' + word)
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
        gfm = GithubMarkdown(issue.body)
        str_markdown = gfm.parse(issue.body)
        str_text = self.markdown_to_text(str_markdown)
        words = self.tokenize_text(str_text)
        print(words)
        freq_keywords = self.find_keywords(words)
        print(freq_keywords)

