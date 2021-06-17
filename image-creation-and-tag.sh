# Copyright 2021 valerio
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

#!/bin/bash

export VERSION=0.1.2

#DATABASES

docker build -t valeriovinciarelli/rendezvous-auth-database:$VERSION ./databases/auth-database/.
docker push valeriovinciarelli/rendezvous-auth-database:$VERSION
docker build -t valeriovinciarelli/rendezvous-roomrouter-database:$VERSION ./databases/roomrouter-database/.
docker push valeriovinciarelli/rendezvous-roomrouter-database:$VERSION
docker build -t valeriovinciarelli/rendezvous-chatroom-database:$VERSION ./databases/chatroom-database/.
docker push valeriovinciarelli/rendezvous-chatroom-database:$VERSION

# MICROSERVICES

docker build -t valeriovinciarelli/rendezvous-auth:$VERSION ./rendezvous-auth-ms/.
docker push valeriovinciarelli/rendezvous-auth:$VERSION
docker build -t valeriovinciarelli/rendezvous-chatroom:$VERSION ./rendezvous-chatroom-ms/.
docker push valeriovinciarelli/rendezvous-chatroom:$VERSION
docker build -t valeriovinciarelli/rendezvous-roomrouter:$VERSION ./rendezvous-roomrouter-ms/.
docker push valeriovinciarelli/rendezvous-roomrouter:$VERSION
docker build -t valeriovinciarelli/rendezvous-ui:$VERSION ./rendezvous-ui/.
docker push valeriovinciarelli/rendezvous-ui:$VERSION