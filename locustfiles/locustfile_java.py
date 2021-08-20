import json
import os
import random

from locust import HttpUser, task, between, tag
from locust.contrib.fasthttp import FastHttpUser


class LinkingTester(FastHttpUser):
    wait_time = between(5, 9)

    paragraphs = []
    pdf_documents = []
    text_documents = []

    @tag('process_pdfs')
    @task
    def classify_temperature(self):
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
        self.client.post(path="/service/process/pdf", data=files, headers=headers, name="/service/process/pdf")

    @tag('process_text')
    @task
    def process_text(self):
        n = random.randint(0, len(self.text_documents) - 1)
        text_document = self.text_documents[n]

        headers = {"Accept": "application/json"}
        files = {"text": text_document}
        self.client.post(path="/service/process/text", data=files, headers=headers, name="/service/process/text")

    @tag('process_json')
    @task
    def process_json(self):
        n = random.randint(0, len(self.paragraphs) - 1)
        paragraph = self.paragraphs[n]

        headers = {"Accept": "application/json"}
        files = {"input": json.dumps(paragraph)}
        self.client.post(path="/service/process/json", data=files, headers=headers, name="/service/process/json")


    def on_start(self):
        for root, dirs, files in os.walk("resources/data/pdfs/"):
            for file_ in files:
                if file_.lower().endswith(".pdf"):
                    abs_path = os.path.join(root, file_)
                    self.pdf_documents.add(abs_path)

        for root, dirs, files in os.walk("resources/data/texts/"):
            for file_ in files:
                if file_.lower().endswith(".txt"):
                    abs_path = os.path.join(root, file_)
                    self.text_documents.add(abs_path)

