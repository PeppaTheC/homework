class PrintableFolder:
    def __init__(self, name: str, content: list = None):
        self.name = name
        self.content = content

    def __str__(self, level=-1):
        text = "|   " * level
        if level > -1:
            text += "|-> "
        text += f"V {self.name}\n"
        if self.content:
            for obj in self.content:
                text += obj.__str__(level + 1)
        return text

    def __contains__(self, item):
        if not self.content:
            return False
        for content in self.content:
            if isinstance(content, PrintableFolder):
                if item in content:
                    return True
            elif isinstance(content, PrintableFile):
                if content == item:
                    return True
        return False


class PrintableFile:
    def __init__(self, name):
        self.name = name

    def __str__(self, level=-1):
        text = "|   " * level
        if level > -1:
            text += "|-> "
        text += self.name + "\n"
        return text


if __name__ == '__main__':
    file1 = PrintableFile("file1")
    file2 = PrintableFile("file2")
    file3 = PrintableFile("file3")

    folder3 = PrintableFolder("folder3", [file3])
    folder2 = PrintableFolder("folder2", [folder3, file2])
    folder1 = PrintableFolder("folder1", [folder2, file1])

    print(folder1)
    print(file3 in folder2)
    print(file1 in folder2)
