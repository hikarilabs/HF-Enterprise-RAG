import os
from pathlib import Path

from dotenv import load_dotenv

from semantic_cache.SemanticCache import SemanticCaching

load_dotenv()

traversaal_url = "https://api-ares.traversaal.ai/live/predict"
traversaal_headers = {
        "x-api-key": os.environ.get("ARES_KEY"),
        "content-type": "application/json"
    }


if __name__ == '__main__':

    ROOT_DIR = Path(__file__).parent.resolve()

    file_path = Path('')
    sc = SemanticCaching(traversaal_url, traversaal_headers)

    q1 = 'Who is the current CEO of Google?'
    q2 = 'What is the Capital of India'
    q3 = 'Is Sundar Pichai the CEO of Google?'
    q4 = 'Can you tell me the Capital of India'

    answer1 = sc.query(q1)
    # print(answer1)

    answer2 = sc.query(q2)
    # print(answer2)

    answer3 = sc.query(q3)
    # print(answer3)

    answer4 = sc.query(q4)
    # print(answer4)

    answer5 = sc.query(q2)

