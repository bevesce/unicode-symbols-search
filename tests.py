import unittest
from unicode_symbols_search.unicode_symbols_search import create_query
from unicode_symbols_search.unicode_symbols_search import parse_symbol


class Query(unittest.TestCase):
    def test_symbol_match(self):
        self.assertTrue(
            create_query('a')(
                ('a', 'x')
            )
        )

    def test_description_match(self):
        self.assertTrue(
            create_query('a')(
                ('x', 'a')
            )
        )

    def test_description_match_both_words(self):
        self.assertTrue(
            create_query('a b')(
                ('x', 'a b')
            )
        )

    def test_description_match_one_words(self):
        self.assertFalse(
            create_query('a b')(
                ('x', 'a c')
            )
        )

    def test_doesnt_match(self):
        self.assertFalse(
            create_query('z')(
                ('x', 'a c')
            )
        )


class Load(unittest.TestCase):
    def test_parse_symbol(self):
        self.assertEqual(
            parse_symbol(' a| letter a'),
            ('a', 'letter a')
        )


if __name__ == '__main__':
    unittest.main()
