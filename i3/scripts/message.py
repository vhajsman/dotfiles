#!/usr/bin/env python3

import subprocess
from subprocess import check_output
import argparse
import os
import re

def createParser():
    def _default(name, default="", arg_type=str):
        val = default
        if name in os.environ:
            val = os.environ[name]

        return arg_type(val)

    strbool = lambda s: s.lower() in ["t", "true", "1"]

    parser = argparse.ArgumentParser(description="Check for package updates.")

    parser.add_argument("-c", "--check", default=_default("CHECK", "False", strbool))
    parser.add_argument("-s", "--set",   default=_default("SET"))
    parser.add_argument("-e", "--erase", default=_default("ERASE", "False", strbool))
    parser.add_argument("-u", "--user",  default=_default("USER"))

    return parser.parse_args()

args = createParser()

fn = ("/root/" if args.user == "root" else f"/home/{args.user}/") + ".message.rc"

def message_set(message):
    with open(fn, "w") as msgfile:
        msgfile.write(message)

def message_get():
    with open(fn, "r") as msgfile:
        return msgfile.read()


if args.check:
    message = message_get()

    if(message == "null"):
        print("")
        
        exit(0)
    
    print(message)
    exit(0)

if args.set:
    message_set(args.set)
    exit(0)

if args.erase:
    message_set("null")
    exit(0)

exit(1)
