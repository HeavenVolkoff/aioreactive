"""Operators Module

The aRx operators are special observables that can be applied to other
observables in order to transform them. The resulting observables can be streamed
to an observers as normal.

```python
Observable | Operator | Operator | Operator > Observer
```

.. note::
    Binary OR ``|`` is used to apply operators to observables.

    Greater than ``>`` is used to subscribe observers to observables.

Example using operators to filter odd numbers from a Iterable source.

```python
from aRx import observables, operators as op
from aRx.observers import AnonymousObserver

async def run() -> None:
    # Observer that will print all data that passes through it
    await (
        observables.FromIterable(range(100)) | op.Filter(lambda x: bool(x % 2))
        > AnonymousObserver(asend=lambda x, _: print(x))
    )
```

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# Project
from .map import Map
from .max import Max
from .min import Min
from .skip import Skip
from .stop import Stop
from .take import Take
from .filter import Filter
from .assertion import Assert
