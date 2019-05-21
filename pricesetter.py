from tornado import ioloop
from tornado.web import *
from tornado.options import define, options
from tornado import httpserver
import redis
import requests, json, time, datetime
from string import Template

db = redis.Redis('localhost', 6379)

            class ApiHandler(RequestHandler):
    def initialize(self, db):
        self.db = db


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000")
        self.set_header("Access-Control-Allow-Headers", "X-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    json_data = None
    def get(self, id):
        self.timestamp = int(db.get("timestamp"))
        self.
