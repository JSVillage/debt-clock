import os
import sys
import random
import argparse
import operator

class TaxDebt():

  def __init__(self):
    self.households = 117538000
    self.debt = 15000000000000
    self.family = 4

    print 'ASSUMED DEBT', '%.2f' % ((self.debt / self.households) / self.family)

  def get_percentile(self, income):

    # http://www.census.gov/compendia/statab/2012/tables/12s0694.pdf
    table = {
      1970: ((18180,  34827,  50656,  72273,  114243), (4.1,  10.8,  17.4,  24.5,  43.3,  16.6)),
      1980: ((18533,  34757,  53285,  78019,  125556), (4.2,  10.2,  16.8,  24.7,  44.1,  16.5)),
      1990: ((19886,  37644,  57591,  87826,  150735), (3.8,  9.6,  15.9,  24.0,  46.6,  18.5)),
      1995: ((20124,  37613,  58698,  91012,  157919), (3.7,  9.1,  15.2,  23.3,  48.7,  21.0)),
      2000: ((22320,  41103,  64985,  101844,  180879), (3.6,  8.9,  14.8,  23.0,  49.8,  22.1)),
      2002: ((21361,  39795,  63384,  100170,  178844), (3.5,  8.8,  14.8,  23.3,  49.7,  21.7)),
      2003: ((20974,  39652,  63505,  101307,  179740), (3.4,  8.7,  14.8,  23.4,  49.8,  21.4)),
      2004: ((20992,  39375,  62716,  99930,  178453), (3.4,  8.7,  14.7,  23.2,  50.1,  21.8)),
      2005: ((21071,  39554,  63352,  100757,  182386), (3.4,  8.6,  14.6,  23.0,  50.4,  22.2)),
      2006: ((21314,  40185,  63830,  103226,  185119), (3.4,  8.6,  14.5,  22.9,  50.5,  22.3)),
      2007: ((20991,  40448,  64138,  103448,  183103), (3.4,  8.7,  14.8,  23.4,  49.7,  21.2)),
      2008: ((20633,  38852,  62487,  99860,  179317), (3.4,  8.6,  14.7,  23.3,  50.0,  21.5)),
      2009: ((20453,  38550,  61801,  100000,  180001), (3.4,  8.6,  14.6,  23.2,  50.3,  21.7)),
    }

    # http://en.wikipedia.org/wiki/Income_tax_in_the_United_States
    taxes = (10, 15, 15, 15, 25, 35)

    population = (self.households / 5, self.households / 5, self.households / 5, self.households / 5, self.households / 5, self.households / 20)

    incomes = map(lambda x: x[0], table.values())
    shares = map(lambda x: x[1], table.values())
    
    average_income = map(lambda x: x / len(incomes), reduce(lambda x, y: map(operator.add, x, y), incomes))
    average_share = map(lambda x: (x / 100) / len(shares), reduce(lambda x, y: map(operator.add, x, y), shares))
    tax_share = map(lambda x: float(x) / sum(taxes), taxes)

    combined_share = map(lambda x: average_share[x] * tax_share[x], range(0,6))
    combined_share = map(lambda x: combined_share[x] / sum(combined_share), range(0,6))

    print 'INCOMES             ', average_income
    #print 'SHARES', average_share
    #print 'TAX SHARES', tax_share

    # Falt Tax
    flat = map(lambda x: '%.2f' % ((average_share[x] * self.debt) / population[x] / self.family), range(0,6))
    print 'FLAT TAX DEBT       ', flat

    # Progressive Tax
    progressive = map(lambda x: '%.2f' % ((tax_share[x] * self.debt) / population[x] / self.family), range(0,6))
    print 'PROGRESSIVE TAX DEBT', progressive

    # Combined
    combined = map(lambda x: '%.2f' % ((combined_share[x] * self.debt) / population[x] / self.family), range(0,6))
    print 'COMBINED TAX DEBT   ', combined




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-i ', '--income', action="store", required=True, help='Annual household income.')
  results = parser.parse_args(sys.argv[1:])

  tax_debt = TaxDebt()
  tax_debt.get_percentile(int(results.income))
