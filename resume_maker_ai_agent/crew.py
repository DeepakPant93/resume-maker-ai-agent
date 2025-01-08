from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_maker_ai_agent.models.response_models import MusicDetails
from resume_maker_ai_agent.tools.custom_tool import search_tool
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


@CrewBase
class ResumeMakerAIAgent:
    """ResumeMakerAIAgent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def job_researcher(self) -> Agent:
        """
        Creates the job researcher agent.

        This agent is responsible for searching for job openings.

        :return: An instance of the Agent class
        """

        return Agent(config=self.agents_config["job_researcher"],
                     tools=[search_tool],
                     verbose=True)

    @agent
    def profiler(self) -> Agent:
        """
        Creates the profiler agent.

        This agent is responsible for researching and generating music details.

        :return: An instance of the Agent class
        """

        return Agent(config=self.agents_config["profiler"],
                     tools=[search_tool],
                     verbose=True)

    @agent
    def resume_strategist(self) -> Agent:
        """
        Creates the resume strategist agent.

        This agent is responsible for customizing resumes based on job
        descriptions.

        :return: An instance of the Agent class
        """

        return Agent(config=self.agents_config["resume_strategist"],
                     tools=[search_tool],
                     verbose=True)

    @task
    def research_task(self) -> Task:
        """
        Creates the research task.

        This task is responsible for searching for job openings.

        :return: An instance of the Task class
        """

        return Task(
            config=self.tasks_config["research_task"],
            async_execution=True
        )

    @task
    def profile_task(self) -> Task:
        """
        Creates the profile task.

        This task is responsible for researching and generating music details.

        :return: An instance of the Task class
        """

        return Task(
            config=self.tasks_config["profile_task"],
            async_execution=True
        )

    @task
    def profile_task(self) -> Task:
        """
        Creates the profile task.

        This task is responsible for generating a profile based on the output
        of the research task.

        :return: An instance of the Task class
        """

        return Task(
            config=self.tasks_config["profile_task"],
            context=[research_task, profile_task],
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
