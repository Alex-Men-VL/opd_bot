from dataclasses import (
    dataclass,
    field,
)
from itertools import count


@dataclass
class QuestionDTO:
    pk: int = field(default_factory=count().__next__, init=False)
    text: str
    answer: str


@dataclass
class CategoryDTO:
    title: str
    questions: list[QuestionDTO] = field(default_factory=list)


class CategoryDTOStruct(list[CategoryDTO]):
    def get_categories(self) -> list[str]:
        return [category.title for category in self]

    def get_questions_by_category(self, category: str) -> list[QuestionDTO] | None:
        value = list(filter(lambda x: x.title == category, self))
        return value[0].questions if value else []

    def get_question_by_pk(self, pk: int) -> QuestionDTO | None:
        for category in self:
            for question in category.questions:
                if question.pk == pk:
                    return question
