import easyocr

class OCRService:
    reader = easyocr.Reader(
        ["en"],
        gpu = False
    )

    @classmethod
    async def extract_text(
        cls,
        file_path : str,
    )->str:
        results = cls.reader.readtext(
            file_path,
            detail=0
        )
        return "\n".join(results)