#!/usr/bin/env python
# -*- coding: utf-8 -*-


class IssueReportAnalyser(object):

    """Docstring for IssueReportAnalyser. """

    def __init__(self):
        """TODO: to be defined1. """
        self.__DEFAULT_COMMENT = ("Dear @vagnerclementino,\n"
                                  "This issues do not looks great :-1:\n"
                                  " Would you like us to help you improve it?"
                                  " :smile:\n"
                                  "You could take the following action:\n"
                                  "- [ ] To Attach files with a screenshots"
                                  ":paperclip:\n"
                                  "- [ ] To mention a user or team on GitHub"
                                  " to trigger a notification and bring"
                                  " their attention to this issue.\n"
                                  "- [ ] Referencing issues."
                                  "\n\n\n"
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
        if issue.number == 12:
            return self.__DEFAULT_COMMENT
        else:
            return None
