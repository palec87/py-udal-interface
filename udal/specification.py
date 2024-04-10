from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar


class NamedQueryInfo():
    """Information about a named query, namely its name, parameters, and
    fields."""

    def __init__(self,
            name: str,
            params: dict[str, type] = {}):
        self._name = name
        self._params = params

    @property
    def name(self) -> str:
        """Query name."""
        return self._name

    @property
    def params(self) -> dict[str, type]:
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


class UDAL(ABC):
    """Uniform Data Access Layer"""

    @property
    @abstractmethod
    def query_names(self) -> List[str]:
        """Names of the queries supported by the current implementation."""
        pass

    @property
    @abstractmethod
    def queries(self) -> List[str]: # TODO Return query info.
        """Information about the queries supported by the current
        implementation."""
        pass

    @abstractmethod
    def execute(self, name: str, params: dict) -> Result:
        """Run a query with the given arguments."""
        pass
