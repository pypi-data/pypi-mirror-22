from itertools import chain
from beautifultable import BeautifulTable

from .utils import get_subsets
from .rule import AssociationRule
import math


class ARM(object):
    """Utility class for Association Rule Mining.

    This class provides methods to generate a set of Association rules
    from a transactional dataset.
    """
    def __init__(self):
        self._dataset = []
        self._rules = []
        self._itemcounts = {}
        self.set_rule_key(lambda rule: (rule.lift, rule.confidence,
                                        len(rule.antecedent)))
        self._apparent_support_threshold = None
        self._apparent_confidence_threshold = None
        self._apparent_coverage_threshold = None
        self._real_support_threshold = math.inf
        self._real_confidence_threshold = math.inf
        self._real_coverage_threshold = math.inf

    @property
    def rules(self):
        """Get a list of rules generated using the loaded dataset."""
        import itertools
        return list(itertools.filterfalse(
            lambda rule: (self._apparent_support_threshold > rule.coverage
                          or self._apparent_confidence_threshold > rule.confidence),
            self._rules))

    @property
    def support_threshold(self):
        return self._apparent_support_threshold

    @property
    def confidence_threshold(self):
        return self._apparent_confidence_threshold

    @property
    def coverage_threshold(self):
        return self._apparent_coverage_threhold

    def load(self, data):
        """Load a set of transactions from a Iterable of lists.

        Parameters
        ----------
        data : Iterable of lists
            List of transactions
        """
        self._clear()
        for row in data:
            self._dataset.append(list(row))

    def load_from_csv(self, filename):
        """Load a set of transactions from a csv file.

        Parameters
        ----------
        filename : string
            Name of the csv file which contains a set of transactions
        """
        self._clear()
        import csv
        with open(filename) as csvfile:
            mycsv = csv.reader(csvfile)
            for row in mycsv:
                self._dataset.append(row)

    def set_rule_key(self, key):
        """Set the key function which should be used to sort rules.

        The default key function sorts rules using lift, confidence and
        size of antecedent respectively. This behaviour can be changed
        using this method.

        Parameters
        ----------
        key : function
            The key function to sort rules
        """
        self._rule_key = key

    def _clear(self):
        self._dataset = []
        self._rules = []
        self._itemcounts = {}

    def _clean_items(self, items):
        return tuple(items)

    def _get_itemcount(self, items):
        try:
            return self._itemcounts[tuple(set(items))]
        except KeyError:
            pass
        count = 0
        for data in self._dataset:
            found = True
            for item in items:
                if item not in data:
                    found = False
                    break
            if found:
                count += 1
        return count

    def _get_initial_itemset(self):
        itemset = []
        items = set(chain(*self._dataset))
        for item in items:
            itemset.append([item])
        return sorted(itemset)

    def _should_join_candidate(self, candidate1, candidate2):
        for i in range(len(candidate1) - 1):
            if candidate1[i] != candidate2[i]:
                return False
        if candidate1[-1] != candidate2[-1]:
            return True
        return False

    def _get_nextgen_itemset(self, itemset):
        new_items = []
        for i, _ in enumerate(itemset):
            for j in range(i, len(itemset)):
                if self._should_join_candidate(itemset[i], itemset[j]):
                    new_items.append(sorted(set(itemset[i]).union(itemset[j])))
        return new_items

    def _prune_itemset(self, itemset):
        to_be_pruned = []
        for items in itemset:
            item_count = self._get_itemcount(items)
            item_support = round(item_count / len(self._dataset), 3)
            if item_support < self._real_support_threshold:
                to_be_pruned.append(items)

        for items in to_be_pruned:
            itemset.remove(items)

    def _prune_rules(self):
        pruned_rules = []
        data_cover_count = [0] * len(self._dataset)
        for rule in self._rules:
            rule_add = False
            for i, data in enumerate(self._dataset):
                items = self._clean_items(data)
                if (rule.match_antecedent(items)
                        and data_cover_count[i] >= 0):
                    rule_add = True
                    data_cover_count[i] += 1
                    if data_cover_count[i] >= self._real_coverage_threshold:
                        data_cover_count[i] = -1

            if rule_add:
                pruned_rules.append(rule)

        self._rules = pruned_rules

    def _print_items(self):
        for item, count in self._itemcounts.items():
            print(item, count)

    def _generate_rules(self, itemset):
        for items in itemset:
            subsets = get_subsets(items)
            for element in subsets:
                remain = set(items).difference(set(element))
                if len(remain) > 0:
                    count_lhs = self._get_itemcount(element)
                    count_rhs = self._get_itemcount(remain)
                    count_both = self._get_itemcount(items)
                    rule = AssociationRule(tuple(element), tuple(remain),
                                           count_both, count_lhs, count_rhs,
                                           len(self._dataset))
                    if (rule.confidence >= self._real_confidence_threshold):
                        self._rules.append(rule)

    def print_rules(self, attributes=('coverage', 'confidence', 'lift')):
        """Print the generated rules in a tabular format.

        Parameters
        ----------
        attributes : array_like
            pass
        """
        table = BeautifulTable()
        table.column_headers = (['Antecedent', 'Consequent']
                                + list(attr.replace('_', ' ').title()
                                       for attr in attributes))

        table.column_alignments[0] = table.ALIGN_LEFT
        table.column_alignments[1] = table.ALIGN_LEFT
        for rule in self.rules:
            table.append_row([rule.antecedent2str(),
                              rule.consequent2str()]
                             + list(getattr(rule, attr)
                                    for attr in attributes))

        print(table)

    def _learn(self, support_threshold, confidence_threshold,
               coverage_threshold):
        self._apparent_support_threshold = support_threshold
        self._apparent_confidence_threshold = confidence_threshold
        self._apparent_coverage_threshold = coverage_threshold
        
        self._real_support_threshold = support_threshold
        self._real_confidence_threshold = confidence_threshold
        self._real_coverage_threshold = coverage_threshold
        
        itemset = self._get_initial_itemset()
        self._rules = []
        while len(itemset) > 0:
            self._prune_itemset(itemset)
            self._generate_rules(itemset)
            itemset = self._get_nextgen_itemset(itemset)

        self._rules = list(set(self._rules))
        self._prune_rules()
        self._rules.sort(key=self._rule_key, reverse=True)

    def learn(self, support_threshold, confidence_threshold,
              coverage_threshold=20):
        """Generate Association rules from the Training dataset.

        Parameters
        ----------
        support_threshold : float
            User defined threshold between 0 and 1. Rules with support
            less than `support_threshold` are not generated.

        confidence_threshold : float
            User defined threshold between 0 and 1. Rules with confidence
            less than `confidence_threshold` are not generated.

        coverage_threshold : int
            Maximum number of rules, a specific transaction can match.
            After it exceeds this, That row is no longer considered for
            matching other rules. Using this process all rules are removed,
            which do not match any transaction left(Default 20).
        """
        if (support_threshold < self._real_support_threshold
                or confidence_threshold < self._real_confidence_threshold
                or coverage_threshold != self._real_coverage_threshold):
            self._learn(support_threshold, confidence_threshold,
                        coverage_threshold)

        self._apparent_support_threshold = support_threshold
        self._apparent_confidence_threshold = confidence_threshold
        self._apparent_coverage_threshold = coverage_threshold
