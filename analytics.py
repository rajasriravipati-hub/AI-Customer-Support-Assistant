import pandas as pd


class Analytics:

    def __init__(self):

        self.total_questions = 0

        self.question_history = []

    def add_question(
        self,
        question
    ):

        self.total_questions += 1

        self.question_history.append(
            question
        )

    def get_total_questions(
        self
    ):

        return self.total_questions

    def get_dataframe(
        self
    ):

        return pd.DataFrame(
            self.question_history,
            columns=["Questions"]
        )


analytics = Analytics()