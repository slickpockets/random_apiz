from hashlib import sha512
import time
import redis
import re, json
import requests
from bottle import Bottle, request, response, hook, run
from bottle import post, get, put, delete

db = redis.Redis("localhost", 6379)
sha512 = sha512()

app = Bottle()
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    
@app.route('/hashyeah', method=['OPTIONS', 'POST'])
def handlehash():
    response.content_type = 'applicantion/json'
    items = ''
    if request.method == 'OPTIONS':
        return {}
    else:
        o = json.load(request.body)
        order = o["order"]
        for item in order:
            items = items + item

        timestamp = str(int(time.time()))
        ordernumber = db.get("ordernumber")
        db.incr("ordernumber")
        sha512.update(timestamp + items)
        hex512 = sha512.hexdigest()
        db.hmset("order:%s" % ordernumber, {"ordernumber": ordernumber, "items": items, "hashurl": hex512, "timestamp": timestamp})
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(ordernumber + "/" + hex512)
    

@get('/status/<ordernumber>/<orderhash>')
def show_order(ordernumber, orderhash):
    pass




if __name__ == '__main__':
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("--host", dest="host", default="localhost",
                          help="hostname or ip address", metavar="host")
        parser.add_option("--port", dest="port", default=6969,
                          help="port number", metavar="port")
        (options, args) = parser.parse_args()
        run(app, host=options.host, port=int(options.port), debug=True)
