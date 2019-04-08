Switchboard Dialog Act Corpus with Penn Treebank links
=========================

## Overview

[The Switchboard Dialog Act Corpus](http://www.stanford.edu/~jurafsky/ws97/) (SwDA) extends
the [Switchboard-1 Telephone Speech Corpus, Release 2](http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC97S62)
with turn/utterance-level dialog-act tags. The tags summarize syntactic,
semantic, and pragmatic information about the associated turn.  The
SwDA project was undertaken at UC Boulder in the late 1990s.

The SwDA is not inherently linked to the Penn Treebank 3 parses of
Switchboard, and it is far from straightforward to align the two
resources. In addition, the SwDA is not distributed with the
Switchboard's tables of metadata about the conversations and their
participants.

This project includes a version of the corpus (`swda.zip`) that
pools all of this information to the best of my ability. In addition,
it includes Python classes that should make it easy to work with
this merged resource.

This project was originally part of my LSA Linguistic Institute 2011
course [Computational Pragmatics](http://compprag.christopherpotts.net/index.html).
Additional resources from that corpus:

* [Corpus overview](http://compprag.christopherpotts.net/swda.html)
* [Experiment: Question acts and interrogative clauses in the SwDA](http://compprag.christopherpotts.net/swda-clausetyping.html)
* [Analysis: Clustering words by tags in the SwDA](http://compprag.christopherpotts.net/swda-clustering.html)

The code in this repository is compatible with Python 2 and Python 3.
Its only other external dependency is [NLTK](http://www.nltk.org/install.html),
with [the data installed](http://www.nltk.org/data.html)
so that WordNet is available.

## Citation

If you use this resource, please cite

```
@techreport{Jurafsky-etal:1997,
	Address = {Boulder, CO},
	Author = {Jurafsky, Daniel and Shriberg, Elizabeth and Biasca, Debra},
	Institution = {University of Colorado, Boulder Institute of Cognitive Science},
	Number = {97-02},
	Title = {Switchboard {SWBD}-{DAMSL} Shallow-Discourse-Function Annotation Coders Manual, Draft 13},
	Year = {1997}}

@article{Shriberg-etal:1998,
	Author = {Shriberg, Elizabeth and Bates, Rebecca and Taylor, Paul and Stolcke, Andreas and Jurafsky, Daniel and Ries, Klaus and Coccaro, Noah and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
	Journal = {Language and Speech},
	Number = {3--4},
	Pages = {439--487},
	Title = {Can Prosody Aid the Automatic Classification of Dialog Acts in Conversational Speech?},
	Volume = {41},
	Year = {1998}}

@article{Stolcke-etal:2000,
	Author = {Stolcke, Andreas and Ries, Klaus and Coccaro, Noah and Shriberg, Elizabeth and Bates, Rebecca and Jurafsky, Daniel and Taylor, Paul and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
	Journal = {Computational Linguistics},
	Number = {3},
	Pages = {339--371},
	Title = {Dialogue Act Modeling for Automatic Tagging and Recognition of Conversational Speech},
	Volume = {26},
	Year = {2000}}
```

## Files

* `swda.py`: the module for processing this corpus distribution
* `swda.zip`: the corpus; needs to be unzipped
* `swda_functions.py`: some simple examples aggregating informaton with `CorpusReader`s
* `metadata_processor.py`: auxiliary processing file used to create `swda/swda-metadata.csv`


## `Transcript` objects

The code's `Transcript` objects model the individual files in the corpus.
A `Transcript` object is built from a transcript filename and the corpus
metadata file:

```python
from swda import Transcript

trans = Transcript('swda/sw00utt/sw_0001_4325.utt.csv', 'swda/swda-metadata.csv')

trans.topic_description
'CHILD CARE'

trans.prompt
'FIND OUT WHAT CRITERIA THE OTHER CALLER WOULD USE IN SELECTING CHILD \
CARE SERVICES FOR A PRESCHOOLER.  IS IT EASY OR DIFFICULT TO FIND SUCH CARE?'

trans.talk_day
datetime.datetime(1992, 3, 23, 0, 0)

trans.talk_day.year
1992

trans.talk_day.month
3

trans.from_caller
1632

trans.from_caller_sex
'FEMALE'
```

`Transcript` instances have many attributes:

```python
for a in sorted([a for a in dir(trans) if not a.startswith('_')]):
	print(a)

conversation_no
conversation_no
from_caller
from_caller_birth_year
from_caller_dialect_area
from_caller_education
from_caller_sex
header
length
metadata
prompt
ptd_basename
swda_filename
talk_day
to_caller
to_caller_birth_year
to_caller_dialect_area
to_caller_education
to_caller_sex
topic_description
utterances
```


## `Utterance` objects

These have many attributes and methods. Some examples:

```python
utt = trans.utterances[19]

utt.caller
'B'

utt.act_tag
'sv'

utt.text
'[ I guess + --'

utt.pos
'[ I/PRP ] guess/VBP --/:'

utt.pos_words()
['I', 'guess', '--']

utt.pos_lemmas(wn_lemmatize=True)
[('I', 'prp'), ('guess', 'v'), ('--', ':')]

len(utt.trees)
1

utt.trees[0].pprint()
'(S
  (EDITED
    (RM (-DFL- \\[))
    (S (NP-SBJ (PRP I)) (VP-UNF (VBP guess)))
    (IP (-DFL- \\+)))
  (NP-SBJ (PRP I))
  (VP
    (VBP guess)
    (RS (-DFL- \\]))
    (SBAR
      (-NONE- 0)
      (S (NP-SBJ (PRP we)) (VP (MD can) (VP (VB start))))))
  (. .))'
```

Because the trees often properly contain the utterance, they cannot be used to
gather word- or phrase-level statistics unless care is taken to restrict attention
to the subtrees, or fragments thereof, that represent the utterance itself.

Not all utterances have trees; only a subset of the Switchboard is fully parsed.
Thus, of the 221,616 utterances in the SwDA, 118,218 (53%) have at least one
tree.



## `CorpusReader` objects

The main interface provided by `swda.py` is the `CorpusReader`, which allows you to
iterate through the entire corpus, gathering information as you go. `CorpusReader`
objects are built from just the root of the directory containing your csv files.
(It assumes that `swda-metadata.csv` is in the first directory below that root.)

```python
from swda import CorpusReader
corpus = CorpusReader('swda')
```

The two central methods for `CorpusReader` objects are `iter_transcripts`
and `iter_utterances`. The method `iter_utterances` is basically an abbreviation
of the following nested loop:

```python
for trans in corpus.iter_transcripts():
    for utt in trans.utterances:
        yield utt
```

For some illustrations, see `swda_functions.py`.


## For more

There's a much fuller overview here:
[http://compprag.christopherpotts.net/swda.html](http://compprag.christopherpotts.net/swda.html)
