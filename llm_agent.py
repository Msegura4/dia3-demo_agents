from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def ask_llm(messages_history):
    client = Groq(api_key=os.environ["GROQ_KEY"])

    messages = [{"role": "system", "content": read_file(file_path="./context.txt")}]
    messages += messages_history

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-120b",
        include_reasoning=False,
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    messages_history = []
    while True:
        question = input("Pose ta question :\n")
        if question.lower() in ("exit", "quit"):
            break
        messages_history.append({"role": "user", "content": question})
        response = ask_llm(messages_history)
        messages_history.append({"role": "assistant", "content": response})
        print("\n" + response + "\n")
