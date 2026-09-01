from pathlib import Path
from .file_filter import get_language, should_ignore

class RepositoryScanner:
    def scan(self, repository_path: str):
        repository_path = Path(repository_path)
        files = []
        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue
            relative_path = file_path.relative_to(repository_path)
            if should_ignore(relative_path):
                continue
            language = get_language(file_path)
            if language is None:
                continue
            files.append({
                "path": str(relative_path),
                "language": language,
                "extension": file_path.suffix.lower(),
                "size": file_path.stat().st_size,
            })
        return files