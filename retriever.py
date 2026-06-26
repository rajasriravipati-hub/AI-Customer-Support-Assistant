import numpy as np

from utils.embeddings import (
    embedding_model
)

from config.settings import (
    TOP_K_RESULTS
)


def retrieve_context(
    question,
    vector_store
):

    query_embedding = (
        embedding_model.model.encode(
            [question]
        )
    )

    distances, indices = (
        vector_store.index.search(
            np.array(
                query_embedding,
                dtype="float32"
            ),
            TOP_K_RESULTS
        )
    )

    retrieved_chunks = []

    for idx in indices[0]:

        if idx < len(
            vector_store.text_chunks
        ):

            retrieved_chunks.append(
                vector_store.text_chunks[idx]
            )

    if len(retrieved_chunks) > 0:
        print("========== RETRIEVED CHUNK ==========")


        print(retrieved_chunks[0])

        print("====================================")

        return retrieved_chunks[0]

    return ""