#!/usr/bin/python

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


MYSQL_USERNAME=os.environ.get("MYSQL_USERNAME")
MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD")
MYSQL_IP=os.environ.get("MYSQL_IP")
ROUTER_USERNAME=os.environ.get("ROUTER_USERNAME")
ROUTER_PASSWORD=os.environ.get("ROUTER_PASSWORD")
ROUTER_IP=os.environ.get("ROUTER_IP")
HTTP_ID=os.environ.get("HTTP_ID")
REDIS_HOST = os.environ.get("REDIS_HOST")