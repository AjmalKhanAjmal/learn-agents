import redis
import json
from app.config.settings import settings

r = redis.Redis.from_url(settings.REDIS_URL)


class RedisMemory:

    @staticmethod
    def save_message(session_id, role, content):
        try:
            key = f"chat:{session_id}"

            existing = r.get(key)

            if existing:
                data = json.loads(existing)
            else:
                data = []

            data.append({
                "role": role,
                "content": content
            })

            r.set(key, json.dumps(data))

            print(f"[SUCCESS] Message saved for session: {session_id}")

        except Exception as e:
            print(f"[ERROR] save_message failed: {e}")
            raise

    @staticmethod
    def get_history(session_id):
        try:
            key = f"chat:{session_id}"

            data = r.get(key)

            if not data:
                return []

            history = json.loads(data)

            print(f"[SUCCESS] History fetched for session: {session_id}")

            return history

        except Exception as e:
            print(f"[ERROR] get_history failed: {e}")
            raise