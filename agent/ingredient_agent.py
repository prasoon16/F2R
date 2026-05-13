import base64
import os

from groq import Groq

class IngredientAgent():
    def __init__(self):
        self.agent = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def encode_image(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode("utf-8")
    def extract_ingredients_from_image_groq(self, image_bytes: bytes, image_ext: str) -> str:
        image_data = self.encode_image(image_bytes)
        ext = image_ext.split(".")[-1].lower()
        media_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

        response = self.agent.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # best free vision model on groq
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """Look at this fridge image carefully.
    List every food ingredient you can see.
    Return ONLY a comma-separated list, nothing else.
    Example: eggs, milk, tomatoes, cheddar cheese, butter"""
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

