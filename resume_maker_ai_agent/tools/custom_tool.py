from crewai_tools import FileWriterTool, ScrapeWebsiteTool, SerperDevTool

jio_savan_scapper_tool = ScrapeWebsiteTool(website_url="https://www.jiosaavn.com")
file_writer_tool = FileWriterTool()
search_tool = SerperDevTool(
    country="in",  # Set to 'in' for India
    locale="en",  # Set locale to English
    n_results=5,  # You can adjust the number of results as needed
)
