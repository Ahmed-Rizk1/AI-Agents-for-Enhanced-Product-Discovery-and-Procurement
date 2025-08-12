# AI Agent for Product Search and Scraping

This project demonstrates the use of an AI agent built with the CrewAI framework to perform automated product searches and web scraping. It leverages several tools to accomplish its tasks, including `Tavily` for general web searches and `Scrapegraph` for targeted web scraping.

## Features

-   **Search Queries Recommendation Agent**: An agent designed to generate specific and varied search queries for products.
-   **Tavily Integration**: Utilizes the Tavily search engine for broad information retrieval.
-   **Scrapegraph Integration**: Employs Scrapegraph to intelligently extract structured data from specific product web pages.
-   **CrewAI Framework**: Built on the CrewAI library to orchestrate multiple agents and tasks.

## Getting Started

### Prerequisites

You will need to have Python installed. It is recommended to use a virtual environment.

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your_username/your_project_name.git](https://github.com/your_username/your_project_name.git)
    cd your_project_name
    ```

2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The project requires API keys for `Tavily` and `Scrapegraph`. You will also need an API key for `OpenAI` as the notebook uses the `gpt-4o` model.

It's recommended to set these as environment variables or use a secret management system like `userdata.get()` in a Colab environment.

```python
import os
from google.colab import userdata

os.environ["OPENAI_API_KEY"] = userdata.get('openai-colab')
# os.environ["AGENTOPS_API_KEY"] = userdata.get('agentops-colab')
# os.environ["TAVILY_API_KEY"] = userdata.get('tavily-colab')
# os.environ["SCRAPEGRAPH_API_KEY"] = userdata.get('scrapegraphe-colab')