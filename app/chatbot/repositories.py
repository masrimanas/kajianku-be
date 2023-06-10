# pylint: disable=line-too-long
import time
from decouple import config
from fastapi import status, HTTPException
import pinecone
import openai
from openai.embeddings_utils import get_embedding
from app.chatbot.schemas import NewData, Question, QuestionOut

pinecone.init(
    api_key=config("PINECONE_API_KEY"),
    environment=config("PINECONE_ENV"),
)
index = pinecone.Index(config("PINECONE_INDEX"))


async def insert(data: NewData):
    try:
        embed = get_embedding(data.content, engine="text-embedding-ada-002")
        index.upsert(
            vectors=[
                {
                    "id": str(time.time()),
                    "values": embed,
                    "metadata": {"text": data.content},
                }
            ]
        )
        return {
            "message": "Data berhasil disimpan",
        }
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Terjadi kesalahan",
        ) from exc


async def ask(question: Question):
    try:
        embed = get_embedding(question.content, engine="text-embedding-ada-002")
        query_result = index.query(
            vector=embed,
            top_k=3,
            include_metadata=True,
            include_values=False,
        )

        # Todo: try to find condition that answer is not found
        # if len(query_result["matches"]) == 0:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "answer": "Maaf, kami tidak dapat menemukan jawaban yang sesuai. Silahkan tulis kembali pertanyaan anda.",
        # }

        context = ""
        for result in query_result["matches"]:
            context += result["metadata"]["text"] + "\n"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah seorang asisten digital yang bisa menjawab pertanyaan berdasarkan data-data yang saya beri",
                },
                {
                    "role": "user",
                    "content": f"Konteks: {context}\n\n Jawablah pertanyaan saya hanya berdasarkan konteks-konteks yang ada dengan tanpa menyebutkan sumbernya",
                    # "content": "Data: {}\n\n Kamu akan menjawab pertanyaan berdasarkan data-data diatas".format(
                    #     context
                    # ),
                },
                {"role": "assistant", "content": "Oke, siap!"},
                {"role": "user", "content": question.content},
            ],
        )
        return QuestionOut(
            status="Berhasil", answer=response.choices[0].message.content
        )
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Terjadi kesalahan",
        ) from exc
