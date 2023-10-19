import os
import PyPDF2
import re
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")


pdf_summary_text = ""

pdf_file_path = "pdfs/Mustafa Kemal Atatürk - Cumali Ordugahı Tabiye ve Tatbikat Seyahati.pdf"

pdf_file = open(pdf_file_path, "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file)
for page_num in range(len(pdf_reader.pages)):
    page_text = pdf_reader.pages[page_num].extract_text().lower()

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful research assistant"},
            {"role": "user", "content": f"Briefly summarize this: {page_text}"},
        ],
    )
    page_summary = response["choices"][0]["message"]["content"]
    pdf_summary_text += page_summary + "\n"
    pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")
    with open(pdf_summary_file, "w+") as file:
        file.write(pdf_summary_text)

pdf_file.close()


with open(pdf_summary_file, "r") as file:
    print(file.read())