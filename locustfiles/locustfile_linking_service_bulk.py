import json
import os
import random

from locust import task, between, tag, constant
from locust.contrib.fasthttp import FastHttpUser


class LinkingTester(FastHttpUser):
    wait_time = between(1, 2)

    paragraphs = []
    formulas = []

    @tag('classify_formula')
    @task
    def classify_formula(self):
        n = random.randint(0, len(self.formulas) - 1)
        formula = self.formulas[n]

        headers = {"Accept": "application/json"}
        files = {"input": json.dumps(formula)}
        self.client.post(path="/classify/formula", data=files, headers=headers, name="/classify/formula")

    @tag('classify_temperature')
    @task
    def classify_temperature(self):
        sentences = []
        for x in range(0, random.randint(10, 150)):
            n = random.randint(0, len(self.paragraphs) - 1)
            sentences.append(self.paragraphs[n])

        headers = {"Accept": "application/json"}
        files = {"input": json.dumps(sentences)}
        self.client.post(path="/classify/tc", data=files, headers=headers, name="/classify/tc")

    @tag('process_links')
    @task
    def process_links(self):
        sentences = []
        for x in range(0, random.randint(10, 150)):
            n = random.randint(0, len(self.paragraphs) - 1)
            sentences.append(self.paragraphs[n])

        print(sentences)

        headers = {"Accept": "application/json"}
        files = {"input": json.dumps(sentences)}
        self.client.post(path="/process/link", data=files, headers=headers, name="/process/link")


    def on_start(self):
        # pydevd_pycharm.settrace('localhost', port=8999, stdoutToServer=True, stderrToServer=True)

        if len(self.paragraphs) == 0:
            print("Loading documents")
            for root, dirs, files in os.walk("resources/data/input/"):
                for file_ in files:
                    if not file_.lower().endswith(".json"):
                        continue
                    abs_path = os.path.join(root, file_)

                    with open(abs_path, 'r') as f:
                        sentences = json.load(f)
                        self.paragraphs.extend(sentences)

        if len(self.formulas) == 0:
            print("Loading formulas")
            with open("resources/data/formulas/materials.sorted.txt", 'r') as f:
                lines = f.readlines()
                self.formulas.extend(lines)

