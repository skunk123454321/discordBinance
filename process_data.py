from datetime import datetime
from typing import List
import pandas as pd
from json_types import TradeInfo


def pandify_prices(trades: List[TradeInfo]):
    x: List[float] = []
    y: List[datetime] = []
    for trade in trades:
        x.append(float(trade.data.p))
        y.append(trade.data.event_time)
    val = pd.DataFrame({"time (EST)": y, "price": x})
    return val




