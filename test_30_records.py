import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 30 demo records
demo_records = [
    "Access control review for employee login system",
    "Monthly bank reconciliation process check",
    "Inventory count verification procedure",
    "Vendor payment approval workflow audit",
    "IT system backup and recovery testing",
    "Segregation of duties review for finance team",
    "Change management process for software updates",
    "Physical security audit for server room",
    "Data encryption review for customer database",
    "Audit log review for system access",
    "Password policy compliance check",
    "Third party vendor risk assessment",
    "Financial statement review process",
    "Payroll processing controls audit",
    "Purchase order approval workflow review",
    "Network security controls assessment",
    "Disaster recovery plan testing",
    "User access rights periodic review",
    "Anti-fraud controls effectiveness review",
    "Compliance with data protection regulations",
    "Internal audit of expense reimbursement process",
    "Review of accounts payable controls",
    "Review of accounts receivable controls",
    "Fixed assets management controls review",
    "Tax compliance controls assessment",
    "Customer data privacy controls review",
    "Email security controls audit",
    "Software license compliance review",
    "Business continuity plan testing",
    "Risk assessment for new system implementation"
]

def test_describe(input_text):
    with open("prompts/describe.txt", "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.replace("{input}", input_text)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content

print(f"Testing {len(demo_records)} demo records...\n")
passed = 0
failed = 0

for i, record in enumerate(demo_records, 1):
    try:
        result = test_describe(record)
        print(f"✅ Record {i}: {record[:40]}...")
        passed += 1
    except Exception as e:
        print(f"❌ Record {i} FAILED: {e}")
        failed += 1

print(f"\n--- Results ---")
print(f"Passed: {passed}/30")
print(f"Failed: {failed}/30")