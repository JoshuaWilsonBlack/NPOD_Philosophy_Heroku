opening_text = """
# Philosophical Contestation in Early New Zealand Newspapers
Joshua Black \n
_University of Canterbury_ \n
<joshua.black@canterbury.ac.nz> \n
<black.joshuad@gmail.com>


This dashboard allows for the inspection of a random subset of the main corpora developed in course of the project and for the generation and inspection of co-occurrence networks of key terms in the final corpora.

The general method of corpus construction is presented at <https://github.com/JoshuaDavidBlack/newspaper-philosophy-methods>. A paper is in preparation describing the method in more detail.

Code for this dashboard is available at <https://github.com/JoshuaDavidBlack/NPOD_Philosophy>.

**Note:** this page contains terms, and charts relationships between terms, from the text of nineteenth century newspapers using various statistical learning methods. As such, it is likely to contain offensive material.
"""

cytoscape_explainer = """
The following controls are available for constructing co-occurrence networks:

* **Document representation**: represent articles as either bags of words (a count for each word in the dictionary), or with the TF-IDF transformation (where words are scaled on the basis of their prevalence in the corpus). TF-IDF reduces the salience of common words.
* **Search term**: select a search term for which co-occurrences have been precalculated.
* **Statistic**: select a way to calculate the significance of co-occurrences. Options are mutual information, which quantifies how much information about the appearance of the other co-occurrence is given by the appearance of the search term. Log Dice is similar, but does not vary with corpus size.
* **Primary co-occurrences**: the number of co-occurring terms for the search term which will appear in the network.
* **Secondary co-occurrences**: the number of co-occurring terms of each of the primary co-occurrences to be added to the network (they may already be on it).

Line thickness represents relative strength of relationship of _within_ a network but should not be used for comparisons across networks.
"""
