#!/usr/bin/env python3

import sys
from vlog import vlog
vlog.GLOBAL_LOG_LEVEL = 1
vl = vlog.vlog

__doc__ = """
Usage: homophones [options] <word>
       homophones --version

Options:
  -v, --version   Show version
  -V, --verbosity=<n>          0 means silent, 10 is maximum
                               [DEFAULT: 1]
  -d, --dictionary=<filename>  A cmudict style phonetic dictionary
                               [DEFAULT: original_cmudict_files/cmudict-0.7b]
  -i, --ignore-stress          Consider words like
  <word>                       Word to find homophones for
"""


def remove_stress(list_of_phonemes):
  to_return = []
  for phoneme in list_of_phonemes:
    if phoneme[-1].isnumeric():
      to_return.append(phoneme[:-1])
    else:
      to_return.append(phoneme)
  return to_return


def sans_alt_counter(word_string):
  """Assumes word counter is one digit in parentheses at end of wordstring"""
  if word_string.endswith(")"):
    return word_string[:-3]
  return word_string


class Pronunciation:
  def __init__(self, list_of_phonemes):
    self.list_of_phonemes = list_of_phonemes

  def __eq__(self, other):
    return self.list_of_phonemes == other.list_of_phonemes

  def eq_sans_stress(self, other):
    return self.sans_stress() == other.sans_stress()

  def sans_stress(self):
    return Pronunciation(remove_stress(self.list_of_phonemes))

  def __str__(self):
    return " ".join(self.list_of_phonemes)


class Word:
  def __init__(self, word, pronunciation):
    self.word = word
    self.pronunciation = pronunciation

  @staticmethod
  def from_cmudict_line(cmudict_line):
    if cmudict_line.startswith(";;;"):
      return None
    line = cmudict_line.strip().split()
    return Word(line[0], Pronunciation(line[1:]))

  @staticmethod
  def from_string(s, words):
    for word in words:
      if sans_alt_counter(word.word).upper() == s.upper():
        yield word

  @staticmethod
  def from_pronunciation(p, words, ignore_stress=False):
    for word in words:
      if word.pronunciation == p or \
          (ignore_stress and word.pronunciation.eq_sans_stress(p)):
        yield word

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    return self.pronunciation == other.pronunciation

  def eq_sans_stress(self, other):
    return self.pronunciation.eq_sans_stress(other.pronunciation)

  def __str__(self):
    return f"{self.word}: " + " ".join(self.pronunciation)


def Words_from_cmudict(filename):
  with open(filename, encoding="ISO-8859-1") as f:
    for line in f:
      to_return = Word.from_cmudict_line(line)
      if to_return != None:
        yield to_return


def homophones(word, words, ignore_stress=False):
  for possible_word in words:
    if possible_word.pronunciation == word.pronunciation or \
        (ignore_stress and possible_word.pronunciation.eq_sans_stress(word.pronunciation)):
      yield possible_word


def dipronunciations(word):
  list_of_phonemes = word.pronunciation.list_of_phonemes
  for i in range(1, len(list_of_phonemes)):
    yield (Pronunciation(list_of_phonemes[:i]), Pronunciation(list_of_phonemes[i:]))


def tripronunciations(word):
  list_of_phonemes = word.pronunciation.list_of_phonemes
  for i in range(1, len(list_of_phonemes) - 1):
    for j in range(i + 1, len(list_of_phonemes)):
      yield (Pronunciation(list_of_phonemes[:i]),
          Pronunciation(list_of_phonemes[i:j]),
          Pronunciation(list_of_phonemes[j:]))


def dihomophones(word, words, ignore_stress=False):
  for dipronunciation in dipronunciations(word):
    vl(2, "  " + " | ".join(map(str, dipronunciation)))
    for first_word in Word.from_pronunciation(dipronunciation[0], words, ignore_stress):
      for second_word in Word.from_pronunciation(dipronunciation[1], words, ignore_stress):
        yield (first_word, second_word)


def trihomophones(word, words, ignore_stress=False):
  for tripronunciation in tripronunciations(word):
    vl(2, "  " + " | ".join(map(str, tripronunciation)))
    for first_word in Word.from_pronunciation(tripronunciation[0], words, ignore_stress):
      for second_word in Word.from_pronunciation(tripronunciation[1], words, ignore_stress):
        for third_word in Word.from_pronunciation(tripronunciation[2], words, ignore_stress):
          yield (first_word, second_word, third_word)


def main():
  from docopt import docopt
  args = docopt(__doc__, version='1.0.0')
  input_word = args["<word>"]
  cmudict = args["--dictionary"]
  ignore_stress = args["--ignore-stress"]
  try:
    vlog.GLOBAL_LOG_LEVEL = int(args["--verbosity"])
  except ValueError as e:
    print(f"--verbosity given '{args['--verbosity']}', need an integer")
    exit(1)

  words = list(Words_from_cmudict(cmudict))
  input_words = list(Word.from_string(input_word, words))

  vl(1, "Homophones:")
  for input_word in input_words:
    vl(2, input_word.word.capitalize())
    for homophone in homophones(input_word, words,
        ignore_stress=ignore_stress):
      vl(2, homophone.word.capitalize())
      vl(1, "  ", end="")
      print(homophone.word.capitalize())

  vl(1, "Dihomophones:")
  for input_word in input_words:
    for dihomophone in dihomophones(input_word, words,
        ignore_stress=ignore_stress):
      vl(1, "  ", end="")
      vl(2, "  ", end="")
      print(dihomophone[0].word.capitalize() + " " + dihomophone[1].word.capitalize())

  vl(1, "Trihomophones:")
  for input_word in input_words:
    for trihomophone in trihomophones(input_word, words,
        ignore_stress=ignore_stress):
      vl(1, "  ", end="")
      vl(2, "  ", end="")
      print(trihomophone[0].word.capitalize() + " " + trihomophone[1].word.capitalize() + " " + trihomophone[2].word.capitalize())


if __name__ ==  "__main__":
  main()
