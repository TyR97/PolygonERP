import os
"""
from docx import Document

class User:
    def __init__(self, name, job_title, base_pay, ):
        self.name = name
        self.job_title = job_title
        self.base_pay = base_pay

print("vvv")
u = User("Jani", "mérges", "egy kicsit")

doc = Document("employee_contract_template.docx")

for p in doc.paragraphs:
    if '{name}' in p.text:
        p.text = p.text.replace('{name}', u.name)
    if '{job_title}' in p.text:
        p.text = p.text.replace('{job_title}', u.job_title)
    if '{base_pay}' in p.text:
        p.text = p.text.replace('{base_pay}', u.base_pay)
doc.save('modified_employee_contract.docx')
"""