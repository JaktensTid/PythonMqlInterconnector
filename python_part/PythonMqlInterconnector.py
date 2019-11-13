import win32file
import win32pipe
from typing import List


class Mql5Candle:
    def __init__(self, high, low, o, close, volume, time):
        self.high = high
        self.low = low
        self.open = o
        self.close = close
        self.volume = volume
        self.time = time

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return not self.__eq__(other)


class Mql5EventHandler:
    def on_float_array(self, float_array: List[float]) -> str:
        pass

    def on_candles(self, candles: List[Mql5Candle]) -> str:
        pass


class Mql5Connector:
    _stopped = False

    def __init__(self, terminal_id: str, symbol: str, event_handler: Mql5EventHandler):
        self._event_handler = event_handler
        self._symbol = symbol
        self._pipe = None
        self._terminal_id = terminal_id

    def stop(self):
        self._stopped = True
        win32file.CloseHandle(self._pipe)

    def start(self):
        self._stopped = False
        self._pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe' + '\\' + self._symbol + self._terminal_id,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        win32pipe.ConnectNamedPipe(self._pipe, None)
        buffer = []
        flag = ''
        while not self._stopped:
            data = win32file.ReadFile(self._pipe, 1024)
            data = data[1].decode('utf-8')
            if data == '~~d' or data == '~~c':
                flag = data
                buffer.clear()
            elif data == '~~close':
                if flag == '~~d':
                    result = self._event_handler.on_float_array([float(c) for c in buffer])
                if flag == '~~c':
                    candles = []
                    for high, low, open, close, volume, time in [[float(e) for e in c.split('|')] for c in buffer]:
                        candles.append(Mql5Candle(high, low, open, close, volume, time))
                    result = self._event_handler.on_candles(candles)
                if result:
                    win32file.WriteFile(self._pipe, str.encode(result))
            else:
                buffer.append(data)
