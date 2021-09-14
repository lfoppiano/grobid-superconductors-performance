import json
import os
import random

from locust import HttpUser, task, between, tag
from locust.contrib.fasthttp import FastHttpUser


class GrobidSuperconductorsTester(HttpUser):
    wait_time = between(5, 9)

    json_documents = []
    pdf_documents = []
    text_documents = []

    @tag('process_pdfs')
    @task
    def process_pdfs(self):
        n = random.randint(0, len(self.pdf_documents) - 1)
        pdf_document = self.pdf_documents[n]

        files = {
            'input': (
                pdf_document,
                open(pdf_document, 'rb'),
                'application/pdf',
                {'Expires': '0'}
            )
        }

        headers = {"Accept": "application/json"}
        self.client.post("/service/process/pdf", files=files, headers=headers, name="/service/process/pdf")

    @tag('process_text')
    @task
    def process_text(self):
        n = random.randint(0, len(self.text_documents) - 1)
        text_document = self.text_documents[n]

        headers = {"Accept": "application/json"}
        files = {"text": text_document}
        self.client.post("/service/process/text", files=files, headers=headers, name="/service/process/text")

    @tag('process_json')
    @task
    def process_json(self):
        n = random.randint(0, len(self.json_documents) - 1)
        paragraph = self.json_documents[n]

        headers = {"Accept": "application/json"}
        files = {"input": json.dumps(paragraph)}
        self.client.post(path="/service/process/json", data=files, headers=headers, name="/service/process/json")

    def on_start(self):
        if len(self.pdf_documents) == 0:
            # for root, dirs, files in os.walk("resources/data/pdfs/"):
            for root, dirs, files in os.walk("resources/data/dataset/superconductors/corpus/pdf/batches"):
                for file_ in files:
                    if file_.lower().endswith(".pdf"):
                        abs_path = os.path.join(root, file_)
                        self.pdf_documents.append(abs_path)

        if len(self.text_documents) == 0:
            for root, dirs, files in os.walk("resources/data/texts/"):
                for file_ in files:
                    if file_.lower().endswith(".txt"):
                        abs_path = os.path.join(root, file_)
                        with open(abs_path, 'r') as text_file:
                            for line in text_file:
                                self.text_documents.append(line.strip())

        if len(self.json_documents) == 0:
            for root, dirs, files in os.walk("resources/data/documents/"):
                for file_ in files:
                    if file_.lower().endswith(".json"):
                        abs_path = os.path.join(root, file_)
                        with open(abs_path, 'r') as text_file:
                            document = json.load(text_file)
                            self.json_documents.extend(document)
