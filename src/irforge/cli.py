from pathlib import Path

from irforge.index import PositionalIndex


def load_documents():
    # I am loading the small example files that come with this project
    project_root = Path(__file__).resolve().parents[2]
    documents_folder = project_root / "data" / "sample_docs"
    documents = {}

    for document_path in sorted(documents_folder.glob("*.txt")):
        documents[document_path.stem.upper()] = document_path.read_text(
            encoding="utf-8"
        )

    return documents


def show_index(index):
    print("\nCurrent inverted index")

    for word in sorted(index.postings):
        document_parts = []

        for document_id, positions in index.postings[word].items():
            positions_text = ", ".join(str(position) for position in positions)
            document_parts.append(f"{document_id}:[{positions_text}]")

        print(f"{word} -> " + "  ".join(document_parts))


def main():
    documents = load_documents()
    index = PositionalIndex().build(documents)

    print("IRForge search demo")
    print("Type words with AND between them for a Boolean search")
    print('Put a phrase in double quotes for a phrase search')
    print("Type :index to inspect the positional index")
    print("Type :quit to close the program")

    while True:
        query = input("\nSearch> ").strip()

        if query.lower() == ":quit":
            print("See you next time")
            break

        if query.lower() == ":index":
            show_index(index)
            continue

        if len(query) >= 2 and query.startswith('"') and query.endswith('"'):
            results = index.search_phrase(query[1:-1])
            search_type = "Phrase results"
        else:
            query_words = query.replace("AND", "and").split("and")
            results = index.search_and(query_words)
            search_type = "Boolean AND results"

        print(f"{search_type}: {', '.join(results) if results else 'No matches'}")
