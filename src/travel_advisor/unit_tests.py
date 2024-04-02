import logging
from langchain.llms import GooglePalm
import logging
import time
from langchain.chains.question_answering import load_qa_chain
from templates import ValidationTemplate
from dotenv import load_dotenv
import os
logging.basicConfig(level=logging.INFO)
from langchain.chains import LLMChain, SequentialChain
load_dotenv()
from initialize_models import Agent
import unittest




travel_agent = Agent(llm_api_key=os.environ["GOOGLE_PALM_API_KEY"],debug=True)

query1 = """
        I want to do a 4 day roadtrip from Delhi to chail (HP) in India.
        I want to visit remote locations with mountain views
        """


query2 = """
        I want to walk from Kashmir to Kanyakumari in 4 days.
        """

# result = travel_agent.validate_travel(query2)


_,result = travel_agent.plan(query1)
print(result)

