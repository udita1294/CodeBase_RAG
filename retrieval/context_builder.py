
class ContextBuilder:
    def build(self, results):
        context_parts = []

        for result in results:
            payload = result.payload

            file_path = payload.get("file_path","unknown")
            name = payload.get("name","unknown")
            chunk_type = payload.get("type","unknown")
            start_line = payload.get("start_line","?")
            end_line = payload.get("end_line","?")
            content = payload.get("content","")
            context = f"""
                            File: {file_path}
                            Type: {chunk_type}
                            Name: {name}
                            Lines: {start_line}-{end_line}

                            Code:
                            {content}
                        """

            context_parts.append(context)
        return "\n\n".join(context_parts)