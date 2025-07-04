from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist

# Creating tasks
verification = Task(
    description="Verify the blood test report at {file_path} for user query: {query}",
    expected_output="A verification report confirming the validity of the blood test report",
    agent=verifier,
    async_execution=False
)

help_patients = Task(
    description="Analyze the blood test report at {file_path} and provide medical advice for user query: {query}",
    expected_output="A comprehensive medical analysis with recommendations",
    agent=doctor,
    async_execution=False
)

nutrition_analysis = Task(
    description="Provide nutrition advice based on the blood report at {file_path} for user query: {query}",
    expected_output="A personalized nutrition plan with dietary recommendations",
    agent=nutritionist,
    async_execution=False
)

exercise_planning = Task(
    description="Create an exercise plan based on the blood report at {file_path} for user query: {query}",
    expected_output="A safe exercise program with intensity guidelines",
    agent=exercise_specialist,
    async_execution=False
)