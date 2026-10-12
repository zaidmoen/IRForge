from collections import defaultdict

from irforge.tokenizer import tokenize


class PositionalIndex:
    def __init__(self):
        self.postings = defaultdict(lambda: defaultdict(list))
        self.document_ids = []

    def build(self, documents):
        """Build the index from a mapping of document ids to text"""
        self.postings.clear()
        self.document_ids = list(documents.keys())

        for document_id, text in documents.items():
            # I am turning this document into words before I start indexing it
            words = tokenize(text)

            # I am keeping positions so I can check exact phrases later
            for position, word in enumerate(words, start=1):
                self.postings[word][document_id].append(position)

        return self

    def get_document_ids(self, word):
        # I am returning an empty list when this word is not in my index
        return list(self.postings.get(word, {}).keys())

    def search_and(self, words):
        # I am cleaning the query the same way I cleaned the documents
        query_words = tokenize(" ".join(words))

        if not query_words:
            return []

        # I am starting with documents that contain the first query word
        matching_documents = set(self.get_document_ids(query_words[0]))

        # I am keeping only documents that contain every query word
        for word in query_words[1:]:
            matching_documents.intersection_update(self.get_document_ids(word))

        # I am using the original document order to make the result predictable
        return [
            document_id
            for document_id in self.document_ids
            if document_id in matching_documents
        ]

    def search_phrase(self, phrase):
        # I am splitting the phrase into the words that must appear next to each other
        phrase_words = tokenize(phrase)

        if not phrase_words:
            return []

        # I am first finding documents that contain every word in the phrase
        candidate_documents = self.search_and(phrase_words)
        matching_documents = []

        for document_id in candidate_documents:
            # I am checking every place where the first phrase word appears
            first_word_positions = self.postings[phrase_words[0]][document_id]

            for start_position in first_word_positions:
                # I am checking whether each next word is in the next position
                phrase_matches = all(
                    start_position + offset
                    in self.postings[word].get(document_id, [])
                    for offset, word in enumerate(phrase_words[1:], start=1)
                )

                if phrase_matches:
                    matching_documents.append(document_id)
                    break

        return matching_documents
