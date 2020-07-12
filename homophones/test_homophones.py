from homophones import homophones as h


def test_dipronunciations():
  word = h.Word("BELCHING", h.Pronunciation(["B", "EH1", "L", "CH", "IH0", "NG",]))
  assert list(h.dipronunciations(word)) == [
    (h.Pronunciation(["B"]), h.Pronunciation(["EH1", "L", "CH", "IH0", "NG",])),
    (h.Pronunciation(["B", "EH1"]), h.Pronunciation(["L", "CH", "IH0", "NG",])),
    (h.Pronunciation(["B", "EH1", "L"]), h.Pronunciation(["CH", "IH0", "NG",])),
    (h.Pronunciation(["B", "EH1", "L", "CH"]), h.Pronunciation(["IH0", "NG",])),
    (h.Pronunciation(["B", "EH1", "L", "CH", "IH0"]), h.Pronunciation(["NG",])),
  ]


def test_from_string():
  words = [
    h.Word("BELCHING", h.Pronunciation(["B", "EH1", "L", "CH", "IH0", "NG",])),
    h.Word("BELCOURT", h.Pronunciation(["B", "EH1", "L", "K", "AO2", "R", "T",])),
    h.Word("BELDEN", h.Pronunciation(["B", "EH1", "L", "D", "AH0", "N",])),
  ]
  assert next(h.Word.from_string("bElCourt", words)) == \
      h.Word("BELCOURT", h.Pronunciation(["B", "EH1", "L", "K", "AO2", "R", "T",]))
  assert next(h.Word.from_string("bElCourt", words)) != \
    h.Word("BELDEN", h.Pronunciation(["B", "EH1", "L", "D", "AH0", "N",])  )


def test_remove_stress():
  pros = [
    ["AE2", "K", "Y", "UW0", "Z", "EY1", "SH", "AH0", "N", "Z",],
    ["AH0", "K", "Y", "UW1", "Z", "AH0", "T", "IH0", "V",],
    ["AH0", "K", "Y", "UW1", "Z", "AH0", "T", "AO2", "R", "IY0",],
    ["AH0", "K", "Y", "UW1", "Z",],
    ["AH0", "K", "Y", "UW1", "Z", "D",],
    ["AH0", "K", "Y", "UW1", "Z", "ER0",],
    ["AH0", "K", "Y", "UW1", "Z", "ER0", "Z",],
    ["AH0", "K", "Y", "UW1", "Z", "IH0", "Z",],
    ["AH0", "K", "Y", "UW1", "Z", "IH0", "NG",],
    ["AH0", "K", "Y", "UW1", "Z", "IH0", "NG", "L", "IY0",],
    ["AH0", "K", "AH1", "S", "T", "AH0", "M",],
  ]
  assert(h.remove_stress(pros[0]) ==  ["AE", "K", "Y", "UW", "Z", "EY", "SH", "AH", "N", "Z",])
  assert(h.remove_stress(pros[1]) ==  ["AH", "K", "Y", "UW", "Z", "AH", "T", "IH", "V",])
  assert(h.remove_stress(pros[2]) ==  ["AH", "K", "Y", "UW", "Z", "AH", "T", "AO", "R", "IY",])
  assert(h.remove_stress(pros[3]) ==  ["AH", "K", "Y", "UW", "Z",])
  assert(h.remove_stress(pros[4]) ==  ["AH", "K", "Y", "UW", "Z", "D",])
  assert(h.remove_stress(pros[5]) ==  ["AH", "K", "Y", "UW", "Z", "ER",])
  assert(h.remove_stress(pros[6]) ==  ["AH", "K", "Y", "UW", "Z", "ER", "Z",])
  assert(h.remove_stress(pros[7]) ==  ["AH", "K", "Y", "UW", "Z", "IH", "Z",])
  assert(h.remove_stress(pros[8]) ==  ["AH", "K", "Y", "UW", "Z", "IH", "NG",])
  assert(h.remove_stress(pros[9]) ==  ["AH", "K", "Y", "UW", "Z", "IH", "NG", "L", "IY",])
  assert(h.remove_stress(pros[10]) ==  ["AH", "K", "AH","S", "T", "AH", "M",])
