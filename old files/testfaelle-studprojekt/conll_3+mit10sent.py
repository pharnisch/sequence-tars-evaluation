import sys
import os
#sys.path.insert(0, os.path.join('C:/', 'Users', 'pharn', 'flair'))
#sys.path.insert(0, os.path.join('C:/', 'Users', 'pharn', 'AppData', 'Local', 'Packages', 'PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0', 'LocalCache', 'local-packages', 'Python38', 'site-packages'))
sys.path.insert(0, "/vol/fob-vol7/mi19/harnisph/flair")
sys.path.insert(0, os.path.join("vol", "fob-vol7", "mi19", "harnisph", "flair"))


import flair
from flair.data import Corpus
#from flair.datasets import TREC_6
from flair.models import SequenceTagger, TARSSequenceTagger, TARSSequenceTagger2
from flair.trainers import ModelTrainer
from flair.embeddings import WordEmbeddings, TransformerWordEmbeddings, TransformerDocumentEmbeddings
from flair.data import Sentence
from flair.data import MultiCorpus
from flair.datasets import MIT_MOVIE_NER_COMPLEX
flair.set_seed(1)

label_name_map = {
#"LOC":"Location","PER":"Person","ORG":"Organization","MISC":"Miscellaneous"
"Character_Name":"Character Name"
}

print(label_name_map)
corpus = MIT_MOVIE_NER_COMPLEX(tag_to_bioes=None, tag_to_bio2="ner", label_name_map=label_name_map)
corpus = corpus.downsample(0.002)

tag_type = "ner"
label_dictionary = corpus.make_label_dictionary(tag_type)
print(label_dictionary)

#embeddings = WordEmbeddings("glove")
#embeddings = TransformerWordEmbeddings()

tagger = TARSSequenceTagger2.load("resources/testfaelle-studproj/conll_3/final-model.pt")
#tagger = TARSSequenceTagger2(tag_dictionary=label_dictionary, tag_type=tag_type, task_name="TEST_NER")
#tagger = TARSSequenceTagger(tag_dictionary=label_dictionary, tag_type=tag_type, task_name="TEST_NER")
#tagger = SequenceTagger(tag_dictionary=corpus.make_tag_dictionary(tag_type), tag_type=tag_type, hidden_size=256, embeddings=embeddings)

tagger.add_and_switch_to_new_task("TEST_NER_CONLL3+MIT10", tag_dictionary=label_dictionary, tag_type=tag_type)

trainer = ModelTrainer(tagger, corpus)
trainer.train(
    base_path='resources/testfaelle-studproj/conll_3+mit10sent',
    learning_rate=0.1,
    mini_batch_size=32,
    mini_batch_chunk_size=None,
    max_epochs=10,
)
