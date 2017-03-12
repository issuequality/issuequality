# test suite.
from nose.tools import assert_equal
from .. import IssueReportAnalyser


def test_get_match_list_gfm_list_simple():
    """Verifica se uma lista formatada como gfm foi recuperada corretamente
    """
    match_list = ['- George Washington', '- John Adams', '* Thomas Jefferson']
    text = '''- George Washington\n- John Adams\n* Thomas Jefferson'''
    gfm_item = 'list'
    analyser = IssueReportAnalyser.IssueReportAnalyser()
    assert_equal(analyser.get_match_list(text, gfm_item),
                 match_list
                 )

def test_get_match_list_gfm_list_numbered():
    """Verifica se uma lista formatada como gfm foi recuperada corretamente
    """
    match_list = ['1. James Madison',
                  '2. James Monroe',
                  '3. John Quincy Adams'
                  ]
    text = '''1. James Madison
              2. James Monroe
              3. John Quincy Adams
            '''
    gfm_item = 'list'
    analyser = IssueReportAnalyser.IssueReportAnalyser()
    assert_equal(analyser.get_match_list(text, gfm_item),
                 match_list
                 )

def test_get_match_list_gfm_list_mixed():
    """Verifica se uma lista formatada como gfm foi recuperada corretamente
    """
    match_list = ['1. Make my changes',
                  '1. Fix bug',
                  '2. Improve formatting',
                  '* Make the headings bigger',
                  '2. Push my commits to GitHub',
                  '3. Open a pull request',
                  '* Describe my changes',
                  '* Mention all the members of my team',
                  '* Ask for feedback'
                  ]
    text = '''1. Make my changes
                1. Fix bug
                2. Improve formatting
                  * Make the headings bigger
              2. Push my commits to GitHub
              3. Open a pull request
                * Describe my changes
                * Mention all the members of my team
                  * Ask for feedback
           '''
    gfm_item = 'list'
    analyser = IssueReportAnalyser.IssueReportAnalyser()
    assert_equal(analyser.get_match_list(text, gfm_item),
                 match_list
                 )
