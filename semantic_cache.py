"""
A python representation of the ipython notebook represented in the cited notebook
@misc{2024
title = {Semantic Cache from Scratch},
author = {Hamza Farooq, Darshil Modi, Kanwal Mehreen, Nazila Shafiei},
keywords = {Semantic Cache},
year = {2024},
copyright = {APACHE 2.0 license}
}
"""

import time

import faiss
from typing import Dict

from sentence_transformers import SentenceTransformer
from api import api_call

class SemanticCaching:
    """
    Semantic caching class implementing Euclidian Distance from faiss module.
    It creates a local non-persistent cache. The class is enriched with api_url and api_headers
    for it to be able to request data from an external API
    """
    def __init__(self, api_url: str, api_headers: Dict):

        self.index = faiss.IndexFlatL2(768)
        if self.index.is_trained:
            print('Index is trained')

        self.api_url = api_url
        self.api_headers = api_headers

        self.encoder = SentenceTransformer('all-mpnet-base-v2')
        self.euclidian_threshold = 0.3
        self. cache = {
                "questions": [],
                "embeddings": [],
                "answers": [],
                "response_text": []
            }

    def query(self, question: str) -> str | None:
        start_time = time.time()

        try:
            q = [question]
            embedding = self.encoder.encode(q)

            # the index search returns a tuple as: distance -> [[3.4028235e+38]] and idx_position -> [[-1]]
            # distance is sorted in ascending order
            # idx_position represents the position it was found in the faiss FlatL2 Index, if not found, it returns -1
            distance, idx_position = self.index.search(embedding, 1)

            print(question)
            print(distance, idx_position)

            if distance[0][0] >= 0:
                if idx_position[0][0] != -1 and distance[0][0] <= self.euclidian_threshold:
                    idx_row = int(idx_position[0][0])

                    # TODO: why do we show an inverse score here?
                    print(f"Question found in cache at position: {idx_row} with the score { 1 - distance[0][0]}")

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Time took to execute the query: {elapsed_time} seconds")

                    return self.cache['response_text'][idx_row]

            api_response = api_call([question], self.api_url, self.api_headers)

            if api_response is not None:
                response_text = api_response['data']['response_text']

                self.cache['questions'].append(question)
                self.cache['embeddings'].append(embedding[0].tolist())
                self.cache['answers'].append(api_response)
                self.cache['response_text'].append(response_text)

                # TODO: what is missing as a param from index.add?
                self.index.add(embedding)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time taken: { elapsed_time } seconds")

                return response_text

            return None

        except Exception as e:
            raise RuntimeError(f"Error during query method: { e }")
