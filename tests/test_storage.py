import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from files_app.storage import Storage


def zip_of(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return buffer.getvalue()


class StorageTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "files"
        self.root.mkdir()
        self.storage = Storage(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_save_then_read_returns_the_same_bytes(self):
        self.storage.save_file("report.pdf", b"%PDF-1.7")
        self.assertEqual(self.storage.read_file("report.pdf"), b"%PDF-1.7")

    def test_save_creates_missing_folders(self):
        self.storage.save_file("2026/q1/invoice.txt", b"total: 42")
        self.assertEqual((self.root / "2026" / "q1" / "invoice.txt").read_bytes(), b"total: 42")

    def test_save_replaces_an_existing_file(self):
        self.storage.save_file("notes.txt", b"first")
        self.storage.save_file("notes.txt", b"second")
        self.assertEqual(self.storage.read_file("notes.txt"), b"second")

    def test_reading_a_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.read_file("nope.txt")

    def test_delete_removes_the_file(self):
        self.storage.save_file("old.txt", b"x")
        self.storage.delete_file("old.txt")
        self.assertFalse((self.root / "old.txt").exists())

    def test_list_dir_returns_sorted_names(self):
        for name in ("b.txt", "a.txt", "c.txt"):
            self.storage.save_file(name, b"")
        self.assertEqual(self.storage.list_dir(), ["a.txt", "b.txt", "c.txt"])

    def test_list_dir_of_a_subfolder(self):
        self.storage.save_file("photos/cat.jpg", b"")
        self.assertEqual(self.storage.list_dir("photos"), ["cat.jpg"])

    def test_extract_archive_writes_every_member(self):
        written = self.storage.extract_archive(zip_of({"a.txt": b"A", "docs/b.txt": b"B"}))
        self.assertEqual(sorted(written), ["a.txt", "docs/b.txt"])
        self.assertEqual(self.storage.read_file("docs/b.txt"), b"B")


if __name__ == "__main__":
    unittest.main()
