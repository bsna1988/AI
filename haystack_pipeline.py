"""
title: Haystack Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Haystack library.
requirements: haystack-ai, datasets>=2.6.1, sentence-transformers>=2.2.0
"""

from typing import List, Union, Generator, Iterator
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore

class Pipeline:
    def __init__(self):
        self.pipeline = None

    async def on_startup(self):
        document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")
        from haystack import Pipeline
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

        generator = OllamaChatGenerator(model="zephyr:7b-alpha-q3_K_S",
                                    url = "http://localhost:11434",
                                    generation_kwargs={
                                    "num_predict": 100,
                                    "temperature": 0.9,
                                    })

        self.pipeline = Pipeline()
        self.pipeline.add_component("embedder", SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"))
        self.pipeline.add_component("retriever", ElasticsearchEmbeddingRetriever(document_store=document_store))
        self.pipeline.add_component("chat_prompt_builder", ChatPromptBuilder(template=template))
        self.pipeline.add_component( "llm",generator)

        self.pipeline.connect("embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever", "chat_prompt_builder.documents")
        self.pipeline.connect("chat_prompt_builder.prompt", "llm.messages")

        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.

        print(messages)
        print(user_message)

        question = user_message
        response = self.pipeline.run(
          {"embedder": {"text": question}, "chat_prompt_builder": {"question": question}}
        )

        return response["llm"]["replies"][0]
