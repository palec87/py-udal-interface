# Uniform Data Access Layer

This is the specification of the Uniform Data Access Layer (UDAL).

## Quick Start


Use an existing UDAL, assuming an existing module `my.udal` with an
implementation `MyUDAL`, supporting a named query `urn:example.com:example`:

```python
from my.udal import MyUDAL

print(MyUDAL().execute('urn:example.com:example').data())
```


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

    @property
    def query_names(self):
        return ['urn:example.com:example']

    @property
    def queries(self):
        return [ udal.NamedQueryInfo('urn:example.com:example') ]

    def execute(self, name, params={}):
        match name:
            case 'urn:example.com:example':
                return MyResult(self.queries[0], 'example data')
            case _:
                raise Exception(f'query "{name}" not supported')
```
