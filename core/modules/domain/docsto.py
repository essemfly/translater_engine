class Line:
    def __init__(self, id, line):
        self.id = id
        self.line = line

    def to_dict(self):
        return {self.id: self.line}


class Paragraph:
    def __init__(self, id, paragraph, lines):
        self.id = id
        self.paragraph = paragraph
        self.lines = lines

    def to_dict(self):
        return {self.id: self.paragraph}