
class CodeChunker:
    def create_chunks(self, files):
        chunks = []

        for file in files:
            code_elements = file.get("code")
            if not code_elements:
                continue

            for element in code_elements:
                chunk = {
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