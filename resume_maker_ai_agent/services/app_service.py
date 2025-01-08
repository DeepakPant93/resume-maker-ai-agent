import warnings

from resume_maker_ai_agent.crew import JioSavanMusicDownloaderAgent
from resume_maker_ai_agent.services.web_scarapper_service import scrape_pages

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def search_music(query: str) -> list[dict]:
    music_details = []
    try:
        # Search the internet for music
        print(f"Searching for music: {query}")
        search_results = search_internet(query)
        print(f"Found {len(search_results)} results")

        # Get music details
        print("Getting music details")
        music_details = get_music_details(search_results)
        print(f"Got details for {len(music_details)} songs")
        print(f"Music details: {music_details}")
        print("Done")
    except Exception as e:
        print(f"An error occurred: {e!s}")

    return music_details


def search_internet(query: str) -> list[dict]:
    # Run the crew
    inputs = {"website": "https://www.jiosaavn.com", "topic": query}
    result = JioSavanMusicDownloaderAgent().crew().kickoff(inputs=inputs)
    links = result.to_dict().get("links", [])
    return links if isinstance(links, list) else []


def get_music_details(songs: list[dict]) -> list[dict]:
    # Get music details by scrapping the pages

    links: list[str] = [album["link"] for album in songs]
    return scrape_pages(links)
