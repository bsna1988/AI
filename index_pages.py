from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument, HTMLToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from pathlib import Path
from document_store_es import document_store

# You’ll need a different file converter class for each file type in our data sources: .pdf, .txt, and .md in this case. 
# Our FileTypeRouter connects each file type to the proper converter.
# Once all our files have been converted to Haystack Documents, we can use the DocumentJoiner component to make these a 
# single list of documents that can be fed through the rest of the indexing pipeline all together.

file_type_router = FileTypeRouter(mime_types=["text/plain", "application/pdf", "text/markdown", "text/html"])
text_file_converter = TextFileToDocument()
markdown_converter = MarkdownToDocument()
pdf_converter = PyPDFToDocument()
html_converter = HTMLToDocument()
document_joiner = DocumentJoiner()

# From there, the steps to this indexing pipeline are a bit more standard. The DocumentCleaner removes whitespace.
# Then this DocumentSplitter breaks them into chunks of 150 words, with a bit of overlap to avoid missing context.
document_cleaner = DocumentCleaner()
document_splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=50)

# Now you’ll add a SentenceTransformersDocumentEmbedder to create embeddings from the documents. 
document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

# Finally, you’ll use a DocumentWriter to write the documents to an InMemoryDocumentStore.
document_writer = DocumentWriter(document_store)
# Now you can put all these components together in a Pipeline.
preprocessing_pipeline = Pipeline()
preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
preprocessing_pipeline.add_component(instance=html_converter, name="html_converter")
preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")
# Next, connect them 
preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")
preprocessing_pipeline.connect("file_type_router.text/html", "html_converter.sources")
preprocessing_pipeline.connect("text_file_converter", "document_joiner")
preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
preprocessing_pipeline.connect("markdown_converter", "document_joiner")
preprocessing_pipeline.connect("document_joiner", "document_cleaner")
preprocessing_pipeline.connect("document_cleaner", "document_splitter")
preprocessing_pipeline.connect("document_splitter", "document_embedder")
preprocessing_pipeline.connect("document_embedder", "document_writer")



# This pipeline will take a list of file paths, convert them to Haystack Documents, clean and split them,
# create embeddings, and write them to the InMemoryDocumentStore.
def index_files(file_paths):
    """
    Index a list of files using the defined Haystack pipeline.
    
    :param file_paths: List of file paths to index.
    """

    for path in file_paths:
        preprocessing_pipeline.run({"file_type_router": {"sources": list(Path(path).glob("**/*"))}})


if __name__ == "__main__":
    # List of file paths to index
    file_paths = [
        "confluence_pages/*",
    ]
    
    # Index the files
    index_files(file_paths)
    print("Indexing completed.")