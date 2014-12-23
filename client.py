#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import socket
import sys

from library.library import configuration_load
from library.library import configuration_save
from library.library import send_message


configuration_file = ""
configuration = {}


def converse(server, incoming_buffer, previous_command):
    global configuration

    if "\0" not in incoming_buffer:
        incoming_buffer += server.recv(4096)
        return converse(server, incoming_buffer, previous_command)
    else:
        index = incoming_buffer.index("\0")
        message = incoming_buffer[0:index-1]
        incoming_buffer = incoming_buffer[index+1:]
    # DEBUG
    print("message received:")
    print(message)
    print()

    lines = message.split('\n')
    fields = lines[0].split()
    command = fields[0]

    if command == 'WELCOME':
        id_ = fields[1]
        configuration["id"] = id_
        configuration_save(configuration_file, configuration)
        send_message(server, "OK\n\0")
        return incoming_buffer

    elif command == 'OK' and previous_command in ("LIST", "NAME"):
        return incoming_buffer

    else:
        # TODO
        # handle invalid commands
        print("error, invalid command")
        sys.exit(-1)


def connection_init(address):
    ip, port = address

    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('error, socket.socket')
        sys.exit(-1)

    # TODO
    # replace with the equivalent code without using an offset
    while True:
        try:
            connection.connect( (ip, port) )
            # DEBUG
            print("connected to server {}:{}".format(ip, port))
            print()
            break
        except socket.error:
            # DEBUG
            print("failed to connect to port {}, trying the next one".format(port))
            port += 1

    return connection


def get_name(configuration_file, configuration):
    print('Specify a user name (press enter for default "{}"): '.format(configuration["id"]))
    name = raw_input()

    if name == "":
        name = configuration["id"]

    configuration['name'] = name
    configuration_save(configuration_file, configuration)


def client():
    global configuration

    # check if an argument was passed
    if len(sys.argv) < 2:
        print("please pass one of the following arguments: {1, 2, 3}")
        sys.exit(-1)

    argument = sys.argv[1]

    configuration = {}

    working_directory = argument

    global configuration_file
    configuration_file = working_directory + "/configuration.json"

    if os.path.isfile(configuration_file):
        configuration = configuration_load(configuration_file)
    else:
        configuration["server_host"] = "localhost"
        configuration["server_port"] = 5000
        configuration["listening_port"] = 10000 + (int(argument) * 1000)
        configuration["id"] = "-"
        configuration["share_directory"] = "share"
        configuration_save(configuration_file, configuration)
    # DEBUG
    print("configuration:")
    print(configuration)
    print()

    share_directory = working_directory + "/" + configuration["share_directory"]
    files_list = [ file_ for file_ in os.listdir(share_directory) if os.path.isfile(os.path.join(share_directory, file_)) ]
    # DEBUG
    print("files_list:")
    print(files_list)
    print()

    server_address = (configuration["server_host"], configuration["server_port"])
    server = connection_init(server_address)


    # start with an empty incoming message buffer
    incoming_buffer = ""


    # send HEY command
    ############################################################################
    send_message(server, "HEY " + configuration["id"] + "\n\0")

    incoming_buffer = converse(server, incoming_buffer, "HEY")


    # send LIST command
    ############################################################################
    list_message = "LIST {}\n".format(len(files_list))
    for file_ in files_list:
        list_message += file_ + '\n'
    list_message += '\0'
    send_message(server, list_message)

    converse(server, incoming_buffer, "LIST")


    # send NAME command
    ############################################################################
    if "name" not in configuration:
        get_name(configuration_file, configuration)
    send_message(server, "NAME " + configuration["name"] + "\n\0")

    converse(server, incoming_buffer, "NAME")

     # send SENDLIST command
    ############################################################################
    print('If you want the list of files type: "SENDLIST" , else type "QUIT".): ')

    while True:
        ask_list = raw_input()
        if ask_list == 'SENDLIST':
            send_message(server, "SENDLIST " + "\n\0")
            break
        elif ask_list == 'QUIT':
            break
        else:
            print('Wrong command!!! Try again.')


    print("conversation successful")


if __name__ == "__main__":
    client()
