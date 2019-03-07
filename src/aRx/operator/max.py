# Internal
import typing as T
from abc import ABCMeta, abstractmethod

# Project
from ..disposable import CompositeDisposable
from ..misc.namespace import Namespace
from ..abstract.observer import Observer
from ..misc.dispose_sink import dispose_sink
from ..abstract.observable import Observable, observe
from ..stream.single_stream import SingleStream


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __gt__(self, other: T.Any) -> bool:
        ...


# Generic Types
K = T.TypeVar("K", bound=Comparable)
L = T.TypeVar("L", bound=T.AsyncContextManager[T.Any])


class _MaxSink(SingleStream[K]):
    _NOT_PROVIDED = object()

    def __init__(self, **kwargs: T.Any) -> None:
        super().__init__(**kwargs)
        self._max: K = T.cast(K, self._NOT_PROVIDED)
        self._namespace: T.Optional[Namespace] = None

    async def __asend__(self, value: K, namespace: Namespace) -> None:
        if self._max == self._NOT_PROVIDED or value > self._max:
            self._max = value
            self._namespace = namespace

    async def __aclose__(self) -> None:
        if self._max != self._NOT_PROVIDED:
            assert self._namespace is not None

            awaitable = super().__asend__(self._max, self._namespace)

            self._max = T.cast(K, self._NOT_PROVIDED)
            self._namespace = None

            await awaitable

        await super().__aclose__()


class Max(Observable[K, CompositeDisposable]):
    """Observable that outputs the largest data read from an observable source.

    .. Note::

        Data comparison is made using the ``>`` (grater than) operation.

    .. Warning::

        This observable only outputs data after source observable has closed.
    """

    def __init__(self, source: Observable[K, L], **kwargs: T.Any) -> None:
        """Max constructor.

        Arguments:
            source: Observable source.
            kwargs: Keyword parameters for super.
        """
        super().__init__(**kwargs)
        self._source = source

    def __observe__(self, observer: Observer[K, T.Any]) -> CompositeDisposable:
        sink: _MaxSink[K] = _MaxSink(loop=observer.loop)
        with dispose_sink(sink):
            return CompositeDisposable(observe(self._source, sink), observe(sink, observer))


def max_op() -> T.Type[Max[K]]:
    """Implementation of :class:`~.Max` to be used with operator semantics.

    Returns:
        Implementation of Max.

    """
    return Max


__all__ = ("Max", "max_op")
