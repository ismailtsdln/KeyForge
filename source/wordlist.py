#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wordlist Module for Passphrase Generation
Contains EFF's long wordlist for secure, memorable passphrase generation.
"""

import secrets
from typing import List


# EFF's Long Wordlist (subset - full list has 7776 words)
# These are carefully selected words that are easy to type and remember
EFF_WORDLIST = [
    # A-C
    "abacus", "abdomen", "abdominal", "abide", "abiding", "ability", "ablaze", "able",
    "abnormal", "abrasion", "abrasive", "abreast", "abridge", "abroad", "abruptly",
    "absence", "absentee", "absently", "absinthe", "absolute", "absolve", "abstain",
    "abstract", "absurd", "accent", "accept", "access", "accident", "acclaim", "acclimate",
    "accomplish", "accordion", "account", "accuracy", "accurate", "accustom", "acetone",
    "achiness", "aching", "acid", "acorn", "acoustic", "acquaint", "acquire", "acre",
    "acrobat", "acronym", "acting", "action", "activate", "activator", "active", "activism",
    "activist", "activity", "actress", "acts", "acutely", "acuteness", "aeration", "aerobics",
    "aerosol", "aerospace", "afar", "affair", "affect", "affection", "affidavit", "affiliate",
    "affirm", "affix", "afflict", "affluent", "afford", "affront", "aflame", "afloat",
    "aflutter", "afoot", "afraid", "afterglow", "afterlife", "aftermath", "aftermost",
    "afternoon", "afterword", "against", "ageless", "agency", "agenda", "agent", "aggravate",
    "aggregate", "aggressor", "aghast", "agile", "agility", "aging", "agnostic", "agonize",
    "agonizing", "agony", "agree", "agreeable", "agreed", "agreeing", "agreement", "aground",
    "ahead", "ahoy", "aide", "aim", "ajar", "alabaster", "alarm", "albatross",
    "album", "alchemy", "alcohol", "alcove", "alder", "ale", "alert", "algebra",
    "algorithm", "alias", "alibi", "alien", "alienable", "alienate", "aliens", "alike",
    "alive", "alkaline", "alkalize", "almanac", "almighty", "almost", "aloe", "aloft",
    "aloha", "alone", "alongside", "aloof", "alphabet", "alphabetic", "alpine", "already",
    "also", "altar", "alter", "altered", "alternate", "although", "altitude", "alto",
    "aluminum", "alumni", "always", "amaretto", "amaze", "amazingly", "amber", "ambiance",
    "ambiguity", "ambiguous", "ambition", "ambitious", "ambulance", "ambush", "amendable",
    "amendment", "amends", "amenity", "amiable", "amicably", "amid", "amigo", "amino",
    "amiss", "ammonia", "ammonium", "amnesty", "amniotic", "among", "amount", "amperage",
    "ample", "amplifier", "amplify", "amply", "amuck", "amulet", "amusable", "amused",
    "amusement", "amuser", "amusing", "anaconda", "anaerobic", "anagram", "anatomist",
    "anatomy", "anchor", "anchovy", "ancient", "android", "anemia", "anemic", "aneurism",
    "anew", "angelfish", "angelic", "anger", "angled", "angler", "angles", "angling",
    "angrily", "angriness", "anguished", "angular", "animal", "animate", "animating",
    "animation", "animator", "anime", "animosity", "ankle", "annex", "annotate", "announcer",
    "annoying", "annual", "annually", "annuity", "anointer", "another", "answering",
    "antarctic", "anteater", "antelope", "antennae", "anthem", "anthill", "anthology",
    "antibody", "antics", "antidote", "antihero", "antiquely", "antiques", "antiquity",
    "antirust", "antitoxic", "antitrust", "antiviral", "antivirus", "antler", "antonym",
    "antsy", "anvil", "anybody", "anyhow", "anymore", "anyone", "anyplace", "anything",
    "anytime", "anyway", "anywhere", "aorta", "apache", "apostle", "appealing",
    "appear", "appease", "appeasing", "appendage", "appendix", "appetite", "appetizer",
    "applaud", "applause", "apple", "appliance", "applicant", "applied", "apply", "appoint",
    "appointee", "appraisal", "appraise", "appraiser", "apprehend", "approach", "approval",
    "approve", "approving", "apricot", "april", "apron", "aptitude", "aptly", "aptness",
    "aqua", "aquarium", "aquatic", "aqueduct", "arbitrary", "arbitrate", "ardently",
    "area", "arena", "arguable", "arguably", "argue", "arise", "armadillo", "armband",
    "armchair", "armed", "armful", "armhole", "arming", "armless", "armoire", "armored",
    "armory", "armrest", "army", "aroma", "arose", "around", "arousal", "arrange",
    "array", "arrest", "arrival", "arrive", "arrogance", "arrogant", "arson", "art",
    "artery", "artful", "article", "artifice", "artillery", "artist", "asbestos",
    "ascend", "ascension", "ascent", "ascertain", "ashamed", "ashen", "ashes", "ashy",
    "aside", "askew", "asleep", "asparagus", "aspect", "aspirate", "aspire", "aspirin",
    "astonish", "astound", "astride", "astrology", "astronaut", "astronomy", "astute",
    "atlantic", "atlas", "atom", "atonable", "atop", "atrium", "atrocious", "atrophy",
    "attach", "attain", "attempt", "attend", "attendant", "attendee", "attention", "attentive",
    "attest", "attic", "attire", "attitude", "attractor", "attribute", "atypical",
    "auction", "audacious", "audacity", "audible", "audibly", "audience", "audio", "audition",
    "augmented", "august", "authentic", "author", "autism", "autistic", "autograph",
    "automaker", "automated", "automatic", "autopilot", "available", "avalanche", "avatar",
    "avenge", "avenue", "average", "aversion", "avert", "aviation", "aviator", "avid",
    "avoid", "await", "awaken", "award", "aware", "awhile", "awkward", "awning",
    "awoke", "awry", "axis", "babble", "babbling", "babied", "baboon", "backache",
    "backboard", "backboned", "backdrop", "backed", "backer", "backfield", "backfire",
    "backhand", "backing", "backlands", "backlash", "backless", "backlight", "backlit",
    "backlog", "backpack", "backpedal", "backrest", "backroom", "backshift", "backside",
    "backslid", "backspace", "backspin", "backstab", "backstage", "backtalk", "backtrack",
    "backup", "backward", "backwash", "backwater", "backyard", "bacon", "bacteria", "bacterium",
    "badass", "badge", "badland", "badly", "badness", "baffle", "baffling", "bagel",
    "baggage", "bagged", "baggie", "bagginess", "bagging", "baggy", "bagpipe", "baguette",
    # ... truncated for brevity - in a real implementation, include all 7776 words
    "zebra", "zenith", "zeppelin", "zero", "zest", "zigzag", "zipfile", "zipper",
    "zipping", "zirconium", "zodiac", "zombie", "zone", "zoning", "zookeeper", "zoologist",
    "zoology", "zoom", "zucchini"
]


def get_random_words(count: int = 4) -> List[str]:
    """
    Get random words from the EFF wordlist.
    
    Args:
        count: Number of words to retrieve
    
    Returns:
        List of random words
        
    Raises:
        ValueError: If count < 1
    """
    if count < 1:
        raise ValueError("Count must be at least 1")
    
    return [secrets.choice(EFF_WORDLIST) for _ in range(count)]


def get_wordlist_size() -> int:
    """
    Get the size of the wordlist.
    
    Returns:
        Number of words in the wordlist
    """
    return len(EFF_WORDLIST)


def calculate_passphrase_entropy(word_count: int) -> float:
    """
    Calculate the entropy of a passphrase based on word count.
    
    Args:
        word_count: Number of words in the passphrase
    
    Returns:
        Entropy in bits
    """
    import math
    return word_count * math.log2(len(EFF_WORDLIST))
