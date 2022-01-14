# classify-tutorials-surveys

This module builds a Random Forest Classifier which identifies suitable research tutorials and surveys. We acquire training data by querying Microsoft Academic Graph (MAG) for research papers and associated metadata. We perform regression analysis to understand data behavior and build the classifier based on these results (choosing features, selecting the model, considering hyper-parameters). Finally, we apply the model by querying for other research and outputting those classified as suitable.

## Setup
Install module dependencies.
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

### Data Acquisition
* Queries for training_data related to keywords in file 
* Returns training_data dict with data for each paper
```python
fetch_papers(num_papers_per_keyword, num_keywords, filename):
  ...
  return training_data
```

* Saves training data into csv for classifier to read and train from
```python
write_papers_csv(papers, filename):
  ...
```

* Returns labels for all article metadata, including label and keyword
```python
get_fieldnames():
  ...
  return fieldname_list
```

### EDA, Model Training & Testing

* Performs Principal Component Analysis on training data
```python
PCA_(filename):
  ...
```

* Returns selected features to be used in model
```python
get_features():
  ...
  return feature_list
```

* Trains, tests, and saves model to joblib file
```python
build_model(filename):
  ...
```

* Returns numpy arrays of features and labels from data in file path
```python
get_training_data(filename):
  ...
  return features, labels
```

* Creates train, test split
* Builds and fits Random Forest Classifier to data
* Saves model to joblib file
* Returns model accuracy on testing split in terms of quantity correctly identified as suitable (outputted 1)
```python
train_test_scholars(feature, label):
  ...
  return model_accuracy
```

### Model Application
* Returns fieldnames representing data to be saved with suitable articles
```python
get_article_info():
  ...
  return info_list
```

* Queries for papers, returns those identified as suitable in pandas DataFrame
```python
get_suitable_papers():
  ...
  return suitable_papers
```

## Demo Video
[![Watch](https://github.com/Forward-UIUC-2021F/matthew-kurapatti-classify-tutorials-surveys/blob/media/prev.png)](https://drive.google.com/file/d/1KVZCfRPXnpiCAEpdFNhrulkvGtQyl6-4/view?usp=sharing)

## Algorithmic Design
This module builds off the previous implementation of our classifier in google scholar. We expand to another data sources, adjusting our classifier to handle different inputs and datasets. We use modular code to avoid feature mismatches between and within datasets, and attempt to improve accuracy of the classifier by adjusting parameters, training, and testing methods.

The module takes an input of keywords and finds articles related to that keyword to train the classifier on. In the case of MAG, this is as simple as updating the API request with the keyword. It saves these results to a file the classifier can read from and train. We also test our classifier with folds from the training data (a technique called cross-validation).

Finally, the purpose of this module is to leverage the classifier to identify suitable articles for given keywords. We query for articles in the same way we found training data and determine an article's suitability by its classification output. This gives us a final list of suitable tutorial/survey articles related to a keyword.

![design architecture](https://github.com/Forward-UIUC-2021F/matthew-kurapatti-classify-tutorials-surveys/blob/media/DesignDocDiagram.png)
