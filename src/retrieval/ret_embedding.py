import os 
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

text_splitter = SemanticChunker(OpenAIEmbeddings())

txt_path = os.path.join("annual_txts_fitz", "USA", "10.Tesla_$663.43B_Industries", "2014", "results.txt")
with open(txt_path) as f:
    txt_content = f.read()


docs = text_splitter.create_documents([txt_content])
print(docs[0].page_content)