from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_maker_ai_agent.models.response_models import MusicDetails
from resume_maker_ai_agent.tools.custom_tool import search_tool


@CrewBase
class JioSavanMusicDownloaderAgent:
    """JioSavanMusicDownloaderAgent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def music_researcher(self) -> Agent:
        """
        Creates a music researcher agent.

        This agent is responsible for searching for the specified music on JioSaavn
        and returning the results in a structured format.

        :return: An instance of the Agent class
        """
        return Agent(config=self.agents_config["music_researcher"], verbose=True)

    @task
    def music_research_task(self) -> Task:
        """
        Creates the music research task.

        This task is responsible for searching for the specified music on JioSaavn
        and returning the results in a structured format.

        :return: An instance of the Task class
        """

        return Task(
            config=self.tasks_config["music_research_task"],
            tools=[search_tool],
            output_json=MusicDetails,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JioSavanMusicDownloaderAgent crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
