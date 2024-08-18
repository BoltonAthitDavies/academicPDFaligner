from openai import OpenAI # openai==1.2.0
import requests
import spacy
from spacy.symbols import ORTH
from spacy.tokens import Token
from spacy import util
from PyPDF2 import PdfReader, PdfWriter
from html.parser import HTMLParser

api_key = "up_peUjBLvnUYMe2yGnpFZWBjpG2hh1i"
input_filename = ".\\CIS_Grad_Template__Dev_.pdf"
input_filename = ".\\Improving MPI Threading Support for Current Hardware Architecture.pdf"
 
url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
headers = {"Authorization": f"Bearer {api_key}"}
files = {"document": open(input_filename, "rb")}
data = {"ocr": True}
response = requests.post(url, headers=headers, files=files, data=data).json()
# print(response)

output_filename = "invoice.html"
html = response["html"]
hope = str(html)

# print(str(html))
 
with open(output_filename,"w", encoding="utf-8") as file:
    file.write(hope)
# method1
# # nlp = spacy.load("en_core_web_trf")
# nlp = spacy.load("en_core_web_sm")

# infixes = nlp.Defaults.infixes + [r'(<)']
# # nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
# # nlp.tokenizer.add_special_case(f"<i>", [{ORTH: f"<i>"}])    
# # nlp.tokenizer.add_special_case(f"</i>", [{ORTH: f"</i>"}])    

# text = """Hello, <i>world</i> !"""
# text = f"""{hope}"""

# doc = nlp(text)
# false_token = [e.text for e in doc]
# print(false_token)
# print(false_token[40740:40748])
# print(f'Length of false_token: {len(false_token)}')