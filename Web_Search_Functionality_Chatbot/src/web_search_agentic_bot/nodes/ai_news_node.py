from langchain_tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNodes:

    def __init__(self, model):
        self.tavily = TavilyClient()
        self.model = model
        self.state = {} #used to capture various steps in this file which will be used later

    def fetch_ai_news(self, state:dict)->dict:

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {"Daily":"d", "Weekly":"w", "Monthly": "m"}

        response = self.tavily.search(
            query="Top Artificial Intelligence News from India and Globally",
            max_results=3,
            topic="news",
            time_range=time_range_map[frequency]
        )

        state['news_data'] = response.get("results", [])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news_node(self, state:dict)->dict:

        news_items = self.state['news_data']

        summarize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", '''Summarize AI news articles into markdown format. For each item include:
                 - Date in **YYYY-MM-DD** format in IST TimeZone
                 - Concise sentences summary from latest news
                 - Sort news by date (latest first)
                 - Source URL as link
                 Use format:
                 ### [Date]
                 - [Summary](URL)'''),
                 ("user", "Articles:\n{articles}")
            ]
        )

        articles_str = "\n\n".join([
            f"Content: {item.get("content", " ")}\n URL: {item.get("url", " ")}\n Date: {item.get("published_date", " ")}"
        for item in news_items])

        summarized_content = self.model.invoke(summarize_prompt.format({"articles":articles_str}))

        state['summary'] = summarized_content.content
        self.state['summary'] = state['summary']

        return state
    
    def save_results(self, state:dict)->dict:
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AI_News/{frequency}_summary.md"
        with open(filename, "w") as f:
            f.write(f"#{frequency.captialize()}_AI_News_Summary")
            f.write(summary)
        self.state['filename'] = filename
        state['filename'] = self.state['filename']
        return state    

