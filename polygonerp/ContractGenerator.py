from docx import Document
import os
from datetime import datetime

class ContractGenerator:
    def __init__(self, user):
        self.user = user

    def generate_contract(self):
        path = "contract.docx"

        doc = Document(path)

        self.replace_placholder(doc, '{name}', self.user.name)
        self.replace_placholder(doc, '{job_title}', self.user.job_title)
        self.replace_placholder(doc, '{base_pay}', self.user.base_pay)
        self.replace_placholder(doc, '{start_date}', datetime.now().strftime("%m/%d/%Y"))

        contract_filename = f"{self.user.username}_contract.docx"
        contract_path = os.path.join('contracts', contract_filename)

        os.makedirs(os.path.dirname(contract_path), exist_ok=True)

        doc.save(contract_path)
        print(f"Contract saved to: {contract_path}")

    def replace_placholder(self, doc, placeholder, replacement):
        for paragraph in doc.paragraphs:
            if placeholder in paragraph.text:
                inline = paragraph.runs
                for run in inline:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, replacement)

