# Copyright 2020 Huawei Technologies Co., Ltd
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
# ============================================================================
"""client script for serving mode"""

import time

from mindspore_serving.client import Client
from fold_service.config import config as serving_config

if __name__ == "__main__":

    client = Client("127.0.0.1:" + str(serving_config.port), "fold_service", "folding")
    instances = [{"input_fasta_path": serving_config.input_fasta_path}]

    print("inferring...")
    t1 = time.time()
    result = client.infer(instances)
    t2 = time.time()
    print("finish inferring! Time costed:", t2 - t1)
    print(result)
