import unittest
from prakriti_expert_system import prakriti, KNOWLEDGE, RULES


def build(**dosha_by_attr):
    """Helper: build facts from {attribute: 'V'|'P'|'K'}."""
    idx = {"V": 0, "P": 1, "K": 2}
    facts = {}

    for attr, d in dosha_by_attr.items():
        facts[attr] = list(KNOWLEDGE[attr])[idx[d]]

    return facts


ALL = [
    "frame", "skin", "hair", "appetite", "digestion",
    "sleep", "temperament", "climate", "speech", "memory"
]


def mix(v=(), p=(), k=()):
    m = {}
    m.update({a: "V" for a in v})
    m.update({a: "P" for a in p})
    m.update({a: "K" for a in k})

    assert sorted(m) == sorted(ALL)

    return build(**m)


class TestPrakriti(unittest.TestCase):

    def check(self, facts, result, scores=None):
        out = prakriti(facts)
        self.assertEqual(out["result"], result)

        if scores:
            self.assertEqual(out["scores"], scores)

        return out

    def test01_pure_vata(self):
        self.check(
            mix(v=ALL),
            "Vata (pure)",
            {"Vata": 12, "Pitta": 0, "Kapha": 0}
        )

    def test02_pure_pitta(self):
        self.check(
            mix(p=ALL),
            "Pitta (pure)",
            {"Vata": 0, "Pitta": 12, "Kapha": 0}
        )

    def test03_pure_kapha(self):
        self.check(
            mix(k=ALL),
            "Kapha (pure)",
            {"Vata": 0, "Pitta": 0, "Kapha": 12}
        )

    def test04_vata_pitta_dual(self):
        f = mix(
            v=["frame", "digestion", "sleep", "appetite"],
            p=[
                "skin", "hair", "temperament",
                "climate", "speech", "memory"
            ]
        )

        self.check(
            f,
            "Vata-Pitta (dual)",
            {"Vata": 6, "Pitta": 6, "Kapha": 0}
        )

    def test05_pitta_kapha_dual(self):
        f = mix(
            p=["frame", "digestion", "skin", "hair"],
            k=[
                "appetite", "sleep", "temperament",
                "climate", "speech", "memory"
            ]
        )

        self.check(
            f,
            "Pitta-Kapha (dual)",
            {"Vata": 0, "Pitta": 6, "Kapha": 6}
        )

    def test06_vata_kapha_dual_canonical_order(self):
        f = mix(
            k=["frame", "digestion", "skin", "hair"],
            v=[
                "appetite", "sleep", "temperament",
                "climate", "speech", "memory"
            ]
        )

        self.check(
            f,
            "Vata-Kapha (dual)",
            {"Vata": 6, "Pitta": 0, "Kapha": 6}
        )

    def test07_boundary_margin_equal_is_dual(self):
        # 7 vs 5, difference == MARGIN
        f = mix(
            v=["frame", "digestion", "skin", "hair", "sleep"],
            p=["appetite", "temperament", "climate", "speech", "memory"]
        )

        self.check(
            f,
            "Vata-Pitta (dual)",
            {"Vata": 7, "Pitta": 5, "Kapha": 0}
        )

    def test08_just_beyond_margin_is_pure(self):
        # 7 vs 4 vs 1, difference between top two is 3
        f = mix(
            v=["frame", "digestion", "skin", "hair", "sleep"],
            p=["appetite", "temperament", "climate", "speech"],
            k=["memory"]
        )

        self.check(
            f,
            "Vata (pure)",
            {"Vata": 7, "Pitta": 4, "Kapha": 1}
        )

    def test09_tridoshic(self):
        f = mix(
            v=["frame", "skin", "hair"],
            p=["digestion", "appetite", "sleep"],
            k=["temperament", "climate", "speech", "memory"]
        )

        self.check(
            f,
            "Tridoshic (Sama)",
            {"Vata": 4, "Pitta": 4, "Kapha": 4}
        )

    def test10_conflicting_traits(self):
        f = mix(
            v=["frame", "skin", "hair", "sleep"],
            p=["digestion", "appetite", "temperament"],
            k=["climate", "speech", "memory"]
        )

        self.check(
            f,
            "Vata-Pitta (dual)",
            {"Vata": 5, "Pitta": 4, "Kapha": 3}
        )

    def test11_partial_but_sufficient_input(self):
        f = build(
            frame="V",
            digestion="V",
            skin="V",
            hair="V",
            sleep="V",
            appetite="V",
            speech="V"
        )

        self.check(
            f,
            "Vata (pure)",
            {"Vata": 9, "Pitta": 0, "Kapha": 0}
        )

    def test12_insufficient_input(self):
        out = self.check(
            build(frame="V", skin="P", hair="K", sleep="V"),
            "Insufficient data"
        )

        self.assertIsNone(out["scores"])

    def test13_invalid_value_rejected(self):
        with self.assertRaises(ValueError):
            prakriti({"frame": "gigantic"})

    def test14_unknown_attribute_rejected(self):
        with self.assertRaises(ValueError):
            prakriti({"height": "tall"})

    def test15_explanation_trace_matches_facts(self):
        f = mix(v=ALL)
        out = prakriti(f)

        self.assertEqual(len(out["trace"]), len(f))

        self.assertEqual(
            sum(r["weight"] for r in out["trace"]),
            sum(out["scores"].values())
        )

    def test16_rule_base_size(self):
        self.assertEqual(len(RULES), 30)


if __name__ == "__main__":
    unittest.main(verbosity=2)
