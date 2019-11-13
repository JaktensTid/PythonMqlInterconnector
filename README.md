Python - MQL5 Meta Trader 5 simple-to-use connector via Named Pipes

**Features:**
Allows to pass double arrays and candles into python script and strings back to MQL5 program

Python usage

```
import typing
import PythonMqlInterconnector

class EventHandler(PythonMqlInterconnector.Mql5EventHandler):
    def on_float_array(self, float_array: typing.List[float]) -> str:
        # do some job
        return 'This will be passed back to MQL5!'
        
    def on_candles(candles: typing.List[Mql5Candle]) -> str:
        # do some job
        return 'This will be passed back to MQL5!'
        

connector = PythonMqlInterconnector.Mql5Connector(symbol='AAPL', 
                                                    terminal_id='id',
                                                    event_handler=EventHandler())
connector.start()
```

MQL5 usage

**To be added**