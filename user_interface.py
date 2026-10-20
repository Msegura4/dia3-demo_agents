import streamlit as st 
from llm_agent import ConversationAgent


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()


	def get_persistant_conversation_agent(self):
		
		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				content = message["content"]
				if isinstance(content, list):
					for block in content:
						if block["type"] == "text":
							st.markdown(block["text"])
						elif block["type"] == "image_url":
							st.image(block["image_url"]["url"])
				else:
					st.markdown(content)


	def run(self):
		text_interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=True,
			accept_audio=True
			)

		if text_interaction:
			image_bytes = None
			image_type = None

			if text_interaction.files:
				uploaded_file = text_interaction.files[0]
				image_bytes = uploaded_file.read()
				image_type = uploaded_file.type

			if text_interaction.audio is not None:
				audio_bytes = text_interaction.audio.read()
				text_interaction = self.conversation_agent_object.transcribe(audio_bytes)
			else:
				text_interaction = text_interaction.text

			self.conversation_agent_object.ask_llm(text_interaction, image_bytes=image_bytes, image_type=image_type)
			self.show_discussion_history()



if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()








































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


