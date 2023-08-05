#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests

class AkinatorError(Exception):
    pass

class Akinator(object):
    URL = "http://api-fr2.akinator.com/ws/"
    def __init__(self):
        self.step = 0
        self.question = None
        self.progression = 0
        self.name = None
        self.description = None
        self.image = None
        self.session, self.signature = self.init_session()

    def requests(self, path, method="GET", params=None, data=None):
        try:
            return requests.request(method, "%s%s" % (self.URL, path), params=params, data=data).json()
        except requests.RequestException as err:
            return None

    def init_session(self):
        res = self.requests("new_session", params={"partner": 1})
        if not res:
            return None, None

        ident = res.get("parameters", {}).get("identification", {})
        self.parse_response(res.get("parameters", {}).get("step_information", {}))
        return ident.get("session"), ident.get("signature")

    def parse_response(self, step_info):
        self.question = step_info.get("question")
        if not self.question:
            raise AkinatorError()

        self.question = self.question
        self.step = int(step_info.get("step"))
        self.progression = float(step_info.get("progression", "0.0"))

    def answer(self, answer):
        params = {"session": self.session, "signature": self.signature, "step": self.step, "answer": answer}
        res = self.requests("answer", params=params)
        if not res:
            return None
        self.parse_response(res.get("parameters", {}))

    def result(self):
        params = {"session": self.session, "signature": self.signature, "step": self.step}
        res = self.requests("list", params=params)
        result = res.get("parameters", {}).get("elements", [])[0].get("element", {})
        self.name = result.get("name", "")
        self.description = result.get("description", "")
        self.image = result.get("absolute_picture_path", "")

def main():
    akinator = Akinator()
    while akinator.progression < 99:
        print(akinator.question)
        akinator.answer(1)

    akinator.result()
    print(akinator.name, akinator.description)

if __name__ == "__main__":
    main()
