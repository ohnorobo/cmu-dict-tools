#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import codecs


CMU_DICT_FILE = "data/cmudict/cmudict.0.7a"
# returns a dictionary if {english_word : [phoneme-reps]}
# some english words have more than one phoneme repr
# a phoneme repr looks like ['RE', 'EH1', 'V', 'Z']
def read_in_cmudict():
  d = {}
  f = open(CMU_DICT_FILE, 'r')
  for line in f:
    if line[0].isalpha(): #drop comments and punctuation
      content = line.split()
      word = content[0]
      pron = content[1:]

      if word[-3:] in ["(1)", "(2)", "(3)"]: #alternate pron
        word = word[:-3]
        if word in d:
          d[word].append(pron)
        else: d[word] = [pron]
      else: #new word
        d[word] = [pron]
  return d

CONVERSION_FILE = "data/conversions"
# read in conversion data between CMU/IPA/TIMBL
# returns 2 dictionaries, one from CMU to IPA,
# one from CMU to TIMBL
def read_in_conversion():
  ipa_conv = {}
  timbl_conv = {}

  f = codecs.open(CONVERSION_FILE, 'r', encoding='utf-8')
  for line in f:
    if line[0].isalpha(): #drop comments and empty lines
      cmu, timbl, ipa = line.split()
      ipa_conv[cmu] = ipa
      timbl_conv[cmu] = timbl
  return ipa_conv, timbl_conv
IPA_CONV, TIMBL_CONV = read_in_conversion()

# takes ['RE', 'EH1', 'V', 'Z']
# returns 
def ipa(phonemes):
  ipa = []
  for phone in phonemes:
    ipa.append(IPA_CONV[phone])
  return "".join(ipa)


#takes cmu-phones
#reutrns timbl
def timbl(phonemes):
  pass


if __name__ == "__main__":
  d = read_in_cmudict()
  #pprint(d)
  for word in sorted(d.keys()):
    print(word)
    prons = d[word]
    for pron in prons:
      print("   " + ipa(pron).encode('utf-8'))
