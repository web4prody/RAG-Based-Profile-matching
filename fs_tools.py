from pathlib import Path
from datetime import datetime

from pypdf import PdfReader
from docx import Document


def read_file(filepath: str) -> dict:
    try:
        path = Path(filepath)

        if not path.exists():
            return {
                "success": False,
                "error": "File not found"
            }

        extension = path.suffix.lower()

        if extension == ".txt":
            content = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        elif extension == ".pdf":
            reader = PdfReader(path)

            content = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        elif extension == ".docx":
            document = Document(path)

            content = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {extension}"
            }

        stat = path.stat()

        return {
            "success": True,
            "content": content,
            "metadata": {
                "name": path.name,
                "extension": extension,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }



def list_files(directory: str, extension: str = None) -> list:
    try:
        folder = Path(directory)

        if not folder.exists():
            return []

        results = []

        if extension:
            if not extension.startswith("."):
                extension = "." + extension

            extension = extension.lower()

        for path in folder.iterdir():

            if not path.is_file():
                continue

            if extension and path.suffix.lower() != extension:
                continue

            stat = path.stat()

            results.append({
                "name": path.name,
                "path": str(path),
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            })

        return results

    except Exception:
        return []



def write_file(filepath: str, content: str) -> dict:
    try:
        path = Path(filepath)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "success": True,
            "filepath": str(path),
            "bytes_written": path.stat().st_size
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }



def search_in_file(filepath: str, keyword: str) -> dict:
    try:
        result = read_file(filepath)

        if not result["success"]:
            return result

        content = result["content"]

        lines = content.splitlines()

        matches = []

        for line_number, line in enumerate(lines, start=1):

            if keyword.lower() in line.lower():

                start = max(0, line_number - 2)
                end = min(len(lines), line_number + 1)

                context = "\n".join(lines[start:end])

                matches.append({
                    "line_number": line_number,
                    "text": line.strip(),
                    "context": context
                })

        return {
            "success": True,
            "filepath": filepath,
            "keyword": keyword,
            "match_count": len(matches),
            "matches": matches
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }