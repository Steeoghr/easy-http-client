from abc import ABC, abstractmethod
import functools
from typing import Any, Callable
from lib.common.utility.generic import T

class BaseDecorator(ABC):
    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            if args and hasattr(args[0], func.__name__):
                # This is likely a method call, args[0] should be self or cls
                instance_or_class = args[0]
                other_args = args[1:]
            else:
                # This is likely a function call or static method
                instance_or_class = None
                other_args = args

            return self.execute(func, instance_or_class, *other_args, **kwargs)

        return wrapper

    @abstractmethod
    def execute(self, func: Callable[..., T], instance_or_class: Any, *args: Any, **kwargs: Any) -> T:
        """
        Abstract method to be implemented by subclasses.
        This is where the actual decorator logic should be implemented.

        :param func: The decorated function or method
        :param instance_or_class: The instance (self) for instance methods,
                                  the class for class methods, or None for functions and static methods
        :param args: Positional arguments passed to the decorated function/method
        :param kwargs: Keyword arguments passed to the decorated function/method
        :return: The result of the decorated function/method
        """
        pass

# Example implementation of a concrete decorator
class TimingDecorator(BaseDecorator):
    def execute(self, func: Callable[..., T], instance_or_class: Any, *args: Any, **kwargs: Any) -> T:
        import time
        start_time = time.time()
        result = func(instance_or_class, *args, **kwargs) if instance_or_class else func(*args, **kwargs)
        end_time = time.time()
        
        if instance_or_class:
            if isinstance(instance_or_class, type):
                print(f"Class method {func.__name__} of {instance_or_class.__name__} took {end_time - start_time:.4f} seconds")
            else:
                print(f"Method {func.__name__} of {instance_or_class.__class__.__name__} instance took {end_time - start_time:.4f} seconds")
        else:
            print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        
        return result

# Usage example
@TimingDecorator()
def test_function(x: int, y: int) -> int:
    import time
    time.sleep(1)
    return x + y

class TestClass:
    @TimingDecorator()
    def instance_method(self, x: int, y: int) -> int:
        import time
        time.sleep(1)
        return x + y


if __name__ == "__main__":
    obj = TestClass()
    print(obj.instance_method(2, 3))