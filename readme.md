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

BibTeX:
```tex
@inproceedings{chaturvedi-etal-2020-divide,
    title = "Divide and Conquer: From Complexity to Simplicity for Lay Summarization",
    author = "Chaturvedi, Rochana  and
      Saachi  and
      Dhani, Jaspreet Singh  and
      Joshi, Anurag  and
      Khanna, Ankush  and
      Tomar, Neha  and
      Duari, Swagata  and
      Khurana, Alka  and
      Bhatnagar, Vasudha",
    booktitle = "Proceedings of the First Workshop on Scholarly Document Processing",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.sdp-1.40/",
    doi = "10.18653/v1/2020.sdp-1.40",
    pages = "344--355",
    abstract = "We describe our approach for the 1st Computational Linguistics Lay Summary Shared Task CL-LaySumm20. The task is to produce non-technical summaries of scholarly documents. The summary should be within easy grasp of a layman who may not be well versed with the domain of the research article. We propose a two step divide-and-conquer approach. First, we judiciously select segments of the documents that are not overly pedantic and are likely to be of interest to the laity, and over-extract sentences from each segment using an unsupervised network based method. Next, we perform abstractive summarization on these extractions and systematically merge the abstractions. We run ablation studies to establish that each step in our pipeline is critical for improvement in the quality of lay summary. Our approach leverages state-of-the-art pre-trained deep neural network based models as zero-shot learners to achieve high scores on the task."
}
```
