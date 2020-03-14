from reglist import reglist

alphalist = reglist.build('[a-z]')
print('\nAlpha List:', alphalist)

upperlist = reglist.build('[A-Z]')
print('\nUpper List:', upperlist)

numlist = reglist.build('[0-9]')
print('\nNumerical List:', numlist)

alnumlist = reglist.build('[a-zA-Z0-9]')
print('\nAlnum List:', alnumlist)