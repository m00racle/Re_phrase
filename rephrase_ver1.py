"""  
Main code on re_phrase app
this will includes the interaction of the backend to the OpenAI ChatGPT
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# load the variables in the .env file
load_dotenv()

class Tutor:
    """  
    class Tutor which will interact with the student (user)
    it will provides :
    definitions
    grades the paraphrases
    asked questions to test student understandings
    """

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.model = "gpt-3.5-turbo" #<- TODO: decouple this variable
        self.role_content = 'You are an Indonesian Teacher' #<- TODO: decouple this variable

        self.definitions = []
        self.paraphrases = []
        self.ratings = []
        self.questions = []

    def getCompletion(self, msg, **tunes):
        """  
        get the answer form chatGPT on the terms passed as argument
        terms: String = keyword to get the definition from
        return : String = response message content on the definition of the terms
        """
        params = {
            "temperature" : 0.5,
            "max_tokens" : 200,
            "top_p" : 1,
            "frequency_penalty" : 0,
            "presence_penalty" : 0
        }

        for k in tunes:
            if k in params: params[k] = tunes[k]

        # debug
        # print(f"params= {params}")

        response = self.client.chat.completions.create(
                    model=self.model,
                    messages=msg,
                    temperature=params['temperature'],
                    max_tokens=params['max_tokens'],
                    top_p=params['top_p'],
                    frequency_penalty=params['frequency_penalty'],
                    presence_penalty=params['presence_penalty']
                    )
        
        return response.choices[0].message.content
    
    def messenger(self, content):
        """  
        message maker

        Parameters:
        content: String = the completion message content
        """
        return [
            {"role": "system", "content": self.role_content},
            {"role": "user", "content": content}
        ]
    
    def giveDefinition(self, topic, question):
        """  
        get definition from posted question 
        Parameters:
        question : string = Question from the 

        return : string = definition for the questiong
        """
        messages = self.messenger('dari topik: ' + topic +' jelaskan secara singkat: ' + question)
        print(f"messages: {messages}")
        definition = self.getCompletion(messages)
        self.definitions.append(definition)
        return definition
    
    def getDefinintions(self):
        return self.definitions

    def giveRating(self, answer):
        """  
            Give rating from the paraphrasing or answer

            Parameter:
            answer: String = the answer posted to tutor

            return : int = score of the answer
        """
        pass # TODO:


def run_test():
    """  
    Running manual test on the project
    This is useful to grasp context on how the program is running
    """
    tutor = Tutor()
    print(f'trial definisi Energi:\n {tutor.giveDefinition("Fisika", "Energi")}')
    print(tutor.getDefinintions())

if __name__ == '__main__':
    run_test()
