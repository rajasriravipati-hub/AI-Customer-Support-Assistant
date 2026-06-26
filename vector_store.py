import faiss
import pickle
import numpy as np
import os

from config.settings import FAISS_INDEX_PATH


class VectorStore:

    def __init__(self):

        self.index = None
        self.text_chunks = []


    def create_index(self, embeddings, chunks):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            np.array(
                embeddings,
                dtype="float32"
            )
        )

        self.text_chunks = chunks


    def save_index(self):

        index_folder = os.path.dirname(
            FAISS_INDEX_PATH
        )

        os.makedirs(
            index_folder,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            FAISS_INDEX_PATH
        )


        chunks_path = os.path.join(
            index_folder,
            "chunks.pkl"
        )

        with open(
            chunks_path,
            "wb"
        ) as f:

            pickle.dump(
                self.text_chunks,
                f
            )


    def load_index(self):

        self.index = faiss.read_index(
            FAISS_INDEX_PATH
        )


        chunks_path = os.path.join(
            os.path.dirname(FAISS_INDEX_PATH),
            "chunks.pkl"
        )

        with open(
            chunks_path,
            "rb"
        ) as f:

            self.text_chunks = pickle.load(f)



vector_store = VectorStore()