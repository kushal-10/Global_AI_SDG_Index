## Convert .docx to .txt, only used for Microsoft as annual reports were avaiable in docx format

import os
from docx import Document

# Define input and output base paths
input_dir = "annual_reports/USA/2.Microsoft_$3.036 T_Information Tech"
output_base_dir = "annual_txts_fitz/USA/2.Microsoft_$3.036 T_Information Tech"

# Loop over each year
for year in range(2014, 2024):
    docx_filename = f"Microsoft{year}.docx"
    docx_path = os.path.join(input_dir, docx_filename)

    # Load and extract text
    if os.path.exists(docx_path):
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])

        # Create output directory for that year
        output_dir = os.path.join(output_base_dir, str(year))
        os.makedirs(output_dir, exist_ok=True)

        # Write to results.txt
        output_txt_path = os.path.join(output_dir, "results.txt")
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {output_txt_path}")
    else:
        print(f"File not found: {docx_path}")
