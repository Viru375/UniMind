from fastapi import APIRouter, HTTPException, Body
from litellm import acompletion
from app.memory.cognee_engine import store_chat_turn, recall_shared_context

router = APIRouter()

@router.post("/completions")
async def handle_universal_chat(
    user_id: str = Body(..., embed=True),
    session_id: str = Body(..., embed=True),
    model_choice: str = Body(..., embed=True),
    user_prompt: str = Body(..., embed=True)
):
    # 1. Pull graph memory insights from Cognee
    shared_brain_context = await recall_shared_context(
        user_id=user_id,
        session_id=session_id,
        current_query=user_prompt
    )

    # 2. Construct an augmented system directive with the ubiquitous memory
    system_instruction = (
        "You are an assistant inside the UniMind ubiquitous architecture. "
        "All AI instances share one centralized memory via Cognee. "
        f"Here is your persistent context on the user: {shared_brain_context}"
    )

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_prompt}
    ]

    try:
        # 3. Call the target AI model dynamically via LiteLLM
        response = await acompletion(
            model=model_choice,
            messages=messages
        )
        ai_reply = response.choices[0].message.content

        # 4. Asynchronously commit the transaction to the central Cognee brain
        interaction_log = f"User said: {user_prompt} -> AI replied: {ai_reply}"
        await store_chat_turn(user_id=user_id, session_id=session_id, chat_payload=interaction_log)

        return {
            "model_used": model_choice,
            "ai_reply": ai_reply,
            "memory_injected": bool(shared_brain_context)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI routing transaction failed: {str(e)}")