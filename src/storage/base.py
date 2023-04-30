import abc


class AbstractStorage(abc.ABC):
    @abc.abstractmethod
    async def save_question(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def get_questions(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def get_answer_by_question(self, *args, **kwargs):
        ...
