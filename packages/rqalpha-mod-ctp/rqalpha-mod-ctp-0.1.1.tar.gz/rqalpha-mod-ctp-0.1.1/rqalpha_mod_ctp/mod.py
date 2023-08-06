#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
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

import os
from rqalpha.interface import AbstractMod
from .ctp_event_source import CtpEventSource
from .ctp_broker import CtpBroker
from .ctp_data_source import CtpDataSource
from .ctp_price_board import CtpPriceBoard

from .ctp.gateway import CtpGateway
from .ctp.data_cache import DataCache


class CtpMod(AbstractMod):
    def __init__(self):
        self._env = None
        self._gateway = None

    def start_up(self, env, mod_config):
        self._env = env
        data_cache = DataCache()
        self._gateway = CtpGateway(env, data_cache,
                                   mod_config.temp_path, mod_config.CTP.userID, mod_config.CTP.password,
                                   mod_config.CTP.brokerID)
        self._gateway.init_td_api(mod_config.CTP.tdAddress)
        if mod_config.default_data_source:
            self._gateway.init_md_api(mod_config.CTP.mdAddress)
        self._gateway.connect_and_sync_data()
        self._env.set_broker(CtpBroker(self._gateway))
        self._env.set_event_source(CtpEventSource(env, mod_config, self._gateway))
        self._env.set_data_source(CtpDataSource(env, data_cache))
        self._env.set_price_board(CtpPriceBoard(data_cache))

    def tear_down(self, code, exception=None):
        self._gateway.exit()
