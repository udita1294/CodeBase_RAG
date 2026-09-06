
class CodeChunker:
    def create_chunks(self, files):
        chunks = []

        for file in files:
            code_elements = file.get("code")
            if not code_elements:
                continue

            for index, element in enumerate(code_elements):
                chunk = {
                    "chunk_id": f"{file['path']}::{element['type']}::{index}",
                    "content": element["content"],

                    "metadata": {
                        "file_path": file["path"],
                        "language": file["language"],
                        "type": element["type"],
                        "name": element["name"],
                        "start_line": element["start_line"],
                        "end_line": element["end_line"],
                    }
                }
                chunks.append(chunk)
        return chunks