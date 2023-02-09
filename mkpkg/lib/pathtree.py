""" Tree """
class PathTree:
    tree = {}
    files = []

    def __str__(self) -> str:

        return ""

    def __list__(self) -> list:
        return self.files

    def __add_tree(self, parts):
        iters = len(parts)
        for i in range(iters):
            j = i + 1
            if j >= iters:
                continue
            self

    def add(self, file):
        if file not in self.files:
            self.files.append(file)


