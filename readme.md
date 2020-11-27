Proposed solution model for [LaySumm (The 1st Computational Linguistics Lay Summary Challenge Shared Task)](https://competitions.codalab.org/competitions/25516)
The task is to create non-technical summaries of scholarly text.

### Directory Structure:

    1 Data - includes all data for the model

        1.1 Input-Data              - includes original full-text & abstract files for all documents
        1.1 Sections-DataFrame      - includes csv file containing all documents text (section wise)
        1.1 Input-wMVC              - includes input documents for the wMVC model
        1.1 Input-BART              - includes input documents for the BART model
        1.1 Section-wise-summaries  - includes summaries for all sections (output of BART model)
        1.1 Merged-final            - includes final merged summaries

    2 Utilities - includes utility python scripts

        2.1 prepare_data.py          - python script for preparing section-wise preprocessed folders
                                        (in Input-wMVC) to be used as input data for wMVC model.

        2.2 preprocess_data.py       - python script for preprocessing input document text

        2.3 merge_summaries.py       - python script for merging section-wise summaries (taking input
                                        from the Section-wise-summaries folder, and saving final
                                        summaries in Merged-final folder)

    3 BART - includes code for generating abstractive summaries using BART model

    4 wMVC - includes code for generating extractive summaries using wMVC model

    5 requirements.txt

### Generate Laysumm Summaries:

#### Steps:

1. Clone the repository and move to the cloned repository:

```bash
git clone https://github.com/anuragjoshi3519/laysumm20
cd laysumm20
```

2. Create virtual environment and install dependencies:

```bash
pip3 install virtualenv
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip3 install -r requirements.txt
python3 -c "from nltk import download; download(['punkt', 'stopwords'])"
```

2. Add test documents (full_texts & abstracts for every document) in Data/Input-Data (first remove default sample_ABSTRACT.txt and sample_FULLTEXT.txt files)

3. Generate summaries for the test documents:

```bash
python3 generateLaysumm.py
```

**Generated summaries can be found in Data/Merged-final folder.**

### Cite:

If you find the work useful, please cite it as:

```
BibTeX:
@inproceedings{chaturvedi2020divide,
  title={Divide and Conquer: From Complexity to Simplicity for Lay Summarization},
  author={Chaturvedi, Rochana and Dhani, Jaspreet Singh and Joshi, Anurag and Khanna, Ankush and Tomar, Neha and Duari, Swagata and Khurana, Alka and Bhatnagar, Vasudha and others},
  booktitle={Proceedings of the First Workshop on Scholarly Document Processing},
  pages={344--355},
  year={2020}
}
```
