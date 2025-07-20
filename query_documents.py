import os
from haystack import Pipeline
from dotenv import load_dotenv
from document_store_es import document_store
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever
load_dotenv()

# Get the base URL, space key, username, and API token from environment variables
os.environ["HF_API_TOKEN"] = os.getenv('HF_API_TOKEN')

from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator


template = [
    ChatMessage.from_user(
        """
Answer the questions based on the given context.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ question }}
Answer:
"""
    )
]
generator = OllamaChatGenerator(model="zephyr",
                            url = "http://localhost:11434",
                            generation_kwargs={
                              "temperature": 0.9,
                              })

pipe = Pipeline()
pipe.add_component("embedder", SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"))
pipe.add_component("retriever", ElasticsearchEmbeddingRetriever(document_store=document_store))
pipe.add_component("chat_prompt_builder", ChatPromptBuilder(template=template))
pipe.add_component("llm", generator)

pipe.connect("embedder.embedding", "retriever.query_embedding")
pipe.connect("retriever", "chat_prompt_builder.documents")
pipe.connect("chat_prompt_builder.prompt", "llm.messages")

question = (
    "How can I endorse my?"
)

pipe.run({"embedder": {"text": question}, "chat_prompt_builder": {"question": question}})
