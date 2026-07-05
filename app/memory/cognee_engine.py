import os
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["LLM_MODEL"] = "ollama/llama3.2"
os.environ["LLM_ENDPOINT"] = "http://localhost:11434"
os.environ["EMBEDDING_PROVIDER"] = "ollama"
os.environ["EMBEDDING_MODEL"] = "ollama/nomic-embed-text"
os.environ["EMBEDDING_ENDPOINT"] = "http://localhost:11434"

import cognee
import logging

logger = logging.getLogger("uvicorn")

async def store_chat_turn(user_id: str, session_id: str, chat_payload: str):
    try:
        await cognee.add(chat_payload, dataset_name=f"unimind_user_{user_id}")
        await cognee.cognify()
        logger.info(f"🧠 Memory stored for User: {user_id}")
    except Exception as e:
        logger.error(f"❌ Cognee write failed: {str(e)}")

async def recall_shared_context(user_id: str, session_id: str, current_query: str) -> str:
    try:
        results = await cognee.search(current_query, dataset_name=f"unimind_user_{user_id}")
        if results:
            return f"\n[Shared Memory Context]:\n{str(results[:3])}\n"
        return ""
    except Exception as e:
        logger.error(f"❌ Cognee recall failed: {str(e)}")
        return ""