#!/bin/bash
# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
set -e

SCRIPT_BASEDIR=$(realpath "$(dirname "$0")")
PROJECT_DIR=$(realpath "$SCRIPT_BASEDIR/../../")

if [ $# -gt 0 ]; then
  if  [ $1 == "mindelec" ]; then
    export PYTHONPATH=$PYTHONPATH:${PROJECT_DIR}/MindElec/
    echo "export PYTHONPATH=$PYTHONPATH"
    echo "Run ut mindelec."
    cd "$PROJECT_DIR" || exit
    UT_PATH="$PROJECT_DIR/tests/ut/mindelec/"
    pytest "$UT_PATH"
    echo "Test all mindelec use cases success."
  elif [ $1 == "mindsponge" ]; then
    echo "Run ut mindsponge."
    cd "$PROJECT_DIR" || exit
    UT_PATH="$PROJECT_DIR/tests/ut/mindsponge/"
    pytest "$UT_PATH"
    echo "Test all mindsponge use cases success."
  fi
else
  export PYTHONPATH=$PYTHONPATH:${PROJECT_DIR}/MindElec/
  echo "export PYTHONPATH=$PYTHONPATH"
  echo "Run all ut."
  cd "$PROJECT_DIR" || exit
  UT_PATH="$PROJECT_DIR/tests/ut/"
  pytest "$UT_PATH"
  echo "Test all use cases success."
  fi