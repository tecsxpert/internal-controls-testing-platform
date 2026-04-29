import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    try:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "hi, how are you?"}
            ],
            temperature=0.3,
            max_tokens=100
        )

        print("\n✅ Groq API Working!\n")
        print("Response:\n")
        print(response.choices[0].message.content)

    except Exception as e:
        print("\n❌ Error testing Groq API:")
        print(e)


if __name__ == "__main__":
    test_groq()