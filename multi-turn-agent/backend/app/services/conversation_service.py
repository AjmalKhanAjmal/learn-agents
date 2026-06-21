from app.memory.redis_memory import RedisMemory
# from app.chains.chat_chain import chain
from app.chains.chat_chain import get_chain

class ConversationService:

    @staticmethod
    def chat(session_id: str, message: str):

        history = RedisMemory.get_history(session_id)

        history_text = ""

        for msg in history:
            history_text += f"{msg['role']}: {msg['content']}\n"

        final_input = f"""
Conversation History:
{history_text}

User Message:
{message}
"""



        chain = get_chain()

        response = chain.invoke({
            "input": final_input
        })

        answer = response.content

        RedisMemory.save_message(session_id, "user", message)
        RedisMemory.save_message(session_id, "assistant", answer)

        return answer