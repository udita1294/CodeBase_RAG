from tree_sitter import Language, Parser
import tree_sitter_python

class CodeParser:
    def __init__(self):
        self.languages = {
            "python": Language(tree_sitter_python.language()),
        }
    def parse(self, code: str, language_name: str):
        if language_name not in self.languages:
            raise ValueError(f"Unsupported language: {language_name}")
        language = self.languages[language_name]
        parser = Parser(language)
        tree = parser.parse(code.encode("utf-8"))
        return tree