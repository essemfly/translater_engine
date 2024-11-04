class GoogleDocument:
    def __init__(self, uri, mime_type, text, pages):
        self.uri = uri
        self.mime_type = mime_type
        self.text = text
        self.pages = pages

    @classmethod
    def from_dict(cls, data):
        pages = [GoogleDocumentPage.from_dict(page) for page in data["pages"]]
        return cls(
            uri=data["uri"], mime_type=data["mimeType"], text=data["text"], pages=pages
        )

    def __repr__(self):
        return f"Document(uri={self.uri}, mime_type={self.mime_type}, text={self.text})"


class GoogleDocumentPage:
    def __init__(
        self, page_number, transforms, dimension, layout, blocks, paragraphs, lines
    ):
        self.page_number = page_number
        self.transforms = transforms
        self.dimension = dimension
        self.layout = layout
        self.blocks = blocks
        self.paragraphs = paragraphs
        self.lines = lines

    @classmethod
    def from_dict(cls, data):
        transforms = [
            GoogleDocumentMatrix.from_dict(t) for t in data.get("transforms", [])
        ]
        dimension = GoogleDocumentDimension.from_dict(data.get("dimension", {}))
        layout = GoogleDocumentLayout.from_dict(data.get("layout", {}))
        blocks = [
            GoogleDocumentBlock.from_dict(block) for block in data.get("blocks", [])
        ]
        paragraphs = [
            GoogleDocumentParagraph.from_dict(paragraph)
            for paragraph in data.get("paragraphs", [])
        ]
        lines = [GoogleDocumentLine.from_dict(line) for line in data.get("lines", [])]

        return cls(
            page_number=data.get("pageNumber", 0),
            transforms=transforms,
            dimension=dimension,
            layout=layout,
            blocks=blocks,
            paragraphs=paragraphs,
            lines=lines,
        )

    def __repr__(self):
        return (
            f"GoogleDocumentPage(page_number={self.page_number}, image={self.image}, "
            f"transforms={self.transforms}, dimension={self.dimension}, layout={self.layout})"
        )


class GoogleDocumentMatrix:
    def __init__(self, rows, cols, type, data):
        self.rows = rows
        self.cols = cols
        self.type = type
        self.data = data

    @classmethod
    def from_dict(cls, data):
        return cls(
            rows=data["rows"], cols=data["cols"], type=data["type"], data=data["data"]
        )

    def __repr__(self):
        return f"GoogleDocumentMatrix(rows={self.rows}, cols={self.cols}, type={self.type}, data={self.data})"


class GoogleDocumentDimension:
    def __init__(self, width, height, unit):
        self.width = width
        self.height = height
        self.unit = unit

    @classmethod
    def from_dict(cls, data):
        return cls(width=data["width"], height=data["height"], unit=data["unit"])

    def __repr__(self):
        return f"GoogleDocumentDimension(width={self.width}, height={self.height}, unit={self.unit})"


class GoogleDocumentLayout:
    def __init__(self, textAnchor, boundingPoly, orientation):
        self.textAnchor = GoogleDocumentTextAnchor.from_dict(textAnchor)
        self.boundingPoly = GoogleDocumentBoundingPoly.from_dict(boundingPoly)
        self.orientation = orientation

    @classmethod
    def from_dict(cls, data):
        return cls(
            textAnchor=data["textAnchor"],
            boundingPoly=data["boundingPoly"],
            orientation=data["orientation"],
        )

    def __repr__(self):
        return f"GoogleDocumentLayout(textAnchor={self.textAnchor}, boundingPoly={self.boundingPoly}, orientation={self.orientation})"


class GoogleDocumentTextAnchor:
    def __init__(self, textSegments, content):
        self.textSegments = [
            GoogleDocumentTextSegment.from_dict(segment) for segment in textSegments
        ]
        self.content = content

    @classmethod
    def from_dict(cls, data):
        return cls(
            textSegments=data["textSegments"], content=data.get("content", "no content")
        )

    def __repr__(self):
        return f"GoogleDocumentTextAnchor(textSegments={self.textSegments}, content={self.content})"


class GoogleDocumentTextSegment:
    def __init__(self, startIndex, endIndex):
        self.startIndex = startIndex
        self.endIndex = endIndex

    @classmethod
    def from_dict(cls, data):
        return cls(startIndex=data.get("startIndex", 0), endIndex=data["endIndex"])

    def __repr__(self):
        return f"GoogleDocumentTextSegment(startIndex={self.startIndex}, endIndex={self.endIndex})"


class GoogleDocumentBoundingPoly:
    def __init__(self, vertices, normalizedVerticies):
        self.vertices = [GoogleDocumentVertex.from_dict(vertex) for vertex in vertices]
        self.normalizedVerticies = [
            GoogleDocumentVertex.from_dict(vertex) for vertex in normalizedVerticies
        ]

    @classmethod
    def from_dict(cls, data):
        return cls(
            vertices=data.get("vertices", []),
            normalizedVerticies=data.get("normalizedVertices", []),
        )

    def __repr__(self):
        return f"GoogleDocumentBoundingPoly(vertices={self.vertices}, normalizedVerticies={self.normalizedVerticies})"


class GoogleDocumentVertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data):
        return cls(
            x=data.get("x", 0),  # Default to 0 if x is missing
            y=data.get("y", 0),  # Default to 0 if y is missing
        )

    def __repr__(self):
        return f"GoogleDocumentVertex(x={self.x}, y={self.y})"


class GoogleDocumentBlock:
    def __init__(self, layout, detectedLanguages):
        self.layout = GoogleDocumentLayout.from_dict(layout)
        self.detectedLanguages = [
            GoogleDocumentDetectedLanguage.from_dict(lang) for lang in detectedLanguages
        ]

    @classmethod
    def from_dict(cls, data):
        detectedLanguages = data.get("detectedLanguages", [])
        detectedLanguages = [
            GoogleDocumentDetectedLanguage.from_dict(lang) for lang in detectedLanguages
        ]
        return cls(layout=data["layout"], detectedLanguages=detectedLanguages)

    def __repr__(self):
        return f"GoogleDocumentBlock(layout={self.layout}, detectedLanguages={self.detectedLanguages})"


class GoogleDocumentDetectedLanguage:
    def __init__(self, languageCode, confidence):
        self.languageCode = languageCode
        self.confidence = confidence

    @classmethod
    def from_dict(cls, data):
        return cls(languageCode=data["languageCode"], confidence=data["confidence"])

    def __repr__(self):
        return f"GoogleDocumentDetectedLanguage(languageCode={self.languageCode}, confidence={self.confidence})"


class GoogleDocumentParagraph:
    def __init__(self, layout, detectedLanguages):
        self.layout = GoogleDocumentLayout.from_dict(layout)
        self.detectedLanguages = [
            GoogleDocumentDetectedLanguage.from_dict(lang) for lang in detectedLanguages
        ]

    @classmethod
    def from_dict(cls, data):
        return cls(
            layout=data["layout"],
            detectedLanguages=data.get("detectedLanguages", []),
        )

    def __repr__(self):
        return f"GoogleDocumentParagraph(layout={self.layout}, detectedLanguages={self.detectedLanguages})"


class GoogleDocumentLine:
    def __init__(self, layout, detectedLanguages):
        self.layout = GoogleDocumentLayout.from_dict(layout)
        self.detectedLanguages = [
            GoogleDocumentDetectedLanguage.from_dict(lang) for lang in detectedLanguages
        ]

    @classmethod
    def from_dict(cls, data):
        return cls(
            layout=data["layout"],
            detectedLanguages=data.get("detectedLanguages", []),
        )

    def __repr__(self):
        return f"GoogleDocumentLine(layout={self.layout}, detectedLanguages={self.detectedLanguages})"
