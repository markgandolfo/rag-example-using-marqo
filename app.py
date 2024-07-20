import glob
import marqo
from document_loader import Documents
import marqo_helpers
import pprint

DOCS_DIR='./docs'
INDEX_NAME='markdown-notes-index'
DELETE_DOCUMENTS_IN_INDEX=True


mq = marqo.Client(url="http://localhost:8882")
marqo_helpers.find_or_create_index(mq, INDEX_NAME)

if DELETE_DOCUMENTS_IN_INDEX:
    marqo_helpers.delete_all_recreate_index(mq, INDEX_NAME)

document_len = len(glob.glob(DOCS_DIR + '/*.md'))
print('Number of documents found:', document_len)

# read in the documents
documents = Documents()
docs = documents.load(DOCS_DIR)

print('Number of documents:', len(docs))

docs_as_json_list = documents.as_json_list()

mq.index(INDEX_NAME).add_documents(
    docs_as_json_list,
    tensor_fields=["page_content"],
)
print("{mq.index(INDEX_NAME).get_stats()['numberOfDocuments']} documents indexed")


query = "Where is coffee made"


results = mq.index(INDEX_NAME).search(
    q = query,
    limit = 5,
    offset = 0,
    search_method = "LEXICAL",
)

print("Query 1:")
pprint.pprint(results)


