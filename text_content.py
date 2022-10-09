opening_text = """
# Philosophical Contestation in Early New Zealand Newspapers
Joshua Wilson Black \n
_University of Canterbury_ \n
<joshua.black@canterbury.ac.nz> \n
<joshua@wilsonblack.nz>


This dashboard provides access to corpora generated from the New Zealand National Library Te Puna Mātauranga o Aotearoa's Paper's Past Newspaper dataset up to 1900.

The general method of corpus construction is presented at <https://github.com/JoshuaWilsonBlack/newspaper-philosophy-methods>. A paper is in preparation describing the method in more detail.

Code for this dashboard is available at <https://github.com/JoshuaWilsonBlack/NPOD_Philosophy>.

**Note:** this page contains terms, and charts relationships between terms, from the text of nineteenth century newspapers using various statistical learning methods. As such, it is likely to contain some offensive material.
"""

cytoscape_explainer = """The following controls are available for constructing co-occurrence networks:

* **Corpus:** Select a corpus to generate cooccurence networks from. The "Final Corpus" is the most recent corpus, candidate corpus 0 is keyword search results for 'philoso*'.
* **Document representation**: represent articles as either bags of words (a count for each word in the dictionary), or with the TF-IDF transformation (where words are scaled on the basis of their prevalence in the corpus). TF-IDF reduces the salience of words which are common across the corpus.
* **Search term**: select a search term for which co-occurrences have been precalculated. For Candidate Corpus 3, this is the entire dictionary.
* **Statistic**: select a way to calculate the significance of co-occurrences. Options are mutual information, which quantifies how much information about the appearance of the other co-occurrence is given by the appearance of the search term. Log Dice is similar, but does not vary with corpus size.
* **Primary co-occurrences**: the number of co-occurring terms for the search term which will appear in the network.
* **Secondary co-occurrences**: the number of co-occurring terms of each of the primary co-occurrences to be added to the network (they may already be on it).

**Note:** Line thickness represents relative strength of relationship of _within_ a network and should not be used for comparisons across networks.
"""
