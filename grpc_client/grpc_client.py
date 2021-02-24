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
"""The Python AsyncIO implementation of the GRPC user.UserInfo client."""

import logging
import asyncio
import grpc
import json
import glob
import os

import user_pb2
import user_pb2_grpc


def read_json(file_name):
    file_path = f"users/{file_name}"
    with open(file_path, "r") as json_file:
        return json.load(json_file)


async def run(file_name):
    grpc_server = os.environ["GRPC_SERVER"]
    async with grpc.aio.insecure_channel(f"{grpc_server}:50051", options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = user_pb2_grpc.UserInfoStub(channel)

        for d in read_json(file_name):
            response = await stub.SendUser(user_pb2.UserRequest(**d))
            print(response.message)


def main():
    file_names = glob.glob("*.json")
    for file_name in file_names:
        asyncio.run(run(file_name))


if __name__ == '__main__':
    logging.basicConfig()
    main()
