import unittest

from irforge.index import PositionalIndex
from irforge.tokenizer import tokenize


class TokenizerTests(unittest.TestCase):
    def test_lowercase_and_punctuation_are_handled(self):
        self.assertEqual(tokenize("Hello, IR World!"), ["hello", "ir", "world"])


class PositionalIndexTests(unittest.TestCase):
    def setUp(self):
        self.documents = {
            "D1": "The database stores student records",
            "D2": "Students search the database for records",
            "D3": "The database stores course records",
            "D4": "Records database stores",
        }
        self.index = PositionalIndex().build(self.documents)

    def test_word_postings_keep_positions(self):
        self.assertEqual(self.index.postings["database"]["D1"], [2])
        self.assertEqual(self.index.postings["records"]["D2"], [6])

    def test_and_search_returns_documents_with_both_words(self):
        self.assertEqual(
            self.index.search_and(["database", "records"]),
            ["D1", "D2", "D3", "D4"],
        )

    def test_phrase_search_checks_word_order_and_positions(self):
        self.assertEqual(self.index.search_phrase("database stores"), ["D1", "D3", "D4"])
        self.assertEqual(self.index.search_phrase("database records"), [])

    def test_phrase_search_handles_repeated_words(self):
        repeated_word_index = PositionalIndex().build({"D1": "go go now"})
        self.assertEqual(repeated_word_index.search_phrase("go go"), ["D1"])


if __name__ == "__main__":
    unittest.main()
