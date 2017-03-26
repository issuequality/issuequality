#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class IssueComment(object):

    """Docstring for IssueComment. """

    def __init__(self, project_name, issue):
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
        self._project_name = project_name
        self._issue = issue
        self._body = str()
        self._comment_metrics = dict()
        self._comment_metrics['step_to_reproduce'] = 0
        self._comment_metrics['attach_file'] = 0
        self._comment_metrics['code_fragment'] = 0
        self._comment_metrics['keyword_completude'] = dict()
        self._start_time = datetime.now()
        self._finish_time = self._start_time

    def set_body(self, str_text):
        """TODO: Docstring for set_body.

       :str_text: TODO
       :returns: TODO

       """
        if self._body:
            self._body = self._body + str_text
        else:
            self._body = str_text

    def set_comment_metric(self, metric, value):
        """TODO: Docstring for set_step_to_reproduce.

        :value: TODO
        :returns: TODO

        """
        self._comment_metrics[metric] = value

    def get_metrics(self):
        """TODO: Docstring for get_metrics.
        :returns: TODO

        """
        return self._comment_metrics

    def _has_comment(self, metrics):
        """TODO: Docstring for function.
        :returns: TODO

        """
        return True

    def get_body(self):
        """TODO: Docstring for  get_body.
        :returns: TODO

        """
        body_full = None
        if self._has_comment(self._comment_metrics):
            head_author = (self._HEAD_COMMENT).format(self._issue.user.login)
            body_full = head_author + self._body + self._FOOT_COMMENT
        return body_full

    def get_all_metrics(self):
        """TODO: Docstring for get_all_metrics.
        :returns: TODO

        """
        return self._comment_metrics

    def get_repo_name(self):
        """TODO: Docstring for get_repo_name.
        :returns: TODO

        """
        return self._project_name

    def get_issue_number(self):
        """TODO: Docstring for get_issue_number.

        :returns: TODO

        """
        return self._issue.number

    def get_start_time(self):
        """TODO: Docstring for get_start_time.
        :returns: TODO

        """
        return self._start_time

    def set_finish_time(self, finish_time):
        """TODO: Docstring for set_finish_time.

        :finish_time: TODO
        :returns: TODO

        """
        self._finish_time = finish_time

    def get_finish_time(self):
        """TODO: Docstring for get_finish_time.
        :returns: TODO

        """
        return self._finish_time
