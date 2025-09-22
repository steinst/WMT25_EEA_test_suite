Test suite and evaluation code for EEA translations.

This test suite was submitted to the WMT 25 test suite shared task. The compilation and evaluation of the test suite is decribed in the paper: Automatic Evaluation for Terminology Translation related to the EEA Agreement




# SentAlign

SentAlign is a sentence alignment tool for parallel corpora. It uses [LaBSE](https://aclanthology.org/2022.acl-long.62.pdf) embeddings to find sentence pairs that are similar in meaning 
and an alignment algorithm based on Dijkstra's algorithm to find the optimal alignment. Dynamic programming with cosine similarity tends to favour many-to-many alignments over 1-1 alignments. To counteract this we end with re-evaluating each alignment by inspecting mergers, insertions and deletions. The approach is described in more detail in the paper [SentAlign: Accurate and Scalable Sentence Alignment](). 

### License 
Copyright 2023 Steinþór Steingrímsson

SentAlign is released under the [Apache License, Version 2.0](LICENSE).


### Building the environment

If you haven't already check out the repository:
```bash
git clone https://github.com/steinst/SentAlign.git
cd SentAlign
```

The environment can be built using the provided environment.yml file:
```bash
conda env create -f environment.yml
```

### Running the aligner
We assume that the documents to be aligned have the same names in the source and target language, but are kept in folders named using the language code. For example, if we want to align the files in the folder `/path/to/files` we would have the following structure:
```bash
/path/to/files/eng/file1.txt
/path/to/files/eng/file2.txt
...
/path/to/files/isl/file1.txt
/path/to/files/isl/file2.txt
```

Assuming a Conda environment has been built as described above, the environment has to be activated before SentAlign is run:
```bash
conda activate SentAlign
```

Start by creating a list of files to align:

```bash
python3 files2align.py -dir /path/to/files --source-language eng
```

Then you run the alignments. Aligning English and Icelandic files:

```bash
python3 sentAlign.py -dir /path/to/files -sl eng -tl isl
```

The aligner generates two type of files in the output folder: `/path/to/files/output`. Files ending with `.path` files containing the alignments and LaBSE scores. They are formatted like this:

```
[0]:[0,1]:0.7565563
[1]:[2]:0.99999994
[2]:[3]:0.92132425
[3]:[4]:0.87890404
[4]:[5,6]:0.9721296
[]:[7]:0
[5]:[8]:0.89229476
[6]:[9]:0.70389956
...
```

and `.aligned` files containing the aligned sentence pairs as well as the LaBSE score. Source sentence in the first column, target sentence in the second and LaBSE score in the third:



## Evaluating Test Sets
The SentAlign paper evaluates the aligner on two evaluation sets: the German-French evaluation set comprising data from the text+berg corpus and published with BleuAlign, and an Icelandic-English test set using data from the Parice corpus. 

To reproduce the results, run the following commands for the German-French test set:

```bash
python3 files2align.py -dir eval_data/bleualign --source-language deu
python3 sentAlign.py -dir eval_data/bleualign -sl deu -tl fra
python3 evaluation/evaluate.py -t eval_data/bleualign/output/test*.txt.path -g eval_data/bleualign/gold/test*.txt
```
Which should give you the following results:
```
 ---------------------------------
|             |  Strict |    Lax  |
| Precision   |   0.935 |   0.998 |
| Recall      |   0.929 |   0.933 |
| F1          |   0.932 |   0.964 |
 ---------------------------------
```

## Parameters

### Input and output settings
```bash
'--corpus-folder', '-dir'
'--source-language', '-sl', default='eng'
'--target-language', '-tl', default='isl'
'--filename', '-f', help='Name of source and target file(s) to be aligned', type=str, nargs='+'
'--output-folder', '-out', default='output'
```
### Aligner settings
```bash
'-n', '--num_overlaps', type=int, default=4, help='Maximum number of allowed overlaps.'
'--max-concatenations', '-concats', type=int, help='Maximum number of concatenated sentences per language', default=4
'--free-concatenations', '-freejoins', type=int, help='Maximum number of concatenations before penalty is applied', default=2
'--score-cutoff', '-cutoff', type=float, help='Minimum similarity score for a sentence pair to be considered', default=0.4
'--minimum-length-words', '-minwords', type=int, help='Minimum number of words per language, for a sentence pair to be considered', default=1
'--maximum-length-words', '-maxwords', type=int, help='Maximum number of words per language, for a sentence pair to be considered', default=110
'--penalty-after-words', '-penwords', type=int, help='Maximum number of words per language, before a length penalty is applied', default=80
'--penalty-per-word', '-wordpen', type=float, help='Penalty applied for each word when maximum number of unpenalized words have been reached', default=0.01
'--anchoring-delimiter', '-anchor', type=int, help='Maximum nodes in the alignment graph, before applying hard delimiters.', default=4000000
'--maximum-length-gale-church', '-maxgc', type=float, help='Maximum number of sentences in file for Gale-Church alignment. If longer, only greedy alignment selection applied', default=10000
```
### Other settings
```bash
'--proc-device', '-device', help='cuda for gpu, cpu if you don''t have an NVIDIA graphics card', default='cuda'
'--num-proc', '-proc', help='number of processors to allocate for the pathfinding calculations', default=8
```

## Publications

```bibtex	
@inproceedings{sentalign-2023,
    title = {{SentAlign: Accurate and Scalable Sentence Alignment}},
    author = "Steingrímsson, Steinþór and
      Loftsson, Hrafn  and
      Way, Andy",
    booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = dec,
    year = "2023",
    address = "Singapore, Singapore",
    publisher = "Association for Computational Linguistics",
}
```
