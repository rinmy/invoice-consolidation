from docquery import document
from docquery.transformers_patch import pipeline
import os

output_file="data/HVQ/Discovery-Tower-Apartment-Service-Charge/Management-Fees/management-fees.csv"
mode = 'a' if os.path.exists(output_file) else 'w'
output= open(output_file, mode)

pipe = pipeline('document-question-answering')

dir_path = "data/HVQ/Discovery-Tower-Apartment-Service-Charge/Management-Fees"

for root,d_names,f_names in os.walk(dir_path):
    for file in f_names:
        file_path=os.path.join(root, file)
        metadata_file=os.path.join(root, "metadata.txt")
        if file_path.endswith("pdf") or file_path.endswith("PDF"):
            doc = document.load_document(file_path)
            output_str = "{}\t".format(file_path)
            with open(metadata_file) as f:
                for line in f.readlines():
                    columns=line.split("=")
                    for column in columns:
                        if not column.startswith("Column"):
                            max_score=.0
                            max_model=None
                            questions = column.split(",")
                            for question in questions:
                                result = pipe(question=question.strip(), ** doc.context).pop()
                                if(result['score'] > max_score):
                                    max_score = result['score']
                                    max_model = result
                            output_str+="{}\t".format(max_model['answer'])
                output_str+="\n"
                output.write(output_str)
                output.flush()

output.close()