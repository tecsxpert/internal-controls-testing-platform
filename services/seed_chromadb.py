import json
import os

# 10 domain knowledge documents
documents = [
    {"id": "doc_0", "content": "Access control reviews ensure only authorized personnel can access systems and data."},
    {"id": "doc_1", "content": "Bank reconciliation is a process of matching internal records with bank statements monthly."},
    {"id": "doc_2", "content": "Inventory count verification involves physically counting stock and comparing with system records."},
    {"id": "doc_3", "content": "Vendor payment approval requires multiple levels of authorization before processing payments."},
    {"id": "doc_4", "content": "IT backup and recovery testing ensures data can be restored in case of system failure."},
    {"id": "doc_5", "content": "Segregation of duties prevents fraud by ensuring no single person controls all parts of a transaction."},
    {"id": "doc_6", "content": "Change management controls ensure all system changes are properly tested and approved before deployment."},
    {"id": "doc_7", "content": "Physical security controls restrict unauthorized access to facilities and sensitive areas."},
    {"id": "doc_8", "content": "Data encryption protects sensitive information from unauthorized access during storage and transmission."},
    {"id": "doc_9", "content": "Audit logging tracks all user activities and system changes for compliance and investigation purposes."}
]

# Save to JSON file
output_path = "services/knowledge_base.json"
with open(output_path, "w") as f:
    json.dump(documents, f, indent=2)

print(f"Successfully seeded knowledge base with {len(documents)} documents!")
for doc in documents:
    print(f"  {doc['id']}: {doc['content'][:60]}...")