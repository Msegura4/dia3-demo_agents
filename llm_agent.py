from groq import Groq
from dotenv import load_dotenv
import os


class Chatagent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.chat_history = [
            {
                "role": "system",
                "content": Chatagent.read_file(file_path="./context.txt")
            }
        ]

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    def update_history_chat(self, role, content):
        self.chat_history.append(
            {
                "role": role,
                "content": content
            }
        )

    def ask_llm(self, question):
        self.update_history_chat(role="user", content=question)

        response = self.groq_client.chat.completions.create(
            messages=self.chat_history,
            model="openai/gpt-oss-120b",
            include_reasoning=False,
        ).choices[0].message.content

        self.update_history_chat(role="assistant", content=response)

        return response


if __name__ == "__main__":
    agent = Chatagent()
    while True:
        question = input("Pose ta question :\n")
        if question.lower() in ("exit", "quit"):
            break
        response = agent.ask_llm(question)
        print("\n" + response + "\n")
