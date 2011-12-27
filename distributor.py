"""
This module supplies the Distributor object.
It helps you to distribute your bets for a given racecourse quotes and stay
close (upper) to the profit you targeted.
Below is an example of how to use it.

>>> targeted_profit = 10
>>> quotes = (5, 8, 7, 12, 10, 7)

>>> dist = Distributor(targeted_profit, quotes)
>>> dist.get_bets()
[11, 7, 8, 5, 6, 8]
>>> dist.get_total_bet()
45
>>> dist.get_effective_profits()
[10, 11, 11, 15, 15, 11]

>>> targeted_profit = 100
>>> quotes = (3, 4, 5, 20, 34)
>>> dist = Distributor(targeted_profit, quotes)
>>> dist.get_bets()
[245, 184, 147, 37, 22]
>>> dist.get_total_bet()
635
>>> dist.get_effective_profits()
[100, 101, 100, 105, 113]
"""

import math


class Distributor:

    def __init__(self, targeted_profit, quotes=[]):
        self._uptodate = False
        self._targeted_profit = float(targeted_profit)
        self._quotes = quotes
        self._bets = [0] * len(quotes)

    def _compute_total_bet(self, bets):
        return sum(bets)

    def _check_all_effective_profit_ok(self, quotes, bets, targeted_profit):
        """
        Returns true if all effective profits are > than targeted_profit.
        """
        i = 0
        profit_ok = True
        while (i < len(quotes) and profit_ok):
            profit_ok = \
                (quotes[i] * bets[i]) - self._compute_total_bet(bets) \
                >= targeted_profit
            i += 1
        return profit_ok

    def _compute_all_bets(self):
        """
        Main method that does all the bets calculation.
        """
        if self._uptodate or not self._quotes:
            return
        all_effective_profit_ok = False
        # recall all rounds if some effective profits are not ok
        while not all_effective_profit_ok:
            for round_n in range(len(self._quotes)):
                # in case of a another while (not all_effective_profit_ok) loop
                self._bets[round_n] = 0
                total_bet = self._compute_total_bet(self._bets)
                bet = (self._targeted_profit + total_bet) \
                    / (self._quotes[round_n] - 1)
                bet = math.ceil(bet)
                bet = int(bet)
                self._bets[round_n] = bet
                # verifies that previous bets are still ok even after
                # the the total_bet value increased (by the last bet value)
                all_effective_profit_ok = \
                    self._check_all_effective_profit_ok(
                        self._quotes, self._bets, self._targeted_profit)
        self._uptodate = True

    def add_quote(self, quote):
        self._uptodate = False
        self.quotes.append(quote)

    def clear_quotes(self):
        self._uptodate = False
        self._quotes = []

    def get_bets(self):
        if not self._uptodate:
            self._compute_all_bets()
        return self._bets

    def get_total_bet(self):
        return sum(self.get_bets())

    def get_quotes(self):
        return self._quotes

    def get_effective_profits(self):
        tmp_bets = self.get_bets()
        total_bet = self._compute_total_bet(tmp_bets)
        effective_profits = []
        for i in range(len(self._quotes)):
            bet = tmp_bets[i]
            quote = self._quotes[i]
            effective_profit = ((bet * quote) - total_bet)
            effective_profits.append(effective_profit)
        return effective_profits

if __name__ == "__main__":
    import doctest
    doctest.testmod()
