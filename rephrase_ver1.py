"""  
Main code on re_phrase app
this will includes the interaction of the backend to the OpenAI ChatGPT
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# load the variables in the .env file
load_dotenv()

class Teacher:
    """  
    class teacher which will interact with the student (user)

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

    def getCompletion(self, msg):
        """  
        get the answer form chatGPT on the terms passed as argument
        terms: String = keyword to get the definition from
        return : String = response message content on the definition of the terms
        """
        response = self.client.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    message=msg,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
        # TODO: decouple the response params
        return response.choices[0].message.content
    