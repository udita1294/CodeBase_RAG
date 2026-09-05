
class CodeExtractor:
    def extract(self, tree, source_code):
        results = []
        self._walk(tree.root_node,results,source_code)
        return results

    def _walk(self, node, results, source_code):
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                content = source_code[node.start_byte:node.end_byte]

                results.append({
                    "type": "function",
                    "name": name_node.text.decode("utf-8"),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                    "content": content,
                })

        elif node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                content = source_code[node.start_byte:node.end_byte]

                results.append({
                    "type": "class",
                    "name": name_node.text.decode("utf-8"),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                    "content": content,
                })

        for child in node.children:
            self._walk(child,results,source_code)