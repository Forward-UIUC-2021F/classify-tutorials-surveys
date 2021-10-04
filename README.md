# classify-tutorials-surveys

This project builds a Random Forest classifier which determines whether research papers are suitable by attempting to determine whether they are tutorial or survey articles. The module finds training data by mining google scholar, mag, and other sources for papers and associated metadata. Then, it trains the classifier on selected features. Using the trained classifier, we can once again query research sources for suitable articles, determining whether an arbitrary article is suitable based on its output when put in to our classifier.

## Functional Design
* Queries for articles related to keyword, returns papers dict with metadata for each article
* Saves paper into accessable format (likely .csv) for classifier to access and train from
```python
fetch_papers(keyword_list):
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

* With the inputted keyword, the module queries for articles related to keyword and determines suitably for each article based on classifier output
```python
find_articles(classifier, keyword)
  ...
  return papers
```


## Algorithmic Design
This module builds off the previous implementation of our classifier in google scholar. We expand to other data sources, adjusting our classifier to handle different inputs and datasets. We appropiately handle feature mismatches between and within datasets, and attempt to improve accuracy of the classifier by adjusting parameters, training, and testing methods.

The module takes an input of keywords, and finds articles related to that keyword to train the classifier on. This can be achieved by querying google scholar with the keyword and appending some information to improve our search (i.e. tutorial, survey), or using existing APIs which do the searching for us. Then, it saves these results to a format where the classifier can access and train from. All parameters and inputs are modular to allow different datasets to be used. We also test our classifier with folds from the training data (a technique called cross-validation).

Finally, the purpose of this module is to use the classifier to find suitable articles for given keywords. We query for articles similar to the way we found training data, and determine the suitability by inputting our data into the classifier. This returns a final list of papers we represent suitable tutorial/survey articles related to a keyword or list of keywords.
