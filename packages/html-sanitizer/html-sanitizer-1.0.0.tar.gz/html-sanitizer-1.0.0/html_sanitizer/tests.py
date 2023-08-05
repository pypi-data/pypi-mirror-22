from __future__ import unicode_literals

from unittest import TestCase

from .sanitizer import Sanitizer


class SanitizerTestCase(TestCase):
    def run_tests(self, entries, sanitizer=Sanitizer()):
        for before, after in entries:
            after = before if after is None else after
            result = sanitizer.sanitize(before)
            self.assertEqual(
                result,
                after,
                "Cleaning '%s', expected '%s' but got '%s'" % (
                    before, after, result))

    def test_01_sanitize(self):
        entries = [
            ('<p>&nbsp;</p>', ''),
            ('<p>           </p>', ''),
            ('<span style="font-weight: bold;">Something</span><p></p>',
                '<strong>Something</strong>'),
            ('<p>abc <span>def <em>ghi</em> jkl</span> mno</p>',
                '<p>abc def <em>ghi</em> jkl mno</p>'),
            ('<span style="font-style: italic;">Something</span><p></p>',
                '<em>Something</em>'),
            ('<p>abc<br />def</p>', '<p>abc<br>def</p>'),
            ('<p><br/><strong></strong>  <br/></p>', ''),
            (
                '<p><br/><strong></strong>  <br/> abc</p>',
                '<p> abc</p>',
            ),
            (
                '<li><br>bla</li>',
                '<li>bla</li>',
            ),
        ]

        self.run_tests(entries)

    def test_02_a_tag(self):
        entries = (
            ('<a href="/foo">foo</a>', None),
            (
                '<a href="/foo" name="bar" target="some" title="baz"'
                ' cookies="yesplease">foo</a>',
                '<a href="/foo" name="bar" target="some" title="baz">foo</a>'
            ),
            ('<a href="http://somewhere.else">foo</a>', None),
            ('<a href="https://somewhere.else">foo</a>', None),
            ('<a href="javascript:alert()">foo</a>', '<a href="#">foo</a>'),
            ('<a href="javascript%3Aalert()">foo</a>', '<a href="#">foo</a>'),
            ('<a href="mailto:foo@bar.com">foo</a>', None),
            ('<a href="tel:1-234-567-890">foo</a>', None),
        )

        self.run_tests(entries)

    def test_03_merge(self):
        entries = (
            ('<h2>foo</h2><h2>bar</h2>', '<h2>foo bar</h2>'),
            ('<h2>foo  </h2>   <h2>   bar</h2>', '<h2>foo   bar</h2>'),
        )

        self.run_tests(entries)

    def test_04_p_in_li(self):
        entries = (
            ('<li><p>foo</p></li>', '<li> foo </li>'),
            ('<li>&nbsp;<p>foo</p> &#160; </li>', '<li> foo </li>'),
            (
                '<li>foo<p>bar<strong>xx</strong>rab</p><strong>baz</strong>'
                'a<p>b</p>c</li>',
                '<li>foo bar <strong>xx</strong>rab<strong>baz</strong>a b'
                ' c</li>'
            ),
        )

        self.run_tests(entries)

    def test_05_p_in_p(self):
        entries = (
            ('<p><p>foo</p></p>', '<p>foo</p>'),
            ('<p><p><p>&nbsp;</p> </p><p><br /></p></p>', ''),
            # This is actually correct as the second <p> implicitely
            # closes the first paragraph, and the trailing </p> is
            # deleted because it has no matching opening <p>
            ('<p>foo<p>bar</p>baz</p>', '<p>foo</p><p>bar</p>baz'),
        )

        self.run_tests(entries)

    def test_06_whitelist(self):
        entries = (
            ('<script src="http://abc">foo</script>', ''),
            ('<script type="text/javascript">foo</script>', ''),
        )

        self.run_tests(entries)

    def test_07_configuration(self):
        sanitizer = Sanitizer({
            'tags': {'h1', 'h2'},
            'empty': set(),
            'separate': set(),
            'attributes': {},
        })

        entries = (
            ('<h1>foo</h1>', None),
            (
                '<h1>foo</h1><h2>bar</h2><h3>baz</h3>',
                '<h1>foo</h1><h2>bar</h2>baz'
            ),
        )

        self.run_tests(entries, sanitizer=sanitizer)

    def test_08_li_with_marker(self):
        entries = (
            ('<li> - foo</li>', '<li>foo</li>'),
            ('<li>* foo</li>', '<li>foo</li>'),
        )

        self.run_tests(entries)

    def test_09_empty_p_text_in_li(self):
        # this results in an empty p.text
        entries = (
            (
                '<li><p><strong>foo</strong></p></li>',
                '<li><strong>foo</strong></li>',
            ),
            (
                '<li><p><em>foo</em></p></li>',
                '<li><em>foo</em></li>',
            ),
        )

        self.run_tests(entries)

    def test_10_broken_html(self):
        entries = (
            (
                '<p><strong>bla',
                '<p><strong>bla</strong></p>',
            ),
            (
                '<p><strong>bla<>/dsiad<p/',
                '<p><strong>bla&lt;&gt;/dsiad</strong></p>',
            ),
        )

        self.run_tests(entries)

    def test_11_nofollow(self):
        sanitizer = Sanitizer({
            'add_nofollow': True,
        })

        entries = (
            (
                '<p><a href="http://example.com/">example.com</a></p>',
                '<p><a href="http://example.com/"'
                ' rel="nofollow">example.com</a></p>',
            ),
        )

        self.run_tests(entries, sanitizer=sanitizer)

    def test_12_replacements(self):
        entries = (
            ('<b>Bla</b>', '<strong>Bla</strong>'),
            ('<i>Bla</i>', '<em>Bla</em>'),
        )

        self.run_tests(entries)

    def test_13_autolink(self):
        self.run_tests([(
            '<p>https://github.com/</p>',
            '<p>https://github.com/</p>',
        )])

        sanitizer = Sanitizer({
            'autolink': True,
        })

        self.run_tests([(
            '<p>https://github.com/</p>',
            '<p><a href="https://github.com/">https://github.com/</a></p>',
        )], sanitizer=sanitizer)

        sanitizer = Sanitizer({
            'autolink': True,
            'add_nofollow': True,
        })

        self.run_tests([(
            '<p>https://github.com/</p>',
            '<p><a href="https://github.com/"'
            ' rel="nofollow">https://github.com/</a></p>',
        )], sanitizer=sanitizer)
