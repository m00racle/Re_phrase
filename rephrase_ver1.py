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
    
    def messenger(self, content:str):
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
        definition = self.getCompletion(messages, temperature=0.1)
        self.definitions.append(definition)
        return definition
    
    def getDefinintions(self):
        return self.definitions

    def giveRating(self, answer):
        """  
            Give rating from the paraphrasing or answer
            Apabila paraphrasing terlalu mirip aslinya juga tidak baik
            apabila terlalu jauh dari konsep juga tidak baik

            Parameter:
            answer: String = the answer posted to tutor

            return : int = score of the answer
        """
        constraints = [
            " apabila uraian semakin dekat isinya ke definisi maka nilainya semakin berkurang",
            " apabila uraian semakin jauh isinya dari definisi maka nilainya semakin berkurang"
        ]
        definition = self.getDefinintions()[-1]
        draft = "ketika ada definisi: " + definition + " kemudian untuk melatih pemahaman siswa memberikan uraian singkat menggunakan bahasa mereka sendiri sebagai berikut: " + answer + ", berikan penilaian berupa angka tanpa uraian antara 1 hingga 10 terhadap uraian tadi dengan batasan sebagai berikut: " + constraints[0] + constraints[1]
        content = self.messenger(draft)
        rating = self.getCompletion(content, temperature=1, max_tokens=10)
        return rating


def run_test():
    """  
    Running manual test on the project
    This is useful to grasp context on how the program is running
    """
    tutor = Tutor()
    print(f'\ntrial definisi Energi:\n {tutor.giveDefinition("Fisika", "Energi")}')
    print(tutor.getDefinintions())
    uraian = "energi pada dasarnya apa yang bisa membuat dan atau dihasilkan ketika ada yang berubah dalam suatu sistem"
    print(f"\npenilaian atas ulasan: {tutor.giveRating(uraian)}")

if __name__ == '__main__':
    run_test()
