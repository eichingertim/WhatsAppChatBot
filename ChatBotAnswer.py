class ChatBotAnswer:

    @staticmethod
    def get_aet_all_answer(par_question):
        with open("answer_database/chat_bot_answers_aet_all.csv", "r") as file:
            for line in file:
                splitted_line = line.strip().split(';')
                if splitted_line[2] == "Antwort":
                    continue
                question = splitted_line[1].lower()
                answer = splitted_line[2]

                if question in str(par_question).lower():
                    return answer
                elif question == str(par_question).lower():
                    return answer

    @staticmethod
    def get_aet_tim_answer(par_question):
        with open("answer_database/chat_bot_answers_aet_tim.csv", "r") as file:
            for line in file:
                splitted_line = line.strip().split(';')
                if splitted_line[2] == "Antwort":
                    continue
                question = splitted_line[1].lower()
                answer = splitted_line[2]

                if question in str(par_question).lower():
                    return answer
                elif question == str(par_question).lower():
                    return answer
