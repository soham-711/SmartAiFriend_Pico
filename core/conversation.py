# from transformers import BlenderbotSmallTokenizer, BlenderbotSmallForConditionalGeneration
# from config import MODEL_NAME

# class ConversationEngine:
#     def __init__(self):
#         self.tokenizer = BlenderbotSmallTokenizer.from_pretrained(MODEL_NAME)
#         self.model = BlenderbotSmallForConditionalGeneration.from_pretrained(MODEL_NAME)
#         self.history = [{
#             "role": "system",
#             "content": (
#                 "You are Pico, a friendly AI companion. Respond conversationally with:\n"
#                 "1. Natural follow-up questions\n"
#                 "2. Occasional humor when appropriate\n"
#                 "3. Concise but thoughtful answers\n"
#                 "4. Context awareness from previous messages"
#             )
#         }]

#     def generate(self, user_input: str) -> str:
#         try:
#             self.history.append({"role": "user", "content": user_input})
#             inputs = self.tokenizer([user_input], return_tensors="pt", truncation=True, max_length=128)
#             reply_ids = self.model.generate(**inputs, max_length=200)
#             response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
#             self.history.append({"role": "assistant", "content": response})
#             return response
#         except Exception as e:
#             return f"Let's talk about something else. (error: {e})"



import ollama

class ConversationEngine:
    def __init__(self, model="phi3:medium"):
        self.model = model
    # core/conversation.py - REPLACE THE ENTIRE SYSTEM PROMPT

        self.history = [
    {
        "role": "system",
        "content": (
            "You are Pico, a friendly and curious AI companion. Respond like a close friend who's genuinely interested in the user's life. "
            "Keep your answers conversational and concise (1-2 sentences max).\n\n"
            
            "**Natural Response Pattern:**\n"
            "1. Briefly acknowledge what they said with empathy or excitement\n"
            "2. Ask a thoughtful follow-up question to learn more\n"
            "3. Optionally share a very short related experience or thought\n\n"
            
            "**Examples of good responses:**\n"
            "- 'That sounds amazing! How did you get started with that?'\n"
            "- 'Oh no, that's frustrating. What happened next?'\n"
            "- 'I love that too! What's your favorite part about it?'\n\n"
            
            "**Crucial:** Never use labels like 'Acknowledge/React' or 'B: Ask a Question'. "
            "Just have a natural, flowing conversation using the pattern intuitively."
        )
    }
]

        # 🔥 Warm-up (so first response is instant)
        try:
            ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": "warmup"}],
                options={"num_predict": 1}  # very fast warmup
            )
        except Exception:
            pass

    def generate(self, user_input: str) -> str:
        try:
            # Add user input to history
            self.history.append({"role": "user", "content": user_input})

            # Stream response from Ollama
            stream = ollama.chat(
                model=self.model,
                messages=self.history,
                options={"num_predict": 80},  # limit reply length for speed
                stream=True
            )

            reply = ""
            for chunk in stream:
                content = chunk["message"]["content"]
                reply += content
                print(content, end="", flush=True)  # prints as Pico types

            print()  # new line after streaming

            # Save assistant reply to history
            self.history.append({"role": "assistant", "content": reply})

            return reply
        except Exception as e:
            return f"Let's talk about something else. (error: {e})"
