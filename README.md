# Uniform Data Access Layer

This is the Python specification of the Uniform Data Access Layer (UDAL).

Documentation: https://lab.fairease.eu/udal/


## Quick Start

There are two sides to a UDAL implementation:

- the user
- the implementer

A user can find existing UDAL implementations that support the named queries
they need. An implementer can provide a package that is able to execute a set of
named queries for their data or for data from third parties.


### Use an existing implementation

Use an existing UDAL implementation, assuming an existing module `my.udal` with
an implementation `MyUDAL`, supporting a named query `urn:example.com:example`:

```python
from my.udal import MyUDAL as UDAL

print(UDAL().execute('urn:example.com:example').data())
```


### Create a new implementation

Create a new UDAL implementation that can be used as above:

```python
import udal.specification as udal

class MyResult(udal.Result[str]):
    """A result containing a string."""

    def data(self, type: type[str] | None = None):
        if type is None or type is str:
            return self._data
        else:
            raise Exception(f'cannot return the data as {type}')

class MyUDAL(udal.UDAL):

    def __init__(self):
        pass

    @property
    def query_names(self):
        return ['urn:example.com:example']

    @property
    def queries(self):
        return {
            'urn:example.com:example': udal.NamedQueryInfo('urn:example.com:example', {})
        }

    def execute(self, name, params={}):
        match name:
            case 'urn:example.com:example':
                return MyResult(self.queries[name], 'example data')
            case _:
                raise Exception(f'query "{name}" not supported')
```
