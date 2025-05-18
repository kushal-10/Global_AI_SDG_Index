import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

from src.retrievalv2.keys import SKIP_REPORTS

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
)

def get_chunks(text: str) -> list :
    """Get a list of chunks from text file."""

    texts = text_splitter.create_documents([text])
    text_contents = [text.page_content for text in texts]
    return text_contents


if __name__ == "__main__":
    fp = "annual_txts_fitz/India/1.Reliance Industries_$244.77 B_Energy/2015/results.txt"
    with open(fp) as f:
        text = f.read()

    texts = get_chunks(text)
    print(texts[0])
    # BASE_DIR = "annual_txts_fitz"
    # reports = []
    #
    # for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    #     if 'results.txt' in filenames:
    #         file_path = os.path.join(dirpath, 'results.txt')
    #         if file_path not in SKIP_REPORTS:
    #             reports.append(file_path)
    #
    # for report in tqdm(reports):
    #     with open(report) as f:
    #         txt_contents = f.read()
    #     chunks = get_chunks(txt_contents)
    #
    # # TODO : Analysis of chunks, avg word count, chunk length etc...



