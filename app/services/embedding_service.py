from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(step_text, video_text):
    """
    Compare step instruction with video content
    using embeddings + cosine similarity
    """

    try:
        # Generate embeddings
        step_embedding = model.encode([step_text])
        video_embedding = model.encode([video_text])

        # Similarity
        similarity = cosine_similarity(
            step_embedding,
            video_embedding
        )[0][0]

        return float(similarity)

    except Exception as e:
        print("[embedding_service] Error:", e)
        return 0.0