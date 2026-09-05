from ingestion.parser import CodeParser

code = """
class AuthService:

    def authenticate(self, token):
        user = verify_token(token)
        return user


def verify_token(token):
    return token != ""
"""

parser = CodeParser()
tree = parser.parse(code, "python")
print(tree.root_node)