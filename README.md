# classify-tutorials-surveys

This module builds a Random Forest classifier which identifies suitable research tutorials and surveys. We begin by querying Microsoft Academic Graph (MAG) for research papers and associated metadata. Then, we analyze the data and train the classifier on selected features. We can once again query for articles, determining whether an arbitrary article is suitable based on our model's classification.

## Setup
Install module dependencies with:
```
  pip install -r requirements.txt
```

## Structure
```
matthew-kurapatti-classify-tutorials-surveys
  - src/
    - classification.py
    - fetch_suitable_papers.py
    - fetch_training_papers.py
  - data/
    - training_keywords.txt
    - training_data.csv
    - suitable_keywords.txt
    - suitable_papers.csv  
```

* `src/fetch_training_papers.py`: Acquires training data from MAG. Requires keyword inputs to query
* `src/classification.py`: Contains functions to train, test, and save model. Also contains function for PCA
* `src/fetch_suitable_papers.py`: Queries MAG and identifies suitable papers with loaded model

* `data/training_keywords.txt`: Keywords to use when querying MAG to find training data
* `data/training_data.csv`: Articles and metadata for training found with 'fetch_training_papers.py'
* `data/suitable_keywords.txt`: Keywords to use when querying MAG to find potentially suitable articles
* `data/suitable_papers.csv`: Articles identified as suitable after running 'fetch_suitable_papers.py'


## Functional Design
* Queries for articles related to keyword, returns papers dict with metadata for each article
* Saves training data into csv for classifier to read and train from
```python
fetch_papers(keyword_list, filename):
  ...
  return
```

* Trains classifiers based on inputted file, using inputted features
```python
train(filename, feature_list):
  ...
  return
```

* Tests classifier based on split from training data (folding, cross validation) and returns accuracy
```python
test(classifier, papers):
  ...
  return accuracy
```

* Queries with keyword and outputs articles identified as suitable
```python
find_articles(classifier, keyword)
  ...
  return papers
```

## Demo Video
[![Watch](https://github.com/Forward-UIUC-2021F/matthew-kurapatti-classify-tutorials-surveys/blob/media/prev.png)](https://drive.google.com/file/d/1KVZCfRPXnpiCAEpdFNhrulkvGtQyl6-4/view?usp=sharing)

## Algorithmic Design
This module builds off the previous implementation of our classifier in google scholar. We expand to another data sources, adjusting our classifier to handle different inputs and datasets. We use modular code to avoid feature mismatches between and within datasets, and attempt to improve accuracy of the classifier by adjusting parameters, training, and testing methods.

The module takes an input of keywords and finds articles related to that keyword to train the classifier on. In the case of MAG, this is as simple as updating the API request with the keyword. It saves these results to a file the classifier can read from and train. We also test our classifier with folds from the training data (a technique called cross-validation).

Finally, the purpose of this module is to leverage the classifier to identify suitable articles for given keywords. We query for articles in the same way we found training data and determine an article's suitability by its classification output. This gives us a final list of suitable tutorial/survey articles related to a keyword.

![design architecture](https://github.com/Forward-UIUC-2021F/matthew-kurapatti-classify-tutorials-surveys/blob/media/DesignDocDiagram.png)
