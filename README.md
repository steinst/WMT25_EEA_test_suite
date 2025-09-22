# Test suite for EEA translations

This test suite was submitted to the WMT 25 test suite shared task. The compilation and evaluation of the test suite is decribed in the paper: Automatic Evaluation for Terminology Translation related to the EEA Agreement

### License 
Copyright 2025 Selma Dís Hauksdóttir, Steinþór Steingrímsson

The test suite for EEA translations is released under [CC BY 4.0](LICENSE).


### Building the environment

If you haven't already check out the repository:
```bash
git clone https://github.com/steinst/WMT25_EEA_test_suite.git
cd WMT25_EEA_test_suite
```

Dependencies can be installed from the `requirements.txt` file using pip:
```bash
pip install -r requirements.txt
```

### Running the evaluation described in the paper
```bash
python3 autoeval.py
```

## Files in the repository
The repository contains the following files and folders:
- `autoeval.py`: The main script to run the evaluation.
- `requirements.txt`: A list of Python packages required to run the evaluation.
- `test_suite/`: A folder containing the EEA test suite files.
- `test_suite/complete`: A folder containing the file submitted to the WMT25 test suite shared task. Not all lines were usable in this file, so we also have a fixed version.
- `test_suite/complete_fixed`: A folder containing a fixed version of the submitted file, containing 299 lines.
- `test_suite/evaluated`: A folder containing the 256 sentences that were correct in submitted file and evaluated automatically for the paper.
- `test_suite/submissions`: A folder containing all systems submissions for our test suite.
- `test_suite/EEA_terms.tsv`: A file containing the English terms evaluated in the test suite with the corresponding Icelandic translation.
- `test_suite/EEA_inflections.tsv`: A file containing all relevant inflectional forms of the Icelandic terms, used for looking up in the translations. This list was compiled using the Database of Icelandic Morphology (DIM).
- `evaluation/`: A folder containing the evaluation results.
- `evaluation/automatic`: The results of the automatic evaluation.
- `evaluation/manual`: The annotated results of the manual evaluation.

## Publications

```bibtex	
@inproceedings{selma-steinthor-2025-eea,
    title = {{Automated Evaluation for Terminology Translation related to the EEA Agreement}},
    author = "Hauksd{\'o}ttir, Selma D{\'i}s and
      Steingr{\'i}msson, Stein{\th}{\'o}r",
    editor = "Koehn, Philipp  and  Haddow, Barry  and  Kocmi, Tom  and  Monz, Christof",
    booktitle = "Proceedings of the Tenth Conference on Machine Translation",
    month = nov,
    year = "2025", 
    address = "China", 
    publisher = "Association for Computational Linguistics", 
}
```
