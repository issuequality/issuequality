#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Padrões de RE para Github Formatted Markdown
gfm_pat = {
    'list': r'[*,-]\s.+|\d+\.\s+.+',
    'attach': (r'(\[.+\.PNG\]|\[.+\.GIF\]|\[.+\.JPG\]|\[.+\.DOCX\]|')
              ('\[.+\.PPTX\]|\[.+\.XLSX]|\[.+\.TXT\]|\[.+\.PDF\]|')
              ('\[.+\.ZIP\])(\(https\:\/\/github\.com\/.+\))')
}
