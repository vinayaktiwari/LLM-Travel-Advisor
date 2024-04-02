import os

MODEL_NAME = "models/text-bison-001"  # palm
TEMPERATURE = 0.2
DUMPED_MAPS_DIR = os.path.join(os.getcwd(), "maps")

EXAMPLE_QUERY = """
I want to do 4 day trip from Delhi to Manali.
I want to visit remote locations and beautiful mountain views.
"""
VALID_MESSAGE = "Plan is valid"