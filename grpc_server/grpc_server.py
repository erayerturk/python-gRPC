#!/usr/bin/env python
# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC user.UserInfo server."""



import logging
import asyncio
import grpc
import json
import time
import glob
import os

import redis
from rq import Queue

from task_bg import enqueue_json

import user_pb2
import user_pb2_grpc


r = redis.Redis(host=os.environ["REDIS_HOST"])
q = Queue(connection=r)


class UserInfo(user_pb2_grpc.UserInfoServicer):

    async def SendUser(self, request: user_pb2.UserRequest, 
                       context: grpc.aio.ServicerContext) -> user_pb2.UserReply:

        information = {'id': request.id, 
                        'first_name': request.first_name, 
                        'last_name': request.last_name,
                        'email': request.email,
                        'gender': request.gender,
                        'ip_address': request.ip_address,
                        'user_name': request.user_name,
                        'agent': request.agent,
                        'country': request.country}

        job = q.enqueue(enqueue_json, information)

        return user_pb2.UserReply(message=f"Added {request.id} {request.first_name}.")


async def serve():
    server = grpc.aio.server()
    user_pb2_grpc.add_UserInfoServicer_to_server(UserInfo(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    q.empty()
    asyncio.run(serve())
