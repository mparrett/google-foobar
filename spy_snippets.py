"""
Spy snippets
============

You've been recruited by the team building Spy4Rabbits, a highly advanced
search engine used to help fellow agents discover files and intel needed to
continue the operations against Dr. Boolean's evil experiments. The team is
known for recruiting only the brightest rabbit engineers, so there's no
surprise they brought you on board. While you're elbow deep in some important
encryption algorithm, a high-ranking rabbit official requests a nice aesthetic
feature for the tool called "Snippet Search." While you really wanted to tell
him how such a feature is a waste of time in this intense, fast-paced spy
organization, you also wouldn't mind getting kudos from a leader. How hard
could it be, anyway?

When someone makes a search, Spy4Rabbits shows the title of the page. Your
commander would also like it to show a short snippet of the page containing the
terms that were searched for.

Write a function called answer(document, searchTerms) which returns the
shortest snippet of the document, containing all of the given search terms. The
search terms can appear in any order.

The length of a snippet is the number of words in the snippet. For example, the
length of the snippet "tastiest color of carrot" is 4. (Who doesn't like a
delicious snack!)

The document will be a string consisting only of lower-case letters [a-z] and
spaces. Words in the string will be separated by a single space. A word could
appear multiple times in the document.
searchTerms will be a list of words, each word comprised only of lower-case
letters [a-z]. All the search terms will be distinct.

Search terms must match words exactly, so "hop" does not match "hopping".

Return the first sub-string if multiple sub-strings are shortest. For example,
if the document is "world there hello hello where world" and the search terms
are ["hello", "world"], you must return "world there hello".

The document will be guaranteed to contain all the search terms.

The number of words in the document will be at least one, will not exceed 500,
and each word will be 1 to 10 letters long. Repeat words in the document are
considered distinct for counting purposes.
The number of words in searchTerms will be at least one, will not exceed 100,
and each word will not be more than 10 letters long.

Test cases
==========

Inputs:
    (string) document = "many google employees can program"
    (string list) searchTerms = ["google", "program"]
Output:
    (string) "google employees can program"

Inputs:
    (string) document = "a b c d a"
    (string list) searchTerms = ["a", "c", "d"]
Output:
    (string) "c d a"
"""


import sys
import re
from collections import namedtuple


def get_len_by_words(left, right, matches, document):
  """
  Return the count of words separated by spaces in the document
  using a particular left and right from the set of matches
  """
  return document[matches[left].left:matches[right].right].count(' ') + 1


def get_distinct(left, right, matches, document):
  """
  Return a set of distinct terms from the document between the left and
  right match indices. Terms are separated by spaces
  """
  return set(document[matches[left].left:matches[right].right].split(' '))


def answer(document, searchTerms):
  """
  Returns shortest snippet in document containing searchTerms
  Strategy: First, all term matches are located using regex
  Then, all sensible snippet start/end positions are analyzed

  Iterating the matches is kind of nasty, O((n^2+n)/2) where n
  is the number of matches in the document.

  We discard any snippets with less words than the number of
  search terms or snippets that don't contain all the terms

  Thankfully the given constraints are helpful here. The search terms will
  never exceed 100, so we can safely assume we will at most iterate over
  5050 substrings and do more intensive substring checking on much
  less than that.

  Scanning the document itself is a little hairy but regex is faster
  than document.find.
  """

  MatchLocation = namedtuple('Matchlocation', ['term', 'left', 'right'])

  re_matches = re.finditer('|'.join(searchTerms), document)

  matches = []
  for m in re_matches:
    term = m.group(0)
    idx = m.start()
    # Save the term and where it was found and ends
    matches.append(MatchLocation(term, idx, idx + len(term)))

  if len(searchTerms) == 1:
    return document[matches[0].left:matches[0].right]

  # Sort in order so the next loop can skip unnecessary combos
  matches.sort(key=lambda x: x.left)

  candidates = []

  for start in xrange(len(matches)):
    for end in xrange(start + 1, len(matches)):

      # Calculate the word count
      word_count = get_len_by_words(start, end, matches, document)

      if word_count < len(searchTerms):
        continue

      distinct = get_distinct(start, end, matches, document)

      if not distinct.issuperset(searchTerms):
        continue

      # Document string position is used as a tie breaker
      candidates.append((word_count, start, end, matches[start].left))


  def match_compare(x, y):
    """ Sort by word count and use start position as a tie breaker"""
    if x[0] == y[0]:
      return x[2] - y[2]
    return x[0] - y[0]

  candidates.sort(cmp=match_compare, reverse=True)
  best = candidates.pop()

  return document[matches[best[1]].left:matches[best[2]].right]



assert (
  answer("many google employees can program", ["google", "program"])
  == 'google employees can program'
  )

assert(answer("a b c d a", ["c", "d", "a"]) == 'c d a')
assert(answer("a b c d a", ["d", "a", "c"]) == 'c d a')
assert(answer("a b c d a", ["c", "d", "a"]) == 'c d a')

assert(answer("the cats run very fast in the rain", ["cats"]) == 'cats')
assert(answer("the", ["the"]) == 'the')

assert(answer("a b c r z q d a c b a a a a a d d d", ["c", "d", "a"]) == 'd a c')

assert(answer("a b c r z q d a c b a a a a a d d d", ["a"]) == 'a')

assert(answer("world there hello hello where world", ["hello", "world"]) == 'world there hello')

