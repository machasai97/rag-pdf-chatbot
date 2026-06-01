# from fastapi import FastAPI, UploadFile

# import shutil

# from pdf_reader import read_pdf

# from chunking import split_text

# from embeddings import (
#     create_embeddings,
#     model
# )

# from vectordb import (
#     store_embeddings,
#     search_embeddings
# )

# from llm import ask_llm


# app = FastAPI()


# @app.post("/upload")

# async def upload_pdf(file: UploadFile):

#     file_path = f"data/{file.filename}"

#     with open(file_path, "wb") as buffer:

#         shutil.copyfileobj(
#             file.file,
#             buffer
#         )

#     text = read_pdf(file_path)

#     chunks = split_text(text)

#     embeddings = create_embeddings(
#         chunks
#     )

#     store_embeddings(
#         chunks,
#         embeddings
#     )

#     return {
#         "message": "PDF uploaded successfully"
#     }


# @app.get("/chat")

# async def chat(question: str):

#     query_embedding = model.encode(
#         question
#     )

#     results = search_embeddings(
#         query_embedding
#     )

#     context = results["documents"][0][0]

#     answer = ask_llm(
#         context,
#         question
#     )

#     return {
#         "question": question,
#         "answer": answer
#     }

from fastapi import (
    FastAPI,
    UploadFile,
    Request
)

from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse

import shutil

from app.pdf_reader import read_pdf

from app.chunking import split_text

from app.embeddings import (
    create_embeddings,
    model
)

from app.vectordb import (
    store_embeddings,
    search_embeddings
)

from app.llm import ask_llm
import os

app = FastAPI()

templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "request": request
        }
    )
@app.post("/upload")

async def upload_pdf(file: UploadFile):

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # READ PDF

    text = read_pdf(file_path)

    print(text)

    # SPLIT TEXT

    chunks = split_text(text)

    print(chunks)

    # CREATE EMBEDDINGS

    embeddings = create_embeddings(chunks)

    print(embeddings.shape)

    # STORE IN CHROMADB

    store_embeddings(
        chunks,
        embeddings
    )

    return {
        "message": "PDF uploaded successfully"
    }


@app.get("/chat")

async def chat(question: str):

    query_embedding = model.encode(
        question
    )

    results = search_embeddings(
        query_embedding
    )

    documents = results["documents"]

    if not documents or not documents[0]:

        return {
            "answer": "No PDF data found. Please upload PDF first."
        }

    context = documents[0][0]

    answer = ask_llm(
        context,
        question
    )

    return {
        "answer": answer
    }