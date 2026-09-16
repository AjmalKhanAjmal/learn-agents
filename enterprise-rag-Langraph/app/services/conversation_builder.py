from app.core.logger import logger


class ConversationBuilder:

    MAX_MESSAGES = 10

    def build(
        self,
        history: list[dict[str, str]],
    ) -> str:
        logger.info("starting Citation Service ")
        if not history:
            return "No previous conversation."

        history = history[-self.MAX_MESSAGES :]

        result: list[str] = []

        for message in history:

            role = message.get(
                "role",
                "user",
            )

            content = message.get(
                "content",
                "",
            )

            if not content:
                continue

            result.append(f"{role.upper()}: {content}")

        return "\n".join(result)
