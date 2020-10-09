import os
import numpy
import pandas as pd
import nltk
nltk.download('punkt')
from nltk import sent_tokenize, word_tokenize
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

def get_summary(doc, model_bart, tokenizer_bart):
    
    if len(doc.split())<2:
        return ""
    
    inputs = tokenizer_bart.encode(doc,max_length = tokenizer_bart.model_max_length,
                                   truncation=True,
                                   truncation_strategy='do_not_truncate',
                                   return_tensors='pt')

    print(f" Sub-Tokenized input length: {len(inputs[0])}")
    
    outputs = model_bart.generate(inputs,do_sample = False,num_beams=5,early_stopping=False) 
    
    summary = [tokenizer_bart.decode(g,skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in outputs]
    
    print(f"Summary Generated | Output length: {len(summary[0].split())} | Sub-Tokenized output length: {len(outputs[0])}")

    return summary[0]

def create_summaries(src_path, dest_path, model_bart, tokenizer_bart):
    
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
        
    count = 1
    
    for doc in os.listdir(src_path):
        if doc not in os.listdir(dest_path):
            if not doc.startswith('.'):
                with open(src_path+doc,'r') as f:
                    text = f.read()
                    print(f"Doc#{count}")
                    print(f"\nGenerating summary for {doc} | Input length: {len(text.split())} ",end="|")
                    summary = get_summary(text, model_bart, tokenizer_bart)
                    summary = ' \n\n'.join([token for token in sent_tokenize(summary)])

                with open(dest_path+doc,'w') as g:
                    g.write(summary)
        count+=1
        
def generate_bart_summ():
    
    model_bart = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer_bart = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    
    for section_folder in os.listdir("../Data/Input-BART"):
        if not section_folder.startswith('.'):
            create_summaries(src_path = f"../Data/Input-BART/{section_folder}/",dest_path=f"../Data/Section-wise-summaries/bart_{section_folder}/",model_bart = model_bart, tokenizer_bart=tokenizer_bart)
            
            
if __name__=='__main__':
    generate_bart_summ()
    