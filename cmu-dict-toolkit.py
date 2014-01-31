#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import codecs


###Utility Functions###
#######################

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
# returns rɛvz
def ipa(phonemes):
  ipa = []
  for phone in phonemes:
    ipa.append(IPA_CONV[phone])
  return "".join(ipa)

STRESS_MARKS = ['-', '\\', '/']
# 0 - , unstressed
# 1 \ , primary stress
# 2 / , secondary stress

# takes ['AE1', 'M', 'P', 'ER0', 'S', 'AE2', 'N', 'D']
# \  - /
# æmpɚsænd
def ipa_stress(phonemes):
  stress = []
  for phone in phonemes:
    ipa = IPA_CONV[phone]
    if not phone.isalpha():
      if '0' in phone:
        stress.append(STRESS_MARKS[0])
      elif '1' in phone:
        stress.append(STRESS_MARKS[1])
      elif '2' in phone:
        stress.append(STRESS_MARKS[2])

      stress.append(' '*(len(ipa)-2))
    else:
      stress.append(' '*len(ipa))

  return "".join(stress)



###TRAIING###
#############

# Unsupervized alignment finding for grapheme/phoneme matches
#
# 1
# measure unigram/bigrams probs for
# graphemes
# phonemes
#
# 1.2
# choose a set of random grapheme - [phonemes] probs
# ???
#
# 2
# then find the 'best pairing' for each word
#
# 3
# measure co-occurence probs for
# grapheme -> [phoneme] s
#
# measure amt of change from the last set of co-occurence probs
#
# repeat 2 and 3 until convergence

# returns a model
def run_training():
  pass


def get_unigram_grapheme_counts(dic):
  pass

def get_unigram_phoneme_counts(dic):
  pass

def get_bigram_grapheme_counts(dic):
  pass

def get_bigram_phoneme_counts(dic):
  pass

def get_random_co_counts():
  pass








###UNIT TESTING###
##################

if __name__ == "__main__":
  d = read_in_cmudict()
  #pprint(d)
  for word in sorted(d.keys()):
    print(word)
    prons = d[word]
    for pron in prons:
      print("   " + ipa_stress(pron))
      print("   " + ipa(pron).encode('utf-8'))

import unittest

class TestCMUTools(unittest.TestCase):

  def test_ipa_stress(self):
    phonemes = ['AE1', 'M', 'P', 'ER0', 'S', 'AE2', 'N', 'D']
    self.assertEqual("\  - /  ", ipa_stress(phonemes))
     # \  - /
     # æmpɚsænd

  def test_ipa(self):
    phonemes = ['R', 'EH1', 'V', 'Z']
    self.assertEqual(u"r\025bvz", ipa(phonemes))
