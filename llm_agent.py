from groq import Groq
from dotenv import load_dotenv
import os
import base64


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    def ask_llm(self, text_interaction, image_bytes=None, image_type=None):
        model = "qwen/qwen3.8-27b"

        if image_bytes is not None:
            content = [
                {"type": "text", "text": text_interaction},
                {"type": "image_url", "image_url": {"url": f"data:{image_type};base64,{self.encode_image(image_bytes)}"}}
            ]
        else:
            content = text_interaction

        self.update_conversation_history(role="user", content=content)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model=model,
            include_reasoning=False,
        ).choices[0].message.content

        self.update_conversation_history(role="assistant", content=response)


    def transcribe(self, audio_bytes):
      transcription = self.groq_client.audio.transcriptions.create(
          file=("audio.wav", audio_bytes, "audio/wav"),
          model="whisper-large-v3",
      )
      return transcription.text


    @staticmethod
    def encode_image(image_bytes):
        return base64.b64encode(image_bytes).decode("utf-8")


if __name__ == "__main__":
    question = input("Pose ta question :\n")
    response = ask_llm(question)
    print("\n")
    print(response)
