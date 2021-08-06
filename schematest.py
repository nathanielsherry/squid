#!/usr/bin/python3

from squid import builder
config = builder.load("./example.yaml")
root = config['display']
w = builder.build(root)

