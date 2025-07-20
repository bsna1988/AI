from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack.dataclasses import ChatMessage

generator = OllamaChatGenerator(model="zephyr:7b-alpha-q3_K_S",
                            url = "http://localhost:11434",
                            generation_kwargs={
                              "num_predict": 100,
                              "temperature": 0.9,
                              })

messages = [ChatMessage.from_system("\nYou are a helpful, respectful and honest assistant"),
ChatMessage.from_user("What's Natural Language Processing?")]

print(generator.run(messages=messages))