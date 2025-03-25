## Extracting Text from PDFs

#### PyMuPDF

This is the OG, the KING of extracting text from PDFs, but with a big caveat, i.e. does not support non-ascii characters
OR when the PDF is scanned instead of being in a digital format

```
python3 src/extract/pdf2text.py
```

Check if PDF to text generates any non_ascii values

```
python3 src/extract/check_non_ascii.py
```
If there are non_ascii values --> Enter OCR. TODO: Check for zh, hi languages

#### Docling OCR

Good enough, off the shelf OCR via langchain