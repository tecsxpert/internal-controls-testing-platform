import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 5 test inputs
test_inputs = [
    "Access control review for employee login system",
    "Monthly bank reconciliation process check",
    "Inventory count verification procedure",
    "Vendor payment approval workflow audit",
    "IT system backup and recovery testing"
]

def test_prompt(input_text):
    with open("prompts/describe.txt", "r") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.replace("{input}", input_text)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Test all 5 inputs
for i, input_text in enumerate(test_inputs, 1):
    print(f"\n--- Test {i} ---")
    print(f"Input: {input_text}")
    print(f"Output: {test_prompt(input_text)}")
    print("---------------")