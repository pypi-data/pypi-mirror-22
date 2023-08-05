Can generate random strings of upper and lowercase alphabets.
Requires length of string or number of words as input.

## INSTALLATION 
pip install randStringify

Functions :
withLength(length , custom='str')
withWords(wordlimit , custom='str')

Import :
from genstr as r

Use :
r.generate.withLength(50)
r.generate.withWords(10)

prototype = 'asdfwe234'
r.generate.withWords(10 , custom=prototype)