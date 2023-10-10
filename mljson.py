import json
import logging
import sys

from utils import *


def ReturnJson(dict):
    print("Content-type: application/json")
    print
    print(json.dumps(dict))


def Return(dict):
    logging.debug(repr(dict))
    ReturnJson(dict)


def Error(str, dict=None):
    if not dict:
        dict = {}
    dict["error"] = str
    Return(dict)
    sys.exit(1)


def ReturnCode(code):
    dict = {}
    dict["code"] = code
    Return(dict)
    sys.exit(1)


def Message(str, dict=None):
    if not dict:
        dict = {}
    dict["message"] = str
    Return(dict)
