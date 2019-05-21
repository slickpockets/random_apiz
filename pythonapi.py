import gnupg
import bottle
import re, json
import redis
from bottle import request, response
from bottle import post, get, put, delete
db = redis.Redis('localhost', 6379)



gpg = gnupg.GPG(binary='/usr/bin/gpg', homedir='./keys', keyring='pubring.gpg', secring='secring.gpg')
