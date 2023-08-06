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
from time import sleep
from six import iteritems
from datetime import date
from Queue import Queue, Empty

from rqalpha.utils.logger import system_log
from rqalpha.const import ACCOUNT_TYPE, ORDER_STATUS
from rqalpha.environment import Environment
from rqalpha.events import EVENT
from rqalpha.events import Event as RqEvent
from rqalpha.model.order import Order
from rqalpha.model.trade import Trade
from rqalpha.model.portfolio import Portfolio

from .api import CtpTdApi, CtpMdApi
from ..utils import cal_commission


class CtpGateway(object):
    def __init__(self, env, data_cache, temp_path, user_id, password, broker_id, retry_times=5, retry_interval=1):
        self._env = env

        self.td_api = None
        self.md_api = None

        self.temp_path = temp_path
        self.user_id = user_id
        self.password = password
        self.broker_id = broker_id

        self._retry_times = retry_times
        self._retry_interval = retry_interval

        self._query_returns = {}
        self._tick_que = Queue()
        self._cache = data_cache

        self.subscribed = []
        self.open_orders = []
        self.order_objects = {}

        self._data_update_date = date.min

    def connect_and_sync_data(self):
        self._connect()
        self.on_log('同步数据中。')

        if self._data_update_date != date.today():
            self._qry_instrument()
            self._qry_account()
            self._qry_position()
            self._qry_order()
            self._data_update_date = date.today()
            self._qry_commission()

        self._subscribe_all()
        self.on_log('数据同步完成。')

        self._env.event_bus.add_listener(EVENT.POST_UNIVERSE_CHANGED, self.on_universe_changed)

    def init_md_api(self, md_address):
        self.md_api = CtpMdApi(self, self.temp_path, self.user_id, self.password, self.broker_id, md_address)
        self._query_returns[self.md_api.api_name] = {}

    def init_td_api(self, td_address, auth_code=None, user_production_info=None):
        self.td_api = CtpTdApi(self, self.temp_path, self.user_id, self.password, self.broker_id, td_address, auth_code, user_production_info)
        self._query_returns[self.td_api.api_name] = {}

    def submit_order(self, order):
        self.td_api.sendOrder(order)
        self._cache.cache_order(order)

    def cancel_order(self, order):
        account = Environment.get_instance().get_account(order.order_book_id)
        self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_PENDING_CANCEL, account=account, order=order))
        self.td_api.cancelOrder(order)

    def get_portfolio(self):
        future_account, static_value = self._cache.account
        start_date = self._env.config.base.start_date
        future_starting_cash = self._env.config.base.future_starting_cash
        return Portfolio(start_date, static_value/future_starting_cash, future_starting_cash, {ACCOUNT_TYPE.FUTURE: future_account})

    def get_ins_dict(self, order_book_id):
        return self._cache.ins.get(order_book_id)

    def get_tick(self):
        while True:
            try:
                return self._tick_que.get(block=True, timeout=1)
            except Empty:
                self.on_debug('Get tick timeout.')

    def exit(self):
        self.td_api.close()
        self.md_api.close()

    def on_universe_changed(self, event):
        self.subscribed = event.universe

    def on_query(self, api_name, n, result):
        self._query_returns[api_name][n] = result

    def on_debug(self, debug):
        system_log.debug(debug)

    def on_log(self, log):
        system_log.info(log)

    def on_err(self, error):
        system_log.error('CTP 错误，错误代码：%s，错误信息：%s' % (str(error['ErrorID']), error['ErrorMsg'].decode('GBK')))

    def on_order(self, order_dict):
        if not order_dict.is_valid:
            return
        self.on_debug('订单回报: %s' % str(order_dict))
        if self._data_update_date != date.today():
            return

        order = self._cache.get_cached_order(order_dict)

        account = Environment.get_instance().get_account(order.order_book_id)

        if order.status == ORDER_STATUS.PENDING_NEW:
            self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_PENDING_NEW, account=account, order=order))
            order.active()
            self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CREATION_PASS, account=account, order=order))
            if order_dict.status == ORDER_STATUS.ACTIVE:
                if order not in self.open_orders:
                    self.open_orders.append(order)
            elif order_dict.status in [ORDER_STATUS.CANCELLED, ORDER_STATUS.REJECTED]:
                order.mark_rejected('Order was rejected or cancelled.')
                self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_UNSOLICITED_UPDATE, account=account, order=order))
                if order in self.open_orders:
                    self.open_orders.remove(order)

            elif order_dict.status == ORDER_STATUS.FILLED:
                order._status = order_dict.status
                if order in self.open_orders:
                    self.open_orders.remove(order)

        elif order.status == ORDER_STATUS.ACTIVE:
            if order_dict.status == ORDER_STATUS.FILLED:
                order._status = order_dict.status
            if order_dict.status == ORDER_STATUS.CANCELLED:
                order.mark_cancelled("%d order has been cancelled." % order.order_id)
                self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CANCELLATION_PASS, account=account, order=order))
                if order in self.open_orders:
                    self.open_orders.remove(order)

        elif order.status == ORDER_STATUS.PENDING_CANCEL:
            if order_dict.status == ORDER_STATUS.CANCELLED:
                order.mark_cancelled("%d order has been cancelled." % order.order_id)
                self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CANCELLATION_PASS, account=account, order=order))
                if order in self.open_orders:
                    self.open_orders.remove(order)
            if order_dict.status == ORDER_STATUS.FILLED:
                order._status = order_dict.status
                if order in self.open_orders:
                    self.open_orders.remove(order)

    def on_trade(self, trade_dict):
        self.on_debug('交易回报: %s' % str(trade_dict))
        if self._data_update_date != date.today():
            self._cache.cache_trade(trade_dict)
        else:
            account = Environment.get_instance().get_account(trade_dict.order_book_id)

            if trade_dict.trade_id in account._backward_trade_set:
                return

            try:
                order = self.order_objects[trade_dict.order_id]
            except KeyError:
                order = Order.__from_create__(trade_dict.order_book_id,
                                              trade_dict.amount, trade_dict.side, trade_dict.style,
                                              trade_dict.position_effect)
            commission = cal_commission(trade_dict, order.position_effect)
            trade = Trade.__from_create__(
                trade_dict.order_id, trade_dict.price, trade_dict.amount,
                trade_dict.side, trade_dict.position_effect, trade_dict.order_book_id, trade_id=trade_dict.trade_id,
                commission=commission, frozen_price=trade_dict.price)

            order.fill(trade)
            self._env.event_bus.publish_event(RqEvent(EVENT.TRADE, account=account, trade=trade))

    def on_tick(self, tick_dict):
        if tick_dict.order_book_id in self.subscribed:
            self._tick_que.put(tick_dict)
        self._cache.cache_snapshot(tick_dict)

    def _connect(self):
        if self.md_api:
            for i in range(self._retry_times):
                self.md_api.connect()
                sleep(self._retry_interval * (i+1))
                if self.md_api.logged_in:
                    self.on_log('CTP 行情服务器登录成功')
                    break
            else:
                raise RuntimeError('CTP 行情服务器连接或登录超时')

        if self.td_api:
            for i in range(self._retry_times):
                self.td_api.connect()
                sleep(self._retry_interval * (i+1))
                if self.td_api.logged_in:
                    self.on_log('CTP 交易服务器登录成功')
                    break
            else:
                raise RuntimeError('CTP 交易服务器连接或登录超时')
        else:
            raise RuntimeError('CTP 交易服务器必须被初始化')

    def __qry_instrumnent(self):
        for i in range(self._retry_times):
            req_id = self.td_api.qryInstrument()
            sleep(self._retry_interval * (i+1))
            if req_id in self._query_returns[self.td_api.api_name]:
                ins_cache = self._query_returns[self.td_api.api_name][req_id].copy()
                del self._query_returns[self.td_api.api_name][req_id]
                self.on_debug('%d 条合约数据返回。' % len(ins_cache))
                return ins_cache
        else:
            raise RuntimeError('请求合约数据超时')

    def __qry_position(self):
        for i in range(self._retry_times):
            req_id = self.td_api.qryPosition()
            sleep(self._retry_interval * (i+1))
            if req_id in self._query_returns[self.td_api.api_name]:
                positions = self._query_returns[self.td_api.api_name][req_id].copy()
                del self._query_returns[self.td_api.api_name][req_id]
                self.on_debug('持仓数据返回: %s。' % str(positions.keys()))
                return positions

        # 持仓数据有可能不返回

    def __qry_account(self):
        for i in range(self._retry_times):
            req_id = self.td_api.qryAccount()
            sleep(self._retry_interval * (i+1))
            if req_id in self._query_returns[self.td_api.api_name]:
                account_dict = self._query_returns[self.td_api.api_name][req_id].copy()
                del self._query_returns[self.td_api.api_name][req_id]
                self.on_debug('账户数据返回: %s' % str(account_dict))
                return account_dict
        else:
            raise RuntimeError('请求账户数据超时')

    def __qry_commission(self, order_book_id):
        for i in range(self._retry_times):
            req_id = self.td_api.qryCommission(order_book_id)
            sleep(self._retry_interval * (i+1))
            if req_id in self._query_returns[self.td_api.api_name]:
                commission_dict = self._query_returns[self.td_api.api_name][req_id].copy()
                del self._query_returns[self.td_api.api_name][req_id]
                return commission_dict
        # commission 数据有可能不返回

    def __qry_order(self):
        for i in range(self._retry_times):
            req_id = self.td_api.qryOrder()
            sleep(self._retry_interval * (i+1))
            if req_id in self._query_returns[self.td_api.api_name]:
                order_dict = self._query_returns[self.td_api.api_name][req_id].copy()
                del self._query_returns[self.td_api.api_name][req_id]
                self.on_debug('订单数据返回')
                return order_dict
        # order 数据有可能不返回

    def __subscribe(self, order_book_id):
        if not self.md_api:
            raise NotImplementedError
        self.md_api.subscribe(order_book_id)

    def _qry_instrument(self):
        ins_cache = self.__qry_instrumnent()
        self._cache.cache_ins(ins_cache)

    def _qry_account(self):
        account_dict = self.__qry_account()
        self._cache.cache_account(account_dict)

    def _qry_position(self):
        positions = self.__qry_position()
        self._cache.cache_position(positions)

    def _qry_order(self):
        order_cache = self.__qry_order()
        for order_dict in order_cache.values():
            order = self._cache.get_cached_order(order_dict)
            if order_dict.status == ORDER_STATUS.ACTIVE:
                if order not in self.open_orders:
                    self.open_orders.append(order)
        self._cache.cache_qry_order(order_cache)

    def _qry_commission(self):
        for order_book_id, ins_dict in iteritems(self._cache.ins):
            if ins_dict.underlying_symbol in self._cache.future_info and 'commission_type' in self._cache.future_info[ins_dict.underlying_symbol]['speculation']:
                continue
            commission_dict = self.__qry_commission(order_book_id)
            self._cache.cache_commission(ins_dict.underlying_symbol, commission_dict)
        self.on_debug('费率数据返回')

    def _subscribe_all(self):
        for order_book_id in self._cache.ins.keys():
            self.__subscribe(order_book_id)
