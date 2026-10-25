"""Attachment storage: files kept under one root directory.

Every name this module receives comes from a user: a download link, an upload
form, a delete button, a folder listing, the member names inside a zip they
uploaded. Each operation turns the name into a path with `safe_path`, which
refuses any name that would land outside the storage root.
"""

import io
import os
import zipfile
from pathlib import Path


class PathRefused(Exception):
    """The name does not stay inside the storage root."""

    def __init__(self, name):
        super().__init__(f"refused: {name!r} leaves the storage root")
        self.name = name


class Storage:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def safe_path(self, name):
        """The path for `name` under the root. Raises PathRefused if it escapes.

        Symlinks are resolved before the check, so a link inside the root that
        points outside it is refused like any other escape.
        """
        candidate = (self.root / name).resolve()
        if not candidate.is_relative_to(self.root):
            raise PathRefused(name)
        return candidate

    def read_file(self, name):
        path = self.safe_path(name)
        return path.read_bytes()

    def save_file(self, name, data):
        """Write `data` atomically: a reader never sees a half-written file."""
        target = self.safe_path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.name + ".partial")
        partial.write_bytes(data)
        os.replace(partial, target)

    def delete_file(self, name):
        existing = self.safe_path(name)
        existing.unlink()

    def list_dir(self, name=""):
        """The names of the entries in a folder under the root, sorted."""
        folder = self.safe_path(name)
        return sorted(entry.name for entry in folder.iterdir())

    def extract_archive(self, data, into=""):
        """Unpack an uploaded zip under the folder `into`.

        Every member name is checked before anything is written: one member
        that would land outside the root refuses the whole archive. Returns
        the names written, relative to the root.
        """
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            planned = []
            for member in archive.infolist():
                if member.is_dir():
                    continue
                dest = self.safe_path(os.path.join(into, member.filename))
                planned.append((dest, member))
            for dest, member in planned:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(archive.read(member))
        return [dest.relative_to(self.root).as_posix() for dest, _ in planned]
