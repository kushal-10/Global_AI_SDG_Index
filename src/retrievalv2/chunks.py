import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

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

    BASE_DIR = "annual_txts_fitz"

    txt_files = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.endswith(".txt"):
                txt_files.append(os.path.join(dirname, filename))


    total_chunks = 0
    for txt_file in tqdm(txt_files):
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = get_chunks(text)

        total_chunks += len(chunks)

    print(f"Total chunks: {total_chunks}")

