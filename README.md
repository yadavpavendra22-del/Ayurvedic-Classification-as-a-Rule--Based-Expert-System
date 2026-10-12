# Ayurvedic Classification as a Rule-Based Expert System

## Project Overview

This project implements an Ayurvedic Prakriti Classification system using a rule-based expert system. It classifies an individual's constitution into Vata, Pitta, Kapha, dual-dosha, or Tridoshic (Sama) categories based on selected physical and behavioral characteristics.

The system uses Python, IF-THEN production rules, and a forward-chaining inference engine to evaluate user-provided attributes and generate an explainable classification result.

## Academic Details

* **Project Title:** Ayurvedic Classification as a Rule-Based Expert System
* **Student Name:** Pavendra Yadav
* **Course:** Bachelor of Science (B.Sc.) in Computer Science
* **Semester:** V
* **Academic Year:** 2026–2027
* **College:** Smt. Devkiba Mohansinhji Chauhan College of Commerce and Science, Silvassa
* **Project Guide:** Asst. Prof. Sini V.

## Objectives

* Represent Ayurvedic Prakriti assessment using a structured knowledge base.
* Implement a deterministic rule-based classification algorithm.
* Apply forward chaining to evaluate user-provided facts.
* Calculate Vata, Pitta, and Kapha scores.
* Provide explanations showing which rules were activated.
* Validate input data and handle insufficient or invalid responses.
* Test the system using multiple test cases.

## Technologies Used

* **Programming Language:** Python 3
* **Concepts:** Artificial Intelligence, Expert Systems, Rule-Based Reasoning
* **Inference Method:** Forward Chaining
* **Testing Framework:** Python `unittest`
* **Dependencies:** Python Standard Library

## System Features

1. **Knowledge Base:** Contains 30 IF-THEN production rules.
2. **Attribute Assessment:** Evaluates 10 attributes, including body frame, skin, hair, appetite, digestion, sleep, temperament, climate preference, speech, and memory.
3. **Dosha Scoring:** Assigns weighted scores to Vata, Pitta, and Kapha.
4. **Classification Engine:** Identifies pure, dual-dosha, or balanced constitutions.
5. **Explanation Module:** Displays the rules activated during classification.
6. **Input Validation:** Rejects unknown attributes and invalid values.
7. **Insufficient Data Handling:** Requires at least 6 answered attributes.
8. **Automated Testing:** Includes 16 test cases covering normal, boundary, partial, and invalid inputs.

## Project Structure

```text
Ayurvedic-Classification-Expert-System/
|
|-- prakriti_expert_system.py
|-- test_prakriti.py
|-- README.md
```

## Installation and Execution

### Prerequisites

Install Python 3 on your system.

Verify the installation:

```bash
python --version
```

### Clone the Repository

```bash
git clone <your-repository-url>
cd Ayurvedic-Classification-Expert-System
```

### Run the Interactive Program

```bash
python prakriti_expert_system.py
```

Follow the prompts and select the appropriate option for each attribute. Press Enter to skip an attribute.

### Run the Demonstration

```bash
python prakriti_expert_system.py --demo
```

### Run the Test Suite

```bash
python test_prakriti.py
```

## Classification Methodology

The system follows these steps:

1. Collect user-provided attributes.
2. Validate the attributes and their allowed values.
3. Check whether at least six attributes have been answered.
4. Evaluate the production rules using forward chaining.
5. Accumulate weighted scores for all three doshas.
6. Apply the classification and tie-breaking rules.
7. Display the result, scores, and activated rules.

### Classification Categories

| Category          | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| Vata (pure)       | Vata has the highest score with sufficient separation.             |
| Pitta (pure)      | Pitta has the highest score with sufficient separation.            |
| Kapha (pure)      | Kapha has the highest score with sufficient separation.            |
| Dual-dosha        | The two highest scores fall within the defined margin.             |
| Tridoshic (Sama)  | The difference between the highest and lowest scores is at most 1. |
| Insufficient data | Fewer than six attributes are provided.                            |

## Testing

The project includes 16 test cases to verify:

* Pure Vata, Pitta, and Kapha classifications.
* Dual-dosha classifications.
* Tridoshic classification.
* Boundary conditions for classification thresholds.
* Mixed and partial attribute inputs.
* Insufficient data handling.
* Invalid values and unknown attributes.
* Consistency of explanation traces.
* Integrity of the 30-rule knowledge base.

## Complexity Analysis

Let `n` represent the number of answered attributes and `R` represent the number of production rules.

* **Validation:** O(n)
* **Inference:** O(R)
* **Classification:** O(1), because the system ranks only three doshas.
* **Overall Time Complexity:** O(R + n)
* **Space Complexity:** O(R), including the rule trace.

Since the current rule base contains 30 rules, the system is computationally lightweight.

## Limitations

* The system uses a simplified knowledge base of 10 attributes and 30 rules.
* Rule weights and classification thresholds are design choices.
* Results depend on the accuracy of user-provided answers.
* The system does not model Vikriti or changing health conditions.
* The classification is intended for academic demonstration and is not a medical diagnosis or treatment recommendation.

## Conclusion

This project demonstrates how traditional Ayurvedic Prakriti classification concepts can be represented through artificial intelligence techniques. By combining a knowledge base, forward-chaining inference, weighted scoring, and an explanation module, the system provides a transparent and deterministic classification process.

The project also demonstrates fundamental concepts of knowledge representation, rule-based reasoning, algorithm design, input validation, and software testing.

## References

1. Charaka Samhita, Vimana Sthana, Chapter 8.
2. Sushruta Samhita, Sharira Sthana, Chapter 4.
3. Russell, S. and Norvig, P. *Artificial Intelligence: A Modern Approach.*

## Disclaimer

This project is developed for academic and educational purposes only. It is not intended to provide medical diagnosis, treatment, or professional healthcare advice.

## License

This project is intended for academic use. Contact the author for permission before redistributing or reusing the project.
