from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from google.colab import userdata
from pydantic import BaseModel, Field
from typing import List
from tavily import TavilyClient
from scrapegraph_py import Client
from .BasicInfo import Basic 

import os
import json


class AGENT_B(Basic):

    class SignleSearchResult(BaseModel):
        title: str
        url: str = Field(..., title="the page url")
        content: str
        score: float
        search_query: str

    class AllSearchResults(BaseModel):
        results: List[SignleSearchResult]
    
    
    tavily_client = TavilyClient(api_key=userdata.get('tavily-colab'))

    @tool
    def search_engine_tool(query: str):
        """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
        return tavily_client.search(query)

    search_engine_agent = Agent(
        role="Search Engine Agent",
        goal="To search for products based on the suggested search query",
        backstory="The agent is designed to help in looking for products by searching for products based on the suggested search queries.",
        llm=Basic.basic_llm,
        verbose=True,
        tools=[search_engine_tool]
    )

    search_engine_task = Task(
        description="\n".join([
            "The task is to search for products based on the suggested search queries.",
            "You have to collect results from multiple search queries.",
            "Ignore any susbicious links or not an ecommerce single product website link.",
            "Ignore any search results with confidence score less than ({score_th}) .",
            "The search results will be used to compare prices of products from different websites.",
        ]),
        expected_output="A JSON object containing the search results.",
        output_json=AllSearchResults,
        output_file=os.path.join(output_dir, "step_2_search_results.json"),
        agent=search_engine_agent
    )