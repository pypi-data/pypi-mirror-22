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

import six

from rqalpha.model.base_position import Positions
from rqalpha.model.order import Order
from rqalpha.const import SIDE, POSITION_EFFECT, ORDER_STATUS, ACCOUNT_TYPE

from .data_dict import FakeTickDict
from ..utils import margin_of


class DataCache(object):
    def __init__(self):
        self._ins_cache = {}
        self._future_info_cache = {}
        self._account_dict = None
        self._pos_cache = {}
        self._trade_cache = {}
        self._qry_order_cache = {}

        self._snapshot_cache = {}

        self._order_cache = {}

        self._account_model = None
        self._position_model = None

    def cache_ins(self, ins_cache):
        self._ins_cache = ins_cache
        self._future_info_cache = {ins_dict.underlying_symbol: {'speculation': {
                'long_margin_ratio': ins_dict.long_margin_ratio,
                'short_margin_ratio': ins_dict.short_margin_ratio,
                'margin_type': ins_dict.margin_type,
            }} for ins_dict in self._ins_cache.values()}

    def cache_commission(self, underlying_symbol, commission_dict):
        self._future_info_cache[underlying_symbol]['speculation'].update({
            'open_commission_ratio': commission_dict.open_ratio,
            'close_commission_ratio': commission_dict.close_ratio,
            'close_commission_today_ratio': commission_dict.close_today_ratio,
            'commission_type': commission_dict.commission_type,
        })

    def cache_position(self, pos_cache):
        self._pos_cache = pos_cache
        for order_book_id, pos_dict in six.iteritems(pos_cache):
            if order_book_id not in self._snapshot_cache:
                self._snapshot_cache[order_book_id] = FakeTickDict(pos_dict)

    def cache_account(self, account_dict):
        self._account_dict = account_dict

    def cache_qry_order(self, order_cache):
        self._qry_order_cache = order_cache

    def cache_snapshot(self, tick_dict):
        self._snapshot_cache[tick_dict.order_book_id] = tick_dict

    def cache_trade(self, trade_dict):
        if trade_dict.order_book_id not in self._trade_cache:
            self._trade_cache[trade_dict.order_book_id] = []
        self._trade_cache[trade_dict.order_book_id].append(trade_dict)

    def get_cached_order(self, order_dict):
        try:
            order = self._order_cache[order_dict.order_id]
        except KeyError:
            order = Order.__from_create__(order_dict.order_book_id, order_dict.quantity, order_dict.side, order_dict.style, order_dict.position_effect)
            self.cache_order(order)
        return order

    def cache_order(self, order):
        self._order_cache[order.order_id] = order

    @property
    def ins(self):
        return self._ins_cache

    @property
    def future_info(self):
        return self._future_info_cache

    @property
    def positions(self):
        PositionModel = self._position_model
        ps = Positions(PositionModel)
        for order_book_id, pos_dict in six.iteritems(self._pos_cache):
            position = PositionModel(order_book_id)

            position._buy_old_holding_list = [(pos_dict.prev_settle_price, pos_dict.buy_old_quantity)]
            position._sell_old_holding_list = [(pos_dict.prev_settle_price, pos_dict.sell_old_quantity)]

            position._buy_transaction_cost = pos_dict.buy_transaction_cost
            position._sell_transaction_cost = pos_dict.sell_transaction_cost
            position._buy_realized_pnl = pos_dict.buy_realized_pnl
            position._sell_realized_pnl = pos_dict.sell_realized_pnl

            position._buy_avg_open_price = pos_dict.buy_avg_open_price
            position._sell_avg_open_price = pos_dict.sell_avg_open_price

            if order_book_id in self._trade_cache:
                trades = sorted(self._trade_cache[order_book_id], key=lambda t: t.trade_id, reverse=True)

                buy_today_holding_list = []
                sell_today_holding_list = []
                for trade_dict in trades:
                    if trade_dict.side == SIDE.BUY and trade_dict.position_effect == POSITION_EFFECT.OPEN:
                        buy_today_holding_list.append((trade_dict.price, trade_dict.amount))
                    elif trade_dict.side == SIDE.SELL and trade_dict.position_effect == POSITION_EFFECT.OPEN:
                        sell_today_holding_list.append((trade_dict.price, trade_dict.amount))

                self.process_today_holding_list(pos_dict.buy_today_quantity, buy_today_holding_list)
                self.process_today_holding_list(pos_dict.sell_today_quantity, sell_today_holding_list)

                position._buy_today_holding_list = buy_today_holding_list
                position._sell_today_holding_list = sell_today_holding_list

            ps[order_book_id] = position
        return ps

    def process_today_holding_list(self, today_quantity, holding_list):
        # check if list is empty
        if not holding_list:
            return
        cum_quantity = sum(quantity for price, quantity in holding_list)
        left_quantity = cum_quantity - today_quantity
        while left_quantity > 0:
            oldest_price, oldest_quantity = holding_list.pop()
            if oldest_quantity > left_quantity:
                consumed_quantity = left_quantity
                holding_list.append(oldest_price, oldest_quantity - left_quantity)
            else:
                consumed_quantity = oldest_quantity
            left_quantity -= consumed_quantity

    @property
    def account(self):
        static_value = self._account_dict.yesterday_portfolio_value
        ps = self.positions
        realized_pnl = sum(position.realized_pnl for position in six.itervalues(ps))
        cost = sum(position.transaction_cost for position in six.itervalues(ps))
        margin = sum(position.margin for position in six.itervalues(ps))
        total_cash = static_value + realized_pnl - cost - margin

        AccountModel = self._account_model
        account = AccountModel(total_cash, ps)
        account._frozen_cash = sum(
            [margin_of(order_dict.order_book_id, order_dict.unfilled_quantity, order_dict.price) for order_dict in
             self._qry_order_cache.values() if order_dict.status == ORDER_STATUS.ACTIVE])
        return account, static_value

    @property
    def snapshot(self):
        return self._snapshot_cache

    def set_models(self, account_model, position_model):
        self._account_model = account_model
        self._position_model = position_model


class RQObjectCache(object):
    def __init__(self):
        self.orders = {}

    def cache_order(self, order):
        self.orders[order.order_id] = order
