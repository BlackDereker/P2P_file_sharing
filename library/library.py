#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import sys
import logging
import json
import socket


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] (%(threadName)s) %(message)s")


def send_message(connection, message):
    try:
        connection.sendall(message)
    except socket.error:
        logging.error("error, send_message")
        sys.exit(-1)

    logging.debug("message sent: " + message)


def json_load(json_file):
    with open(json_file, "rb") as file_:
        json_ = json.load(file_)

    return json_


def json_save(json_file, json_):
    with open(json_file, "wb+") as file_:
        json.dump(json_, file_, sort_keys=True, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    print("This file is meant to be imported, not run.")
