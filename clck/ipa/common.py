

from clck.language.containers import PhonemeGroup
from clck.phonology.phonemes import ConsonantPhoneme, VowelPhoneme


DEFAULT_PATTERN_WILDCARDS: dict[str, PhonemeGroup] = {
    "C" : PhonemeGroup.from_type("C", ConsonantPhoneme),
    "V" : PhonemeGroup.from_type("V", VowelPhoneme),
}