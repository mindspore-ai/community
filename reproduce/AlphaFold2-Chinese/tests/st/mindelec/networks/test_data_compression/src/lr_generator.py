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
# ============================================================================
"""learning rate generator"""


def step_lr_generator(step_size, epochs, lr, lr_decay_milestones):
    """generate step decayed learnig rate"""

    total_steps = epochs * step_size

    milestones = [int(total_steps * i / lr_decay_milestones) for i in range(1, lr_decay_milestones)]
    milestones.append(total_steps)
    learning_rates = [lr*0.5**i for i in range(0, lr_decay_milestones - 1)]
    learning_rates.append(lr*0.5**(lr_decay_milestones - 1))

    print("total_steps: %s, milestones: %s, learning_rates: %s " %(total_steps, milestones, learning_rates))

    return milestones, learning_rates
