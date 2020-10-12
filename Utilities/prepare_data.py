from os import mkdir, listdir
from os.path import isdir

from pandas import read_csv, DataFrame
from nltk import sent_tokenize

from Utilities.preprocess_data import preprocessed_text


def removeLines(text: str) -> str:
    tokens = sent_tokenize(text)
    return ' \n\n'.join([token for token in tokens if len(token.split()) > 3])


def preprocess(text: str) -> str:
    text = text.strip()
    if text != '' and str.isalnum(text[-1]):
        text += '.'
    return text


def savefile(text: str, path: str):
    with open(path, 'w') as f:
        f.write(text)


def addNone(text: str) -> str:
    if len(text) == 0:
        return str('None.')
    else:
        return text


def makeSectionFolders():
    df = read_csv('Data/Sections-DataFrame/sections.csv', index_col='ID')

    for section in ['Abstract', 'Conclusions', 'Discussion', 'Introduction']:

        section_df = df[[section]]
        section_df.fillna('None.', inplace=True)

        section_df.loc[:, section] = section_df.loc[:, section].map(str).apply(
            lambda x: preprocessed_text(x, keep_parenthesis=True)).apply(removeLines)

        section_df.loc[:, section] = section_df.loc[:, section].apply(preprocess)
        section_df.loc[:, section] = section_df.loc[:, section].apply(addNone)

        if not isdir(f'Data/Input-wMVC/{section}/'):
            mkdir(f'Data/Input-wMVC/{section}/')

        for idx, inputs in zip(section_df.index, section_df.loc[:, section]):
            savefile(inputs, f'Data/Input-wMVC/{section}/{idx}.txt')


def getSectionDataFrames():
    # Folder must contain FULLTEXT & ABSTRACT files for each doc in it
    testset_path = 'Data/Input-Data/'

    testset_data = {
        'ID': [],
        'Prefix': [],
        'Title': [],
        'Full_Text': [],
        'Abstract': []
    }

    ID_set = set()

    for file in listdir(testset_path):
        if not file.startswith('.'):
            ID_set.add(file.split('_')[0])

    ID_set = list(ID_set)

    for ID in ID_set:
        testset_data['ID'].append(ID)
        for file in listdir(testset_path):
            if not file.startswith('.'):
                if file.split('_')[0] == ID:
                    if file.split('_')[1] == 'ABSTRACT':
                        with open(testset_path + file, 'r') as f:
                            testset_data['Prefix'].append(f.readline())
                            for _ in range(5):
                                f.readline()
                            testset_data['Title'].append(f.readline())
                            f.readline()
                            testset_data['Abstract'].append(' '.join(f.read().split('PARAGRAPH')[:]))

                    elif file.split('_')[1] == 'FULLTEXT':
                        with open(testset_path + file, 'r') as f:
                            for _ in range(8):
                                f.readline()
                            testset_data['Full_Text'].append(f.read())

    testdata_df = DataFrame(testset_data)

    # Getting separate sections from FULLTEXT

    introduction = []
    discussion = []
    conclusions = []

    for idx, fulltext in enumerate(testdata_df.iloc[:, 3]):
        intro = ''
        conc = ''
        disc = ''
        for text in fulltext.split('SECTION\n\n')[1:]:
            if 'introduction' in text.split('PARAGRAPH')[0].lower():
                intro = intro + ''.join(text.split('PARAGRAPH')[1:])

            elif 'discussion' in text.split('PARAGRAPH')[0].lower():
                disc = disc + ''.join(text.split('PARAGRAPH')[1:])

            elif 'conclusion' in text.split('PARAGRAPH')[0].lower():
                conc = conc + ''.join(text.split('PARAGRAPH')[1:])

        if intro == '':
            introduction.append(None)
        else:
            introduction.append(intro)

        if conc == '':
            conclusions.append(None)
        else:
            conclusions.append(conc)

        if disc == '':
            discussion.append(None)
        else:
            discussion.append(disc)

    testdata_df['Introduction'] = introduction
    testdata_df['Discussion'] = discussion
    testdata_df['Conclusions'] = conclusions

    # Saving DataFrame
    testdata_df.index = testdata_df.ID
    testdata_df.drop('ID', axis=1, inplace=True)
    testdata_df.to_csv('Data/Sections-DataFrame/sections.csv')


def prepareData():
    getSectionDataFrames()
    makeSectionFolders()
