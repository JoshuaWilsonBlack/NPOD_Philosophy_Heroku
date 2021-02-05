opening_text = """
# Investigating Philosophical Discourse in Early New Zealand Newspapers
## DATA601 Summer Project (UC Arts Digital Lab)
Joshua Black
black.joshuad@gmail.com

This dashboard allows for the inspection of a random subset of the main corpora developed in course of the project and for the generation and inspection of co-occurrence networks of key terms in the corpora.

The full general philosophy corpus and religion-science corpus are availble for download as zip files containing the articles in markdown format: (add links)

The corpora, and labelled dataset used for training classifiers, are also available as pickled pandas dataframes along with almost all other project files and got at the project's [GitHub page](https://github.com/JoshuaDavidBlack/NPOD_Philosophy).

Code for this dashboard is available at <https://github.com/JoshuaDavidBlack/NPOD_Philosophy>.

**Note:** this page contains terms, and charts relationships between terms, from the text of nineteenth century newspapers using various statistical learning methods. As such, it is likely to contain offensive material.
"""

cytoscape_explainer = """
The following controls are available for constructing co-occurrence networks:

* **Corpus**: select which of the corpora produced as part of the project you want to investigate. 'Naive Bayes 2' is the final general philosophy corpus, and 'Religion Science' is a corpus produced by extracting articles about the relationship between religion and science from the Naive Bayes 2 corpus.
* **Document representation**: represent articles as either bags of words (a count for each word in the dictionary), or with the TF-IDF transformation (where words are scaled on the basis of their prevalence in the corpus). TF-IDF reduces the salience of common words.
* **Search term**: select a search term for which co-occurrences have been precalculated.
* **Statistic**: select a way to calculate the significance of co-occurrences. Options are mutual information, which quantifies how much information about the appearance of the other co-occurrence is given by the appearance of the search term. Log Dice is similar, but takes less account of the number of distinct documents a word appears in. It was designed with lexicographers in mind.
* **Primary co-occurrences**: the number of co-occurring terms for the search term which will appear in the network.
* **Secondary co-occurrences**: the number of co-occurring terms of each of the primary co-occurrences to be added to the network (they may already be on it).
"""
