from pathlib import Path
from typing import Any, Optional

import toml

from gourmand.gglobals import gourmanddir


class Prefs(dict):
    """A singleton dictionary for handling preferences."""

    __single = None

    @classmethod
    def instance(cls):
        if Prefs.__single is None:
            Prefs.__single = cls()

        return Prefs.__single

    def __init__(self, filename='preferences.toml'):
        super().__init__()
        self.filename = Path(gourmanddir) / filename
        self.load()

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        if key not in self and default is not None:
            self[key] = default
        return super().get(key)

    def save(self):
        self.filename.parent.mkdir(exist_ok=True)
        with open(self.filename, 'w') as fout:
            toml.dump(self, fout)

    def load(self) -> bool:
        if self.filename.is_file():
            with open(self.filename) as fin:
                for k, v in toml.load(fin).items():
                    self.__setitem__(k, v)
            return True
        return False
