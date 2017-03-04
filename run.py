#!/usr/bin/env python
# -*- coding: utf-8 -*-

from IssueQuality import IssueQuality
import sys

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    issue_quality = IssueQuality()
    issue_quality.run()
