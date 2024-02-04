"""  
this is the file to trial the OpenAI Assistant API
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Tutor:
    """  
    class Tutor will interact with the student (user)
    it will provides:
    thread of learnings with certain topic
    """
    def __init__(self, subject:str) -> None:
        self.subject = subject
        self.client = OpenAI(
            api_key=os.getenv('OPEN_API_KEY')
        )
        self.model = "gpt-3.5-turbo-1106"
        # initiate assitant:
        self.assistant = self.client.beta.assistants.create(
            name = "Tutor " + self.subject,
            instructions="Anda adalah guru Indonesia pengampu pelajaran " + self.subject,
            tools=[{"type": "code_interpreter"}],
            model=self.model
        )
        # initiate thread
        self.thread = self.client.beta.threads.create()
        self.run = None

    def setQueries(self, queries:str):
        """  
        process quries : String = content of message as user
        """
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=queries
        )

        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

    def getStatus(self):
        """  
        return run status of the thread
        """
        if self.run != None:
            return self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id
            )
        else:
            return None
        
    def getResponses(self):
        """  
        return list of response from the assitant's thread
        """
        return self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
    
def run_test():
    tutor_fisika = Tutor("fisika")
    tutor_fisika.setQueries("berikan definisi Energi")
    print(f"\nstatus run: {tutor_fisika.getStatus()}")
    print(f"\nhasil response: {tutor_fisika.getResponses()}")

if __name__ == '__main__':
    run_test()