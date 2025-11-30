from typing import List

import fitz  

class PDFProcessor:
    def __init__(self) -> None:
        pass

    def extract_text_with_markers(self, pdf_bytes: bytes) -> str:
        """
        Extracts text from a PDF provided as bytes, inserting markers before paragraphs.
        
        The marker format is !!<page_no>,<y_coordinate>!! on a separate line.
        Page numbers are 1-based.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text: List[str] = []

        for page_num, page in enumerate(doc, start=1):
            # Get text blocks. Each block is a tuple: (x0, y0, x1, y1, "text", block_no, block_type)
            blocks = page.get_text("blocks")
            
            # Sort blocks vertically then horizontally to ensure reading order
            blocks.sort(key=lambda b: (b[1], b[0]))

            for block in blocks:
                # block[4] contains the text content
                # block[6] is the block type (0 for text, 1 for image)
                if block[6] == 0: 
                    y_coord = int(block[1]) # y0 coordinate
                    text_content = block[4].strip()
                    
                    if text_content:
                        marker = f"!!{page_num},{y_coord}!!"
                        full_text.append(marker)
                        full_text.append(text_content)

        return "\n".join(full_text)
    
async def get_pdf_processor():
    yield PDFProcessor()
