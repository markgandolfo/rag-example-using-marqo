import os
import re
from datetime import datetime
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document as LangchainDocument

#
# Load markdown files from a directory and return them as a list of Document objects
#
class Documents:
    def __init__(self):
        self.documents = []

    def load(self, path):
        loader = MarkdownLoader(path)
        langchain_documents = loader.load()
        for doc in langchain_documents:
            doc = Document(
                page_content=doc.page_content,
                hashtags=doc.metadata['hashtags'],
                creation_date=doc.metadata['creation_date']
            )
            self.documents.append(doc)

        return self.documents

    def as_json_list(self):
        return list(map(lambda x: x.to_dict(), self.documents))


# 
# A simple class to represent a document
#
class Document:
    def __init__(self, page_content, hashtags, creation_date):
        self.page_content = page_content
        self.creation_date = creation_date
        self.hash_tags = hashtags

    def to_dict(self):
        return {
            'page_content': self.page_content,
            'creation_date': self.creation_date,
            'hash_tags': self.hash_tags
        }



#
# Load markdown files from a directory
# They're returned in LangchainDocument format
# 
class MarkdownLoader(DirectoryLoader):
    def __init__(self, path):
        super().__init__(path, glob="**/*.md", show_progress=True,  use_multithreading=False)

    def load(self):
        docs = super().load()
        processed_docs = []
        for doc in docs:
            content = doc.page_content
            metadata = doc.metadata
            creation_date = self.get_creation_date(metadata['source'])
            hashtags = self.extract_hashtags(content)

            new_content = f"Created: {creation_date}\nHashtags: {hashtags}\n\n{content}"
            new_metadata = {**metadata, 'creation_date': creation_date, 'hashtags': hashtags}

            processed_docs.append(LangchainDocument(page_content=new_content, metadata=new_metadata))

        return processed_docs

    def extract_hashtags(self, text):
        return ' '.join(re.findall(r'#\w+', text))

    def get_creation_date(self, file_path):
        return datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')

