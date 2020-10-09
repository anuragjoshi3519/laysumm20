import re
from nltk.tokenize import sent_tokenize

filter_chars = {'¥','©','¬','®','°','±','¼','Á','Å','Æ','Ç','É','Ñ','Ó','Ö','×','ß','à','á','â','ã','ä','å','æ','ç','è','é','ê','ë','í',
 'î','ï','ñ','ò','ó','ô','õ','ö','ø','ú','ü','ý','ā','ą','ć','Č','č','ē','ĕ','ė','ě','ğ','ħ','ı','ĺ','Ł','ł','ń','ņ',
 'ň','ō','Ř','І','В','С','ř','ś','Ş','ş','Š','š','ť','ū','ŭ','ů','ų','Ż','Ž','ž','ǧ','ǫ','ș','ə','ˆ','ˇ','˙','˜','́','̂','̃','̄',
 '̈','Γ','Δ','Θ','Λ','Π','Σ','Φ','Χ','Ψ','Ω','α','β','γ','δ','ε','ζ','η','θ','κ','λ','μ','ν','ξ','π','ρ','σ','τ','υ',
 'φ','χ','ψ','ω','ϑ','ϕ','ϱ','ϵ','ḯ','‖','†','…','‰','′','″','€', '⃖', '⃗','ℓ','ℜ','™','←','↑','→','↓','↦','⇀','⇒','⇔',
 '⇢','∀','∂','∃','∅','∆','∇','∈','∉','∏','∑','∘','∙','∝','∞','∠','∣','∥','∧','∨','∩','∪','∫','∭','∼','≃','≅','≈','≔','≜',
 '≠','≡','≤','≥','≪','≫','≲','≳','⊂','⊆','⊕','⊖','⊗','⊙','⋀','⋁','⋂','⋃','⋅','⋆','⋒','⋮','⋯','⌊','⌋','□','△','▽','♯',
 '✔','➔','⟶','⟹','⩽','⩾','⪰','〈','〉','丙','东','作','六','务','印','厂','合','塘','大','子','宁','宅','宝','宫','尚','局',
 '峰','府','建','承','汪','浦','船','药','路','辰','铜','食','︷','︸','＋','−','{','}'
 ,'ˆ',':','[',']','+','=','*','<','>','^','/','-','–','&','#'}



def preprocessed_text(txt,keep_parenthesis=False):
    
    # remove links, if any  
    txt = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*', '', txt, flags=re.MULTILINE)
    
    # remove references, if any
    txt = re.sub(r"\s\([A-Z][a-z]+,\s[A-Z][a-z]?\.[^\)]*,\s\d{4}\)", "", txt)
    
    # replace multiple spaces with a single space
    txt = re.sub(r" +"," ", txt, flags = re.I)      
    
    txt = txt.replace("tab.","table ")       
    txt = txt.replace("Tab.","Table ") 
    txt = txt.replace("Fig.","Figure ")       
    txt = txt.replace("fig.","figure ")
    txt = txt.replace("eq.","equation ")
    txt = txt.replace("Eq.","Equation ")
    txt = txt.replace("etal.", "et al ")
    txt = txt.replace("et al.", "et al ")
    txt = txt.replace("pp.", "pp ")
    txt = txt.replace("i.e.", "ie ")
    txt = txt.replace("e.g.", "example ")
    txt = txt.replace("ref.", "ref ")
    txt = txt.replace("Ref.", "Ref ")
    txt = txt.replace("etc.", "etcetera ")
    txt = txt.replace("Figs.", "Figures ")
    txt = txt.replace("figs.", "figures ")
    txt = txt.replace("No.", "Number ")
    txt = txt.replace("eqs.", "equations ")
    
    # '. singlelowercasechar' -> '.singlelowercasechar' 
    txt = re.sub(r'(?<=[\.])\s+(?=(?:[a-z|[0-9]))', '', txt)
    
    # converting patterns: ab.a -> ab a,   b.1 -> b 1,   A.F -> A F,   word.something -> word something 
    for pattern in re.findall(r"[a-zA-Z]\.[a-zA-Z0-9]",txt ):
        txt = txt.replace(pattern,f"{pattern.split('.')[0]} {pattern.split('.')[1]}")
    
    
    # this and next line of code ensures that lines with single word (PARAGRAPH, SECTION,etc.)
    # have fullstop after they end, so that they are not included in any sentence.
    txt = re.sub(r"\n+",". \n\n",txt) 
    txt = re.sub(r"\.+",".",txt)      

    
    # For each sentence in text we count the number of all the words with any of the above mentioned
    # character(filter_chars) in it. And if in a sentence more than 20% of such words are found then
    # that sentence is removed from text.
    sents = sent_tokenize(txt)
    final_txt = ''
    for sent in sents:
        word_count=0
        for word in sent.split():
            for char in word: 
                if char in filter_chars:
                    word_count+=1
                    break
        if word_count/len(sent.split())<0.2:
            final_txt+=sent+' \n\n'
            
    #remove content between curly braces       
    final_txt = re.sub(r'\{.*?\}',' ', final_txt) 
    
    # removing square brackets
    final_txt = re.sub(r'\[.*?\]', ' ', final_txt)
    
    if keep_parenthesis==False:         

        # removing parenthesis
        final_txt = re.sub(r'\(.*?\)', ' ', final_txt)
        
        punctuation = "\"#$&\'()-/:;@[\\]_`~'“”´ʼ‘’{|}+*^=><−"
    
    if keep_parenthesis==True:  
        
        # removing parenthesis with no alpha numeric character except (abcijkmnpqrtxy)
        final_txt = re.sub('\(([0-9+-/*^><=&$#@%.,!{} abcijkmnpqrtxyABCIJKMNPQRTXY]*)\)', ' ', final_txt)

        punctuation = "\"#$&\'-/:;@\\_`~'“”´ʼ‘’{|}[]+*^=><−"
        
    # removes punctuation  
    final_txt = "".join([c if c not in punctuation and c not in filter_chars else " " for c in final_txt])
    #removing extra spaces
    final_txt = re.sub(r" +"," ", final_txt, flags = re.I)
    
    return final_txt