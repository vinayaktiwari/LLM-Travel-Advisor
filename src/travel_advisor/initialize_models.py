import logging
from langchain.llms import GooglePalm
import logging
import time
from langchain.chains.question_answering import load_qa_chain
from templates import ValidationTemplate, PlannerTemplate, MappingTemplate
from dotenv import load_dotenv
import os
logging.basicConfig(level=logging.INFO)
from langchain.chains import LLMChain, SequentialChain
load_dotenv()


class Agent:
    def __init__(self,
                 llm_api_key,
                 temperature =0.3,
                 debug=True):
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Base LLM is Google Palm")
        self.chat_model = GooglePalm(
                temperature=temperature,
                google_api_key=llm_api_key,
            )
        
        self.palm_key = llm_api_key
        self.validation_prompt = ValidationTemplate()
        self.planner_prompt = PlannerTemplate()
        self.mapping_prompt = MappingTemplate()

        self.validation_chain = self.set_up_validation_chain(debug)
        self.actual_chain = self.set_up_agent_chain(debug)  
        

    
    
    def set_up_validation_chain(self,debug= True):
        validation_agent = LLMChain(llm=self.chat_model,
                                    prompt=self.validation_prompt.chat_prompt,
                                    output_parser=self.validation_prompt.parser,
                                    output_key="validation_output",
                                    verbose = debug)
        
        # add to sequential chain 
        overall_chain = SequentialChain(
            chains=[validation_agent],
            input_variables=["query", "format_instructions"],
            output_variables=["validation_output"],
            verbose=debug,
        )
        return overall_chain
    

    def set_up_agent_chain(self,debug= True):
        planner_agent = LLMChain(llm=self.chat_model,
                                    prompt=self.planner_prompt.chat_prompt,
                                    output_key="agent_output",
                                    verbose = debug)
        
        parser = LLMChain(
            llm=self.chat_model,
            prompt=self.mapping_prompt.chat_prompt,
            output_parser=self.mapping_prompt.parser,
            verbose=debug,
            output_key="mapping_list",
        )
        
        # add to sequential chain 
        overall_chain = SequentialChain(
            chains=[planner_agent,parser],
            input_variables=["query","format_instructions"],
            output_variables=["agent_output","mapping_list"],
            verbose=debug,
        )
        return overall_chain



    def validate_travel(self, query):
        self.logger.info("Validating query")
        t1 = time.time()
        self.logger.info(
            "Calling validation (model is {}) on user input".format(
                self.chat_model.model_name
            )
        )
        validation_result = self.validation_chain(
            {
                "query": query,
                "format_instructions": self.validation_prompt.parser.get_format_instructions(),
            }
        )

        validation_test = validation_result["validation_output"].dict()
        t2 = time.time()
        self.logger.info("Time to validate request: {}".format(round(t2 - t1, 2)))

        return validation_test
    

    def plan(self, query):
        self.logger.info("Actual query")
        t1 = time.time()
        self.logger.info(
            "Calling Actual (model is {}) on user input".format(
                self.chat_model.model_name
            )
        )

        result = self.actual_chain(
            { "query": query,"format_instructions": self.mapping_prompt.parser.get_format_instructions(),
            }
        )

        planner_output = result["agent_output"]
        places_of_visit_dict = result["mapping_list"].dict()

        t2 = time.time()
        self.logger.info("Time to request: {}".format(round(t2 - t1, 2)))

        return planner_output,places_of_visit_dict
    
    



    


# travel_agent = Agent(llm_api_key=os.environ["GOOGLE_PALM_API_KEY"],debug=True)

# query = """
#         I want to do a 5 day roadtrip from Delhi to Ladakh in India.
#         I want to visit remote locations with mountain views
#         """

# travel_agent.validate_travel(query)