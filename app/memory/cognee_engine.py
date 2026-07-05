import os
import logging
import cognee

# Set correct Cognee environment parameters
# Why we strip 'ollama/': Cognee's internal Ollama adapter routes requests through AsyncOpenAI.
# Using 'ollama/llama3.2' will request that exact string from Ollama which fails with 404 (model not found).
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["LLM_MODEL"] = "llama3.2"
os.environ["LLM_ENDPOINT"] = "http://localhost:11434/v1"
os.environ["LLM_API_KEY"] = "ollama"

# Embeddings endpoint for Ollama requires direct /api/embed and dimension 768 for nomic-embed-text
os.environ["EMBEDDING_PROVIDER"] = "ollama"
os.environ["EMBEDDING_MODEL"] = "nomic-embed-text"
os.environ["EMBEDDING_ENDPOINT"] = "http://localhost:11434/api/embed"
os.environ["EMBEDDING_DIMENSIONS"] = "768"

logger = logging.getLogger("uvicorn")

async def store_chat_turn(user_id: str, session_id: str, chat_payload: str):
    """Stores the latest chat interaction as a memory frame in the Cognee graph database."""
    try:
        # cognee.add accepts dataset_name to specify which namespace the data belongs to.
        await cognee.add(chat_payload, dataset_name=f"unimind_user_{user_id}")
        await cognee.cognify()
        logger.info(f"🧠 Central memory graph updated for User: {user_id}")
    except Exception as error:
        logger.error(f"❌ Cognee write failed: {str(error)}")

async def recall_shared_context(user_id: str, session_id: str, current_query: str) -> str:
    """Retrieves relevant past interactions/memories from the user's namespace in the graph database."""
    try:
        # Why 'datasets' instead of 'dataset_name': Cognee's search function signature takes 'datasets' (str or list of str).
        results = await cognee.search(current_query, datasets=f"unimind_user_{user_id}")
        if results:
            return f"\n[Shared Memory Context]:\n{str(results[:3])}\n"
        return ""
    except Exception as error:
        logger.error(f"❌ Cognee recall failed: {str(error)}")
        return ""