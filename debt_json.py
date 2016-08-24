from itertools import izip

def pairwise(t):
    it = iter(t)
    return izip(it,it)

if __name__ == "__main__":

  with open('debt_taxes.js', 'w') as j:
    j.write("/* IRS TAX TABLES: https://www.irs.gov/uac/SOI-Tax-Stats---Individual-Statistical-Tables-by-Size-of-Adjusted-Gross-Income */\n")
    j.write('\n')
    j.write("var taxes_null = { 'bracket_min':0, 'paid':0, 'tax_rate':0, 'total':1 };\n")
    j.write('\n')

    j.write('var taxes = {\n')

    total = 0;
    with open('debt_taxes.csv', 'r') as f:
      for line in f.readlines():
        columns = line.strip().split('\t')

        if len(columns) == 1:
          if columns[0]:
            j.write("  '%s':[\n" % columns[0].strip())
          else:
            j.write("  ],\n" )
        else:
          columns = dict(zip(columns[0::2], columns[1::2]))
          j.write("    { 'bracket_min':%s, 'paid':%s, 'tax_rate':%s },\n" % (columns['bracket_min'].strip(), columns['paid'], columns['tax_rate']))

    j.write('}')
