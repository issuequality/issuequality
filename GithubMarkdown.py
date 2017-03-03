import re
from hashlib import md5

def gfm(text):
    # Extract pre blocks.
    extractions = {}
    def pre_extraction_callback(matchobj):
        digest = md5(matchobj.group(0)).hexdigest()
        extractions[digest] = matchobj.group(0)
        return "{gfm-extraction-%s}" % digest
    pattern = re.compile(r'<pre>.*?</pre>', re.MULTILINE | re.DOTALL)
    text = re.sub(pattern, pre_extraction_callback, text)

    # Prevent foo_bar_baz from ending up with an italic word in the middle.
    def italic_callback(matchobj):
        s = matchobj.group(0)
        if list(s).count('_') >= 2:
            return s.replace('_', '\_')
        return s
    text = re.sub(r'^(?! {4}|\t)\w+_\w+_\w[\w_]*', italic_callback, text)

    # In very clear cases, let newlines become <br /> tags.
    def newline_callback(matchobj):
        if len(matchobj.group(1)) == 1:
            return matchobj.group(0).rstrip() + '  \n'
        else:
            return matchobj.group(0)
    pattern = re.compile(r'^[\w\<][^\n]*(\n+)', re.MULTILINE)
    text = re.sub(pattern, newline_callback, text)

    # Insert pre block extractions.
    def pre_insert_callback(matchobj):
        return '\n\n' + extractions[matchobj.group(1)]
    text = re.sub(r'{gfm-extraction-([0-9a-f]{32})\}', pre_insert_callback, text)

    return text


# test suite.
try:
    from nose.tools import assert_equal
except importerror:
    def assert_equal(a, b):
        assert a == b, '%r != %r' % (a, b)

def test_single_underscores():
    """don't touch single underscores inside words."""
    assert_equal(
        gfm('foo_bar'),
        'foo_bar',
    )

def test_underscores_code_blocks():
    """don't touch underscores in code blocks."""
    assert_equal(
        gfm('    foo_bar_baz'),
        '    foo_bar_baz',
    )

def test_underscores_pre_blocks():
    """don't touch underscores in pre blocks."""
    assert_equal(
        gfm('<pre>\nfoo_bar_baz\n</pre>'),
        '\n\n<pre>\nfoo_bar_baz\n</pre>',
    )

def test_pre_block_pre_text():
    """don't treat pre blocks with pre-text differently."""
    a = '\n\n<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    b = 'hmm<pre>\nthis is `a\\_test` and this\\_too\n</pre>'
    assert_equal(
        gfm(a)[2:],
        gfm(b)[3:],
    )

def test_two_underscores():
    """escape two or more underscores inside words."""
    assert_equal(
        gfm('foo_bar_baz'),
        'foo\\_bar\\_baz',
    )

def test_newlines_simple():
    """turn newlines into br tags in simple cases."""
    assert_equal(
        gfm('foo\nbar'),
        'foo  \nbar',
    )

def test_newlines_group():
    """convert newlines in all groups."""
    assert_equal(
        gfm('apple\npear\norange\n\nruby\npython\nerlang'),
        'apple  \npear  \norange\n\nruby  \npython  \nerlang',
    )

def test_newlines_long_group():
    """convert newlines in even long groups."""
    assert_equal(
        gfm('apple\npear\norange\nbanana\n\nruby\npython\nerlang'),
        'apple  \npear  \norange  \nbanana\n\nruby  \npython  \nerlang',
    )

def test_newlines_list():
    """don't convert newlines in lists."""
    assert_equal(
        gfm('# foo\n# bar'),
        '# foo\n# bar',
    )
    assert_equal(
        gfm('* foo\n* bar'),
        '* foo\n* bar',
    )
