import os
import nltk
nltk.download('punkt')
from nltk import sent_tokenize

def mergeSumm():
    
    if not os.path.isdir("Data/Merged-final/bart_wMVC_ACD"):
        os.mkdir("Data/Merged-final/bart_wMVC_ACD")

    for file in os.listdir("Data/Section-wise-summaries/bart_Abstract"):
        if not file.startswith('.'):
            summary = ""
            with open(f"Data/Section-wise-summaries/bart_Abstract/{file}","r") as f:
                summary+=f.read()+'\n\n'
            with open(f"Data/Section-wise-summaries/bart_Conclusions/{file}","r") as f:
                init_text = f.read()
                for sent in sent_tokenize(init_text):
                    if len(summary.split())>100:
                        break
                    summary+=sent+'\n\n'    
            with open(f"Data/Section-wise-summaries/bart_Discussion/{file}","r") as f:
                init_text = f.read()
                for sent in sent_tokenize(init_text):
                    if len(summary.split())>100:
                        break
                    summary+=sent+'\n\n'  
            with open(f"Data/Section-wise-summaries/bart_Introduction/{file}","r") as f:
                init_text = f.read()
                for sent in sent_tokenize(init_text):
                    if len(summary.split())>100:
                        break   
                    summary+=sent+'\n\n'         
            with open(f"Data/Merged-final/bart_wMVC_ACD/{file}","w") as f:
                f.write(summary)
            