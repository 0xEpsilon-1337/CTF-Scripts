#!/usr/bin/env python3
import os, sys
import subprocess
msg = input("message: ")

if len(msg) > 64:
    print("Too long (character limit 64)")
    sys.exit(0)


subprocess.run(["./chall"], input=msg.encode())
