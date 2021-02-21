import time
from datetime import datetime, timedelta
from typing import Dict, List

from binance.websockets import BinanceSocketManager, Client

from process_data import pandify_prices
from json_types import TradeInfo
import multiprocessing as mp
from threading import Thread
from queue import Queue, Empty

from plotting import get_line_plot


def get_symbol_store(symbols) -> Dict[str, List[TradeInfo]]:
    symbol_store: Dict[str, List[TradeInfo]] = dict()
    for symbol in symbols:
        symbol_store[symbol] = []
    return symbol_store


def clean_filter(x: TradeInfo):
    return datetime.now() < x.data.event_time + timedelta(minutes=10)


def clean_store(symbol_store: Dict[str, List[TradeInfo]]) -> Dict[str, List[TradeInfo]]:
    for k, v in symbol_store.items():
        symbol_store[k] = list(filter(clean_filter, symbol_store[k]))
    return symbol_store


def clean_store_for_symbol(trade_info: TradeInfo, symbol_store: Dict[str, List[TradeInfo]]) -> Dict[str, List[TradeInfo]]:
    symbol_store[trade_info.data.s] = list(filter(clean_filter, symbol_store[trade_info.data.s]))
    symbol_store[trade_info.data.s].append(trade_info)
    return symbol_store


def store_manager(symbols: List[str], q_to_store: Queue, q_request_from_store: mp.Queue, q_pipe_store_to_request: mp.Queue):
    symbol_store = get_symbol_store(symbols)
    last_garbage_clean = time.time()
    while True:
        try:
            trade: TradeInfo = q_to_store.get(block=False)
            symbol_store = clean_store_for_symbol(trade, symbol_store)
        except Empty:
            pass
        try:
            symbol = q_request_from_store.get(block=False)
            if symbol is not None:
                data_frame = pandify_prices(symbol_store[symbol])
                base_64 = get_line_plot(symbol, data_frame)
                q_pipe_store_to_request.put(base_64)
                # q_pipe_store_to_request.put({"data": [x.objectify() for x in symbol_store[symbol]]})
        except Empty:
            pass
        if time.time() - last_garbage_clean > 10:
            symbol_store = clean_store(symbol_store)
            last_garbage_clean = time.time()


def get_msg_processor(q_to_store: Queue):
    def process_m_message(msg):
        trade = TradeInfo(msg)
        q_to_store.put(trade)
    return process_m_message


def timed_data_cache(
        client: Client,
        symbol_with_ticker: List[str],
        symbols: List[str],
        queue_request_from_store: mp.Queue,
        queue_pipe_store_to_request: mp.Queue
):
    bm = BinanceSocketManager(client)
    queue_to_store = Queue()
    t = Thread(target=store_manager, args=(symbols, queue_to_store, queue_request_from_store, queue_pipe_store_to_request,))
    t.start()
    process_m_message = get_msg_processor(queue_to_store)
    # pass a list of stream names
    # noinspection PyTypeChecker
    bm.start_multiplex_socket(symbol_with_ticker, process_m_message)
    bm.start()




