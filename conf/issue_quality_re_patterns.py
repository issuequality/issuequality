#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Padrões de RE para Github Formatted Markdown
gfm_pat = {
    'list': r'[*,-]\s.+|\d+\.\s+.+',
    'attach': r'(\[.+\.png\]|\[.+\.gif\]|\[.+\.jpg\]|\[.+\.docx\]|\[.+\.pptx\]|\[.+\.xlsx]|\[.+\.txt\]|\[.+\.pdf\]|\[.+\.zip\])(\(https\:\/\/github\.com\/.+\))'
}
