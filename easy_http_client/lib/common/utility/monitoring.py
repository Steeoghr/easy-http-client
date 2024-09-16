from datetime import datetime, timedelta
from typing import Callable, Any

class ExecutionTimeTracker:
    def __init__(self, func: Callable):
        self.func = func
        self._start_time: datetime = None
        self._end_time: datetime = None
        self._execution_time: timedelta = None

    def execute(self, *args, **kwargs) -> Any:
        self._start_time = datetime.now()
        error = None
        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            error = e
        self._end_time = datetime.now()
        self._execution_time = self._end_time - self._start_time
        if error is not None:
            raise error
        return result

    @property
    def start_datetime(self) -> datetime:
        return self._start_time

    @property
    def end_datetime(self) -> datetime:
        return self._end_time

    @property
    def execution_timedelta(self) -> timedelta:
        return self._execution_time

    @property
    def execution_seconds(self) -> float:
        return self._execution_time.total_seconds() if self._execution_time else None

    def __str__(self) -> str:
        return (f"Function: {self.func.__name__}\n"
                f"Start time: {self.start_datetime}\n"
                f"End time: {self.end_datetime}\n"
                f"Execution time: {self.execution_timedelta}")