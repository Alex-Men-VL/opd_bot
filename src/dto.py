from dataclasses import dataclass


@dataclass
class QuestionDTO:
    question: str
    answer: str
