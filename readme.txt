1 Directory Structure:

    1.1 Data - includes all data for the model

        1.1.1 Input-Data              - includes original full-text & abstract files for all documents
        1.1.2 Sections-DataFrame      - includes csv file containing all documents text (section wise)
        1.1.3 Input-wMVC              - includes input documents for the wMVC model
        1.1.4 Input-BART              - includes input documents for the BART model
        1.1.5 Section-wise-summaries  - includes summaries for all sections (output of BART model)
        1.1.6 Merged-final            - includes final merged summaries
    
    1.2 Utilities - includes utility python scripts
        
        1.2.1 prepare_data.py          - python script for preparing section-wise preprocessed folders 
                                        (in Input-wMVC) to be used as input data for wMVC model.
                                        
        1.2.2 preprocess_data.py       - python script for preprocessing input document text
        
        1.2.3 merge_summaries.py       - python script for merging section-wise summaries (taking input 
                                        from the Section-wise-summaries folder, and saving final summaries 
                                        in Merged-final folder)
                                        
    1.3 BART - includes code for generating abstractive summaries using BART model
    
    1.4 wMVC - includes code for generating extractive summaries using wMVC model
    
    1.5 requirements.txt
    

2 Procedure to follow (for generating Laysumm summaries):

    2.1 Add test data (full_texts & abstracts for every document) in Input-Data folder
    
    2.2 Go to Utilities folder & run:  python3 prepare_data.py
    
        - It will generate input data for wMVC model (will be stored in Input-wMVC folder)
    
    2.3 Go to wMVC folder & run:  python3 generate_wMVC_summ.py
    
        - It will generate extractive summaries for all sections to be used as input for BART
          model (will be stored in Input-BART folder)
    
    2.4 Go to BART folder & run:  python3 generate_bart_summ.py
    
        - It will generate section-wise summaries (will be stored in Section-wise-summaries folder)
    
    2.5 Go to Utilities folder & run:  python3 merge_summaries.py
    
        - It will take bart generated section-wise summaries and merge them to make final laysum 
          summaries (will be stored in Merged-final folder).
