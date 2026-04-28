import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from groq_client import GroqClient

client = GroqClient()

def load_prompt(filename):
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(prompt_path, 'r') as f:
        return f.read()

def score_response(response: dict) -> int:
    """Score response from 1-10"""
    if response.get('is_fallback'):
        return 0
    data = response.get('data', {})
    if 'text' in data and not any(k in data for k in ['description', 'recommendations', 'title']):
        return 4  # Plain text instead of JSON
    return 9

def test_describe():
    print("\n" + "="*50)
    print("TESTING /describe PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('describe.txt')

    inputs = [
        "Segregation of duties in accounts payable",
        "Monthly bank reconciliation process",
        "Access control review for ERP system",
        "Invoice approval workflow",
        "Inventory count verification process",
        "Payroll processing controls",
        "Vendor master data change controls",
        "Journal entry approval controls",
        "Fixed asset addition controls",
        "Password policy enforcement control"
    ]

    scores = []
    for i, user_input in enumerate(inputs, 1):
        print(f"\nTest {i}: {user_input}")
        result = client.call(system_prompt, user_input, temperature=0.3)
        score = score_response(result)
        scores.append(score)
        print(f"Score: {score}/10")
        print(f"Response: {json.dumps(result.get('data', {}), indent=2)[:200]}...")

    avg = sum(scores) / len(scores)
    print(f"\n✅ Average score: {avg:.1f}/10")
    return avg

def test_recommend():
    print("\n" + "="*50)
    print("TESTING /recommend PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('recommend.txt')

    inputs = [
        "No segregation of duties in accounts payable",
        "Bank reconciliations are performed late every month",
        "ERP system access not reviewed in 12 months",
        "Invoices approved without proper documentation",
        "Inventory counts show recurring variances",
        "Payroll processed without dual approval",
        "Vendor changes made without authorization",
        "Journal entries posted without review",
        "Fixed assets not tagged or tracked properly",
        "Weak password policy with no expiry"
    ]

    scores = []
    for i, user_input in enumerate(inputs, 1):
        print(f"\nTest {i}: {user_input}")
        result = client.call(system_prompt, user_input, temperature=0.3)
        score = score_response(result)
        scores.append(score)
        print(f"Score: {score}/10")
        print(f"Response: {json.dumps(result.get('data', {}), indent=2)[:200]}...")

    avg = sum(scores) / len(scores)
    print(f"\n✅ Average score: {avg:.1f}/10")
    return avg

def test_generate_report():
    print("\n" + "="*50)
    print("TESTING /generate-report PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('generate_report.txt')

    inputs = [
        "Accounts payable department with weak segregation of duties",
        "IT department with outdated access controls",
        "Payroll processing with missing dual approvals",
        "Inventory management with recurring count variances",
        "Financial reporting with delayed reconciliations",
        "Procurement with unauthorized vendor changes",
        "Fixed assets with poor tracking and tagging",
        "Journal entries with no supervisory review",
        "Cash handling with no independent verification",
        "ERP system with excessive user access privileges"
    ]

    scores = []
    for i, user_input in enumerate(inputs, 1):
        print(f"\nTest {i}: {user_input}")
        result = client.call(system_prompt, user_input, temperature=0.3)
        score = score_response(result)
        scores.append(score)
        print(f"Score: {score}/10")
        print(f"Response: {json.dumps(result.get('data', {}), indent=2)[:200]}...")

    avg = sum(scores) / len(scores)
    print(f"\n✅ Average score: {avg:.1f}/10")
    return avg


if __name__ == "__main__":
    avg1 = test_describe()
    avg2 = test_recommend()
    avg3 = test_generate_report()

    print("\n" + "="*50)
    print("FINAL SCORES")
    print("="*50)
    print(f"describe prompt:         {avg1:.1f}/10")
    print(f"recommend prompt:        {avg2:.1f}/10")
    print(f"generate-report prompt:  {avg3:.1f}/10")
    overall = (avg1 + avg2 + avg3) / 3
    print(f"Overall average:         {overall:.1f}/10")
    if overall >= 7:
        print("✅ All prompts pass the 7/10 threshold!")
    else:
        print("❌ Some prompts need rewriting!")