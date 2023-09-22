from clck.phonology.phonotactics2 import GeneratorRule, Phonotactics, PostGenerationRule, PreGenerationRule


def is_pre_generation_rule(rule: GeneratorRule) -> bool:
    match rule:
        case PreGenerationRule():
            return True
        case _:
            return False

 
def is_post_generation_rule(rule: GeneratorRule) -> bool:
    match rule:
        case PostGenerationRule():
            return True
        case _:
            return False


def fetch_rules(phonotactics: Phonotactics,
        subtype: type[GeneratorRule]) -> tuple[GeneratorRule, ...]:
    """
    Returns a tuple of generator rules based on the given :GeneratorRule:
    subtype.
    """
    rl: list[GeneratorRule] = []
    for rule in phonotactics.rules:
        match rule:
            case subtype():
                rl.append(rule)
    
    return tuple(rl)


def fetch_pre_generation_rules(phonotactics: Phonotactics) -> tuple[GeneratorRule]:
    """Returns a tuple of pre-generation phonotactic rules."""
    return fetch_rules(phonotactics, PreGenerationRule)


def fetch_post_generation_rules(phonotactics: Phonotactics) -> tuple[GeneratorRule]:
    """Returns a tuple of post-generation phonotactic rules."""
    return fetch_rules(phonotactics, PostGenerationRule)