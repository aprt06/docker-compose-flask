# Copyright 2018 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import socket

from flask import Flask
from redis import Redis
from flask_executor import Executor
from flask_shell2http import Shell2HTTP


app = Flask(__name__)
executor = Executor(app)

redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello Container World! I have been seen %s times and my hostname is %s.\n' % (redis.get('hits'),socket.gethostname())


shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/commands/")

def my_callback_fn(context, future):
  # optional user-defined callback function
  print(context, future.result())

def compose_callback(context,future):
  print(context, future.result())

shell2http.register_command(endpoint="saythis", command_name="echo", callback_fn=my_callback_fn, decorators=[])
shell2http.register_command(endpoint="generate", command_name="docker-compose", callback_fn=newfile_callback, decorators=[])