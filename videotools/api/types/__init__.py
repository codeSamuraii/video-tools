from pathlib import Path
from typing import TypeVar, Optional

Source = TypeVar('Source', str, Path)
Dest = Optional[Source]
