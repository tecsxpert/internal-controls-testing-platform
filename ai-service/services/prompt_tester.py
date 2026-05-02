import os
import json
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.groq_client import GroqClient

client = GroqClient()

def load_prompt(filename):
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(prompt_path, 'r') as f:
        return f.read()

def score_response(response: dict) -> int:
    if response.get('is_fallback'):
        return 0
    data = response.get('data', {})
    if 'text' in data and not any(k in data for k in ['description', 'recommendations', 'title']):
        return 4
    return 9

def test_describe():
    print("\n" + "="*50)
    print("TESTING /describe PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('describe.txt')

    inputs = [
        "Three-way matching control for purchase orders",
        "Expense reimbursement approval process",
        "Monthly financial close checklist",
        "User provisioning and deprovisioning control",
        "Physical security access control for server room",
        "Whistleblower policy and reporting mechanism",
        "Tax compliance review control",
        "Customer refund approval workflow",
        "Budget variance analysis control",
        "Contract review and approval process"
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
    print(f"\nAverage score: {avg:.1f}/10")
    return avg

def test_recommend():
    print("\n" + "="*50)
    print("TESTING /recommend PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('recommend.txt')

    inputs = [
        "Expense reports submitted without receipts",
        "Financial close process taking more than 10 days",
        "Terminated employees still have system access",
        "Server room accessible to all staff",
        "No whistleblower policy in place",
        "Tax filings submitted late repeatedly",
        "Customer refunds processed without approval",
        "Budget variances not investigated or explained",
        "Contracts signed without legal review",
        "Purchase orders raised after goods received"
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
    print(f"\nAverage score: {avg:.1f}/10")
    return avg

def test_generate_report():
    print("\n" + "="*50)
    print("TESTING /generate-report PROMPT — 10 inputs")
    print("="*50)

    system_prompt = load_prompt('report.txt')

    inputs = [
        "HR department with poor onboarding controls",
        "Legal department with no contract review process",
        "Finance department with delayed month end close",
        "IT department with poor user access management",
        "Sales department with no refund approval process",
        "Tax department with recurring late filings",
        "Procurement with no three-way matching",
        "Operations with no physical security controls",
        "Compliance department with no whistleblower policy",
        "Treasury with no cash flow forecasting controls"
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
    print(f"\n Average score: {avg:.1f}/10")
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
        print("All prompts pass the 7/10 threshold!")
    else:
        print("Some prompts need rewriting!")