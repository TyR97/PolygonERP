from docx import Document

def create_contract(user):
    doc = Document("employee_contract_template.docx")

    placeholders = {
        '{name}': user.name,
        '{maiden_name}': user.maiden_name,
        '{mothers_name}': user.mothers_name,
        '{pob}': user.pob,
        '{dob}': str(user.dob),
        '{address}': str(user.address),
        '{tax_num}': str(user.tax_num),
        '{taj_number}': str(user.taj_number),
        '{job_title}': user.job_title,
        '{base_pay}': str(user.base_pay)
    }

    for paragraph in doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    doc.save(f"{user.name}_contract.docx")