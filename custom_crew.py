from langchain_community.llms import Ollama
import traceback


class CustomCrew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.llm = Ollama(model="llama3", base_url="http://localhost:11434")

    def kickoff(self, inputs):
        results = {}
        try:
            for task in self.tasks:
                agent = next((a for a in self.agents if a.role == task.agent.role), None)
                if not agent:
                    continue

                # Prepare the prompt
                prompt = (
                    f"ROLE: {agent.role}\n"
                    f"GOAL: {agent.goal.format(**inputs)}\n"
                    f"BACKSTORY: {agent.backstory}\n"
                    f"TASK: {task.description.format(**inputs)}\n"
                    f"EXPECTED OUTPUT: {task.expected_output}\n"
                    "RESPONSE:\n"
                )

                # Execute tool if needed
                if agent.tools:
                    tool_output = agent.tools[0]._run(inputs['file_path'])
                    prompt += f"REPORT CONTENT:\n{tool_output}\n\n"

                # Get response
                response = self.llm.invoke(prompt)
                results[agent.role] = response

        except Exception as e:
            traceback.print_exc()
            return f"Crew execution failed: {str(e)}"

        return "\n\n".join([f"## {agent}\n{response}" for agent, response in results.items()])