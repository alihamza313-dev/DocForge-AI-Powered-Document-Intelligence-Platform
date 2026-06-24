import asyncio
from app.services.ocr import OCRService

async def main():
    text = await OCRService.extract_text("uploads/test5.png")

    print(text)

asyncio.run(main())