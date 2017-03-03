# test suite.
from nose.tools import assert_equal
from .. import GithubMarkdown


def test_single_underscores():
    """don't touch single underscores inside words."""
    assert_equal(
        GithubMarkdown.gfm('foo_bar'),
        'foo_bar',
    )


def test_underscores_code_blocks():
    """don't touch underscores in code blocks."""
    assert_equal(
        GithubMarkdown.gfm('    foo_bar_baz'),
        '    foo_bar_baz',
    )


def test_underscores_pre_blocks():
    """don't touch underscores in pre blocks."""
    assert_equal(
        GithubMarkdown.gfm('<pre>\nfoo_bar_baz\n</pre>'),
        '\n\n<pre>\nfoo_bar_baz\n</pre>',
    )


def test_pre_block_pre_text():
    """don't treat pre blocks with pre-text differently."""
    a = '\n\n<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    b = 'hmm<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    assert_equal(
        GithubMarkdown.gfm(a)[2:],
        GithubMarkdown.gfm(b)[3:],
    )


def test_two_underscores():
    """escape two or more underscores inside words."""
    assert_equal(
        GithubMarkdown.gfm('foo_bar_baz'),
        'foo\\_bar\\_baz',
    )


def test_newlines_simple():
    """turn newlines into br tags in simple cases."""
    assert_equal(
        GithubMarkdown.gfm('foo\nbar'),
        'foo  \nbar',
    )


def test_newlines_group():
    """convert newlines in all groups."""
    assert_equal(
        GithubMarkdown.gfm('apple\npear\norange\n\nruby\npython\nerlang'),
        'apple  \npear  \norange\n\nruby  \npython  \nerlang',
    )


def test_newlines_long_group():
    """convert newlines in even long groups."""
    assert_equal(
        GithubMarkdown.gfm(('apple\npear\norange\n'
                            'banana\n\nruby\npython\nerlang'
                            )
                           ),
        'apple  \npear  \norange  \nbanana\n\nruby  \npython  \nerlang',
    )


def test_newlines_list():
    """don't convert newlines in lists."""
    assert_equal(
        GithubMarkdown.gfm('# foo\n# bar'),
        '# foo\n# bar',
    )
    assert_equal(
        GithubMarkdown.gfm('* foo\n* bar'),
        '* foo\n* bar',
    )
