from openai import OpenAI # openai==1.2.0
import requests
import spacy
from spacy.symbols import ORTH
from spacy.tokens import Token
from spacy import util
from PyPDF2 import PdfReader, PdfWriter
from html.parser import HTMLParser
import os
import json
# from spacy.tokenizer import Tokenizer
# from spacy.lang.tokenizer_exceptions import TOKEN_MATCH
# Token.set_extension('tag', default=False)

# method2
class MyHTMLTokenizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        self.tokens.append(("StartTag", tag, dict(attrs)))

    def handle_endtag(self, tag):
        self.tokens.append(("EndTag", tag))

    def handle_data(self, data):
        if data.strip():  # Ignore empty data
            self.tokens.append(("Data", data.strip()))

    def handle_comment(self, data):
        self.tokens.append(("Comment", data))

    def handle_entityref(self, name):
        self.tokens.append(("EntityRef", name))

    def handle_charref(self, name):
        self.tokens.append(("CharRef", name))

    def tokenize(self, html):
        self.feed(html)
        return self.tokens

def reconstruct_html(tokens):
    html = []
    for token in tokens:
        if token[0] == "StartTag":
            attrs = "".join(f' {k}="{v}"' for k, v in token[2].items())
            html += [f"<{token[1]}{attrs}>"]
        elif token[0] == "EndTag":
            html += [f"</{token[1]}>"]
        elif token[0] == "Data":
            html += [token[1]]
        elif token[0] == "Comment":
            html += [f"<!--{token[1]}-->"]
        elif token[0] == "EntityRef":
            html += [f"&{token[1]};"]
        elif token[0] == "CharRef":
            html += [f"&#{token[1]};"]
    return html

def split_pdf(input_pdf_path, output_folder):
    reader = PdfReader(input_pdf_path)
    os.makedirs(output_folder, exist_ok=True)
    for page_number in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number])
        
        output_pdf_path = f".\\{output_folder}\\page_{page_number + 1}.pdf"
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)
        print(f"Saved {output_pdf_path}")

if __name__ == "__main__":
    # initialize path
    api_key = "up_Xog15QwG0oCoojzgD5h9K9eR2jLU7"
    input_filename = ".\\CIS_Grad_Template__Dev_.pdf"
    input_filename = ".\\Improving MPI Threading Support for Current Hardware Architecture.pdf"

    #split pdf pages
    output_folder = "split_pages_pdf"
    split_pdf(input_filename, output_folder)

    os.makedirs("split_pages_html", exist_ok=True)
    for i in range(len(os.listdir(output_folder))):
        # analyze layout
        input_filename = f".\\{output_folder}\\page_{i + 1}.pdf"
        url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {"document": open(input_filename, "rb")}
        data = {"ocr": True}
        response = requests.post(url, headers=headers, files=files, data=data).json()
        # print(response)

        # # save html
        # output_filename = f".\\split_pages_html\\web_page_{i+1}.html"
        # html = response["html"]
        # hope = str(html)
        
        # with open(output_filename,"w", encoding="utf-8") as file:
        #     file.write(hope)
        
        os.makedirs("split_pages_json", exist_ok=True)
        with open(f'.\\split_pages_json\\upstage{i+1}.json', "w") as json_file:
            json.dump(response, json_file, indent=4)
        # html_code = f"""{hope}"""

        # tokenizer = MyHTMLTokenizer()
        # tokens = tokenizer.tokenize(html_code)
#BoltonAthitDavies
        # reconstructed_html = reconstruct_html(tokens)

        # # for i in range(20):
        # #     print(tokens[i])

        # # for i in range(20):
        # #     print(reconstructed_html[i])

        # print(reconstructed_html[:20])
