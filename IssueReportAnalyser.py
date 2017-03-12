#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf.issue_quality_re_patterns as patterns
import re


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
        if issue.number == 12:
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
            if counter:
                comment = comment + self._FOOT_COMMENT
                return comment
        else:
            return None


    def get_match_list(self, text, gfm_item):
        """Retorna a lista de string que match com um dado item do Github
        Formatted Markdown

        :text: TODO
        :gfm_item: TODO
        :returns: TODO

        """
        if gfm_item == 'list':
            match_list = re.findall(patterns.gfm_pat['list'],
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

        if len(match_list) > 0:
            return (" - [ ] Add step to reproduce.\n")
        else:
            None

