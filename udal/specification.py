from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, Literal, Tuple, TypeVar, Union


ParamType = Union[
    Literal['null', 'str', 'number', 'boolean'],
    Tuple[Literal['literal'], str | int | float],
    Tuple[Literal['list'], 'ParamType'],
    Tuple[Literal['tuple'], 'ParamType'],
    Tuple[Literal['dict'], Literal['str'], 'ParamType'],
]
"""Description of the type of a parameter."""

Params = dict[str, ParamType | list[ParamType]]

def tliteral(l: str | int | float) -> ParamType:
    return ('literal', l)

def tlist(pt: ParamType) -> ParamType:
    return ('list', pt)

def ttuple(pt: ParamType) -> ParamType:
    return ('tuple', pt)

def tdict(pt: ParamType) -> ParamType:
    return ('dict', 'str', pt)


class NamedQueryInfo():
    """Information about a named query, namely its name, parameters, and
    fields."""

    def __init__(self,
            name: str,
            params: Params = {}):
        self._name = name
        self._params = params

    @property
    def name(self) -> str:
        """Query name."""
        return self._name

    @property
    def params(self) -> Params:
        """Query parameters."""
        return self._params

    def as_dict(self) -> dict:
        """`dict` representation of the query."""
        return {
            'name': self._name,
            'params': { k: v for k, v in self._params },
        }


T = TypeVar('T')

class Result(ABC, Generic[T]):
    """Result from executing an UDAL query."""

    def __init__(self, query: NamedQueryInfo, data: Any, metadata: dict = {}):
        self._query = query
        self._data = data
        self._metadata = metadata

    @property
    def query(self):
        """Information about the query that generated the data in this
        result."""
        return self._query

    @property
    def metadata(self):
        """Metadata associated with the result data."""
        return self._metadata

    @abstractmethod
    def data(self, type: type[T] | None = None) -> T:
        """The data of the result."""
        pass


class Config(ABC):
    """UDAL configuration object"""

    cache_dir: Path | None
    api_tokens: dict[str, str]

    def __init__(self,
            cache_dir: str|Path|None = None,
            api_tokens: dict[str, str] = {},
            ):
        if cache_dir is None:
            self.cache_dir = None
        else:
            self.cache_dir = Path(cache_dir)
        self.api_tokens = api_tokens


class UDAL(ABC):
    """Uniform Data Access Layer"""

    @abstractmethod
    def __init__(self, connectionString: str | None = None, config: Config = Config()):
        """Uniform Data Access Layer.

        Args:
            connectionString: string representing the data source to connect to.
            config: UDAL implementation configuration (e.g., cache directory and API tokens).
        """
        pass

    @property
    def query_names(self) -> list[str]:
        """Names of the queries supported by the current implementation."""
        return list(self.queries.keys())

    @property
    @abstractmethod
    def queries(self) -> dict[str, NamedQueryInfo]:
        """Information about the queries supported by the current
        implementation."""
        pass

    @abstractmethod
    def execute(self, name: str, params: dict) -> Result:
        """Run a query with the given arguments."""
        pass
