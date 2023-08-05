import warnings
import inspect
from functools import wraps
from time import monotonic


# TODO: collect events from all Steps and combine when possible, only flush
# after some time
class Steps:
    def __init__(self):
        self._stack = []
        self._subscribers = []

    def get_current(self):
        return self._stack[-1] if self._stack else None

    def get_new(self, title):
        step = Step(title, level=len(self._stack) + 1)
        return step

    def push(self, step):
        assert step not in self._stack
        self._stack.append(step)
        step.parent = self.get_current()
        step.level = len(self._stack)

    def pop(self, step):
        assert self._stack[-1] is step
        self._stack.pop()

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def notify(self, event):
        # TODO: buffer and try to merge consecutive events
        for subscriber in self._subscribers:
            subscriber(event)

steps = Steps()


class StepEvent:
    def __init__(self, step, data, *, resource=None, stream=False):
        self.ts = monotonic()  # used to keep track of the events age
        self.step = step
        self.data = data
        self.resource = resource
        self.stream = stream

    def __str__(self):
        result = [str(self.step)]
        if self.resource:
            result.append(self.resource.__class__.__name__)
        result.append(", ".join(
            "{}={}".format(k, repr(v)) for k, v in self.data.items() if v is not None
        ))
        return " ".join(result)

    def _invalidate(self):
        self.ts = None
        self.step = None
        self.data = None
        self.resource = resource
        self.stream = None

    def merge(self, other):
        if not self.stream and not other.stream:
            return False
        if self.ts > other.ts:
            return False
        if self.resource is not other.resource:
            return False
        if self.data.keys() != other.data.keys():
            return False
        for k, v in other.data:
            self.data[k] += v
        other._invalidate()
        return True

    @property
    def age(self):
        return monotonic() - self.ts


# TODO: allow attaching log information, using a Resource as meta-data
class Step:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.args = None
        self.result = None
        self._start_ts = None
        self._stop_ts = None
        self._skipped = False

    def __repr__(self):
        result = [
            "Step(title={!r}, level={}, status={}".format(
                self.title,
                self.level,
                self.status,
            )
        ]
        if self.args is not None:
            result.append(", args={}".format(self.args))
        if self.result is not None:
            result.append(", result={}".format(self.result))
        duration = self.duration
        if duration >= 0.001:
            result.append(", duration={:.3f}".format(duration))
        result.append(")")
        return "".join(result)

    def __str__(self):
        return "{}".format(self.title)

    @property
    def duration(self):
        if self._start_ts is None:
            return 0.0
        elif self._stop_ts is None:
            return monotonic() - self._start_ts
        else:
            return self._stop_ts - self._start_ts

    @property
    def status(self):
        if self._start_ts is None:
            return 'new'
        elif self._stop_ts is None:
            return 'active'
        else:
            return 'done'

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_done(self):
        return self.status == 'done'

    def _notify(self, event: StepEvent):
        assert event.step is self
        steps.notify(event)

    def start(self):
        assert self._start_ts is None
        self._start_ts = monotonic()
        steps.push(self)
        self._notify(StepEvent(self, {
            'state': 'start',
            'args': self.args,
        }))

    def skip(self, reason):
        assert self._start_ts is not None
        self._notify(StepEvent(self, {'skip': reason}))

    def stop(self):
        assert self._start_ts is not None
        assert self._stop_ts is None
        self._stop_ts = monotonic()
        # TODO: report duration
        self._notify(StepEvent(self, {
            'state': 'stop',
            'result': self.result,
        }))
        steps.pop(self)

    def __del__(self):
        if not self.is_done:
            warnings.warn("__del__ called before {} was done".format(step))


def step(*, title=None, args=[], result=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*_args, **_kwargs):
            if title is None:
                step = steps.get_new(func.__name__)
            else:
                step = steps.get_new(title)
            # optionally pass the step object
            if 'step' in inspect.signature(func).parameters:
                _kwargs['step'] = step
            if args:
                captured = inspect.getcallargs(func, *_args, **_kwargs)
                step.args = {k: captured[k] for k in args}
            step.start()
            try:
                _result = func(*_args, **_kwargs)
                if result:
                    step.result = _result
            finally:
                step.stop()
            return _result

        return wrapper

    return decorator
