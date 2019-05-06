from Calender import Calender


class ChatBotAnswer:

    @staticmethod
    def get_aet_tim_answer(par_question):
        return Calender.get_current_event()
