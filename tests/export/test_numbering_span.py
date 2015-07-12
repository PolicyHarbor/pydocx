# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)


from unittest import TestCase

from pydocx.export.numbering_span import NumberingSpanBuilder
from pydocx.openxml.wordprocessing import (
    Break,
    Paragraph,
    Run,
    TabChar,
    Text,
)


class NumberingSpanTestBase(TestCase):
    def setUp(self):
        self.builder = NumberingSpanBuilder()


class CleanParagraphTestCase(NumberingSpanTestBase):
    def test_empty_paragraph(self):
        paragraph = Paragraph()
        expected = Paragraph()

        self.builder.clean_paragraph(paragraph, 'Foo')
        self.assertEqual(repr(paragraph), repr(expected))


class RemoveInitialTextFromParagraphTestCase(NumberingSpanTestBase):
    def test_empty_paragraph(self):
        paragraph = Paragraph()
        expected = Paragraph()

        self.builder.remove_initial_text_from_paragraph(paragraph, 'Foo ')
        self.assertEqual(repr(paragraph), repr(expected))

    def test_single_run_single_text_node(self):
        paragraph = Paragraph(children=[
            Run(children=[Text(text='Foo Bar')]),
        ])
        expected = Paragraph(children=[
            Run(children=[Text(text='Bar')]),
        ])

        self.builder.remove_initial_text_from_paragraph(paragraph, 'Foo ')
        self.assertEqual(repr(paragraph), repr(expected))

    def test_only_removes_if_leading_text_matches(self):
        paragraph = Paragraph(children=[
            Run(children=[Text(text='NO Foo Bar')]),
        ])
        expected = Paragraph(children=[
            Run(children=[Text(text='NO Foo Bar')]),
        ])

        self.builder.remove_initial_text_from_paragraph(paragraph, 'Foo ')
        self.assertEqual(repr(paragraph), repr(expected))

    def test_many_runs_many_text_nodes(self):
        paragraph = Paragraph(children=[
            Run(children=[
                Text(text='a'),
                Text(text='b'),
            ]),
            Run(children=[
                Text(text='c'),
                Text(text='d'),
            ]),
            Run(children=[
                Text(text='e'),
                Text(text='f'),
            ]),
        ])
        expected = Paragraph(children=[
            Run(children=[
                Text(text=''),
                Text(text=''),
            ]),
            Run(children=[
                Text(text=''),
                Text(text=''),
            ]),
            Run(children=[
                Text(text=''),
                Text(text='f'),
            ]),
        ])

        self.builder.remove_initial_text_from_paragraph(paragraph, 'abcde')
        self.assertEqual(repr(paragraph), repr(expected))

    def test_leading_non_text_is_ignored(self):
        paragraph = Paragraph(children=[
            Run(children=[
                Break(),
                Text(text='Foo Bar'),
            ]),
        ])
        expected = Paragraph(children=[
            Run(children=[
                Break(),
                Text(text='Bar'),
            ]),
        ])

        self.builder.remove_initial_text_from_paragraph(paragraph, 'Foo ')
        self.assertEqual(repr(paragraph), repr(expected))

    def test_all_text_is_removed(self):
        paragraph = Paragraph(children=[
            Run(children=[
                Text(text='a'),
                Text(text='b'),
            ]),
            Run(children=[
                Text(text='c'),
                Text(text='d'),
            ]),
        ])
        expected = Paragraph(children=[
            Run(children=[
                Text(text=''),
                Text(text=''),
            ]),
            Run(children=[
                Text(text=''),
                Text(text=''),
            ]),
        ])

        self.builder.remove_initial_text_from_paragraph(paragraph, 'abcd')
        self.assertEqual(repr(paragraph), repr(expected))


class RemoveInitialTabCharsFromParagraphTestCase(NumberingSpanTestBase):
    def test_empty_paragraph_nothing_changes(self):
        paragraph = Paragraph()
        expected = Paragraph()

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))

    def test_single_run_single_text_node_no_tabs_nothing_changes(self):
        paragraph = Paragraph(children=[
            Run(children=[Text(text='Foo')]),
        ])
        expected = Paragraph(children=[
            Run(children=[Text(text='Foo')]),
        ])

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))

    def test_single_initial_tab_is_removed(self):
        paragraph = Paragraph(children=[
            Run(children=[TabChar()]),
        ])
        expected = Paragraph(children=[
            Run(),
        ])

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))

    def test_many_runs_many_tabs_are_removed(self):
        paragraph = Paragraph(children=[
            Run(children=[
                TabChar(),
                TabChar(),
            ]),
            Run(children=[
                TabChar(),
            ]),
            Run(),
            Run(children=[
                TabChar(),
                TabChar(),
            ]),
        ])
        expected = Paragraph(children=[
            Run(),
            Run(),
            Run(),
            Run(),
        ])

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))

    def test_only_tabs_before_break_are_removed(self):
        paragraph = Paragraph(children=[
            Run(children=[
                TabChar(),
            ]),
            Run(children=[
                TabChar(),
                Break(),
                TabChar(),
            ]),
        ])
        expected = Paragraph(children=[
            Run(),
            Run(children=[
                Break(),
                TabChar(),
            ]),
        ])

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))

    def test_only_tabs_before_first_text_are_removed(self):
        paragraph = Paragraph(children=[
            Run(children=[
                TabChar(),
            ]),
            Run(children=[
                TabChar(),
                Text(),
                TabChar(),
            ]),
        ])
        expected = Paragraph(children=[
            Run(),
            Run(children=[
                Text(),
                TabChar(),
            ]),
        ])

        self.builder.remove_initial_tab_chars_from_paragraph(paragraph)
        self.assertEqual(repr(paragraph), repr(expected))
