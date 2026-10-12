"""
IKS Concept as CS Concept
Ayurvedic Prakriti Classification as a Rule-Based Expert System

Components of the expert system
  1. Knowledge base   : RULES (IF attribute = value THEN dosha += weight)
  2. Working memory   : the user's answers (facts)
  3. Inference engine : forward chaining over the rule base
  4. Explanation      : trace of every rule that fired

NOTE: This is a CLASSIFICATION tool for an academic exercise.
      It is NOT a medical diagnosis or treatment system.
"""

import sys

DOSHAS = ("Vata", "Pitta", "Kapha")
MARGIN = 2
TRIDOSHA_SPREAD = 1
MIN_FACTS = 6

# Attribute -> {value: (dosha, weight)}
# Weight 2 for the two major attributes (body frame, digestion), 1 otherwise.
KNOWLEDGE = {
    "frame": {
        "thin": ("Vata", 2),
        "medium": ("Pitta", 2),
        "broad": ("Kapha", 2)
    },
    "skin": {
        "dry": ("Vata", 1),
        "warm_sensitive": ("Pitta", 1),
        "thick_cool": ("Kapha", 1)
    },
    "hair": {
        "dry_thin": ("Vata", 1),
        "fine_early_gray": ("Pitta", 1),
        "thick_oily": ("Kapha", 1)
    },
    "appetite": {
        "irregular": ("Vata", 1),
        "strong_sharp": ("Pitta", 1),
        "slow_steady": ("Kapha", 1)
    },
    "digestion": {
        "gas_constipation": ("Vata", 2),
        "acidity_loose": ("Pitta", 2),
        "sluggish": ("Kapha", 2)
    },
    "sleep": {
        "light_broken": ("Vata", 1),
        "moderate": ("Pitta", 1),
        "deep_long": ("Kapha", 1)
    },
    "temperament": {
        "anxious_quick": ("Vata", 1),
        "irritable_intense": ("Pitta", 1),
        "calm_steady": ("Kapha", 1)
    },
    "climate": {
        "dislikes_cold": ("Vata", 1),
        "dislikes_heat": ("Pitta", 1),
        "dislikes_damp": ("Kapha", 1)
    },
    "speech": {
        "fast_talkative": ("Vata", 1),
        "sharp_precise": ("Pitta", 1),
        "slow_measured": ("Kapha", 1)
    },
    "memory": {
        "quick_forgets": ("Vata", 1),
        "sharp_moderate": ("Pitta", 1),
        "slow_lasting": ("Kapha", 1)
    }
}

# Flatten the knowledge into numbered production rules R01 ... R30
RULES = []

for _attr, _opts in KNOWLEDGE.items():
    for _val, (_dosha, _w) in _opts.items():
        RULES.append({
            "id": f"R{len(RULES) + 1:02d}",
            "attr": _attr,
            "value": _val,
            "dosha": _dosha,
            "weight": _w
        })


def validate(facts):
    """Reject unknown attributes / invalid values (input validation)."""
    if not isinstance(facts, dict):
        raise TypeError("facts must be a dict {attribute: value}")

    for attr, val in facts.items():
        if attr not in KNOWLEDGE:
            raise ValueError(f"Unknown attribute: {attr!r}")

        if val not in KNOWLEDGE[attr]:
            raise ValueError(
                f"Invalid value {val!r} for {attr!r}. "
                f"Allowed: {list(KNOWLEDGE[attr])}"
            )


def infer(facts):
    """Forward chaining: fire every rule whose condition matches the facts."""
    scores = {d: 0 for d in DOSHAS}
    trace = []

    for rule in RULES:
        if facts.get(rule["attr"]) == rule["value"]:
            scores[rule["dosha"]] += rule["weight"]
            trace.append(rule)

    return scores, trace


def classify(scores):
    """Conflict resolution / decision rules on the accumulated scores."""
    ranked = sorted(
        DOSHAS,
        key=lambda d: (-scores[d], DOSHAS.index(d))
    )

    top, second = ranked[0], ranked[1]
    hi, lo = scores[ranked[0]], scores[ranked[2]]

    if hi - lo <= TRIDOSHA_SPREAD:
        return "Tridoshic (Sama)"

    if scores[top] - scores[second] <= MARGIN:
        pair = sorted([top, second], key=DOSHAS.index)
        return f"{pair[0]}-{pair[1]} (dual)"

    return f"{top} (pure)"


def prakriti(facts):
    """Full pipeline: validate -> infer -> classify -> explain."""
    validate(facts)

    if len(facts) < MIN_FACTS:
        return {
            "result": "Insufficient data",
            "scores": None,
            "trace": [],
            "note": f"Need at least {MIN_FACTS} attributes, got {len(facts)}."
        }

    scores, trace = infer(facts)

    return {
        "result": classify(scores),
        "scores": scores,
        "trace": trace,
        "note": ""
    }


def explain(out):
    lines = [f"Result : {out['result']}"]

    if out["scores"]:
        lines.append(
            "Scores : " +
            ", ".join(f"{d}={out['scores'][d]}" for d in DOSHAS)
        )

        lines.append("Rules fired:")

        for r in out["trace"]:
            lines.append(
                f" {r['id']}: {r['attr']} = {r['value']} "
                f"-> {r['dosha']} +{r['weight']}"
            )

    if out["note"]:
        lines.append("Note   : " + out["note"])

    return "\n".join(lines)


def interactive():
    print(
        "=== Prakriti Expert System "
        "(classification only, not medical advice) ==="
    )

    facts = {}

    for attr, opts in KNOWLEDGE.items():
        names = list(opts)

        print(f"\n{attr.upper()}:")

        for i, n in enumerate(names, 1):
            print(f" {i}. {n}")

        choice = input("Choose number (Enter to skip): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(names):
            facts[attr] = names[int(choice) - 1]

    print("\n" + explain(prakriti(facts)))


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo = {
            "frame": "thin",
            "skin": "dry",
            "hair": "dry_thin",
            "appetite": "irregular",
            "digestion": "gas_constipation",
            "sleep": "light_broken",
            "temperament": "anxious_quick",
            "climate": "dislikes_cold",
            "speech": "fast_talkative",
            "memory": "quick_forgets"
        }

        print(explain(prakriti(demo)))
    else:
        interactive()
