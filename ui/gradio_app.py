import gradio as gr
import asyncio

from backend.app.services.chatroom_service import ChatRoom

chatroom = ChatRoom()

# def chat(input_text, history):
#     asyncio.run(chatroom.run_turn(input_text))

#     messages = []
#     for msg in chatroom.get_history():
#         if msg.role == "human":
#             messages.append({"role": "user", "content": msg.content})
#         elif msg.role in ["nietzsche", "dostoevsky"]:
#             messages.append({"role": "assistant", "content": msg.content})

#     return messages

def chat(input_text, history):
    import asyncio
    asyncio.run(chatroom.run_turn(input_text))

    formatted_messages = []

    for msg in chatroom.get_history():
        if msg.role == "human":
            formatted_messages.append({"role": "user", "content": msg.content})
        elif msg.role in ["nietzsche", "dostoevsky"]:
            # Assign colors
            if msg.role == "nietzsche":
                speaker_name = "Nietzsche"
                color = "red"
            else:
                speaker_name = "Dostoevsky"
                color = "blue"

            # Wrap text in HTML for color
            content_html = f"<b style='color:{color}'>{speaker_name}:</b> {msg.content}"

            formatted_messages.append({"role": "assistant", "content": content_html})

    return formatted_messages


with gr.Blocks() as demo:
    gr.Markdown("# The Examining of Life ")
    gr.Markdown("Debate between Me, Nietzsche and Dostoevsky. Use commands like `/ask nietzsche` or `/debate`.")

    chatbot = gr.Chatbot()
    textbox = gr.Textbox(placeholder="Type a command or question...")

    textbox.submit(chat, [textbox, chatbot], chatbot)

demo.launch()


if __name__ == "__main__":
    demo.launch()
