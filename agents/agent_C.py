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
from scrapegraph_py import Client


import os
import json



class AGENT_C(Basic):


    class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str

    class SingleExtractedProduct(BaseModel):
        page_url: str = Field(..., title="The original url of the product page")
        product_title: str = Field(..., title="The title of the product")
        product_image_url: str = Field(..., title="The url of the product image")
        product_url: str = Field(..., title="The url of the product")
        product_current_price: float = Field(..., title="The current price of the product")
        product_original_price: float = Field(title="The original price of the product before discount. Set to None if no discount", default=None)
        product_discount_percentage: float = Field(title="The discount percentage of the product. Set to None if no discount", default=None)

        product_specs: List[ProductSpec] = Field(..., title="The specifications of the product. Focus on the most important specs to compare.", min_items=1, max_items=5)

        agent_recommendation_rank: int = Field(..., title="The rank of the product to be considered in the final procurement report. (out of 5, Higher is Better) in the recommendation list ordering from the best to the worst")
        agent_recommendation_notes: List[str]  = Field(..., title="A set of notes why would you recommend or not recommend this product to the company, compared to other products.")


    class AllExtractedProducts(BaseModel):
        products: List[SingleExtractedProduct]



    scraper_client = Client(api_key=userdata.get('scrapegraphe-colab'))
    @tool
    def web_scraping_tool(page_url: str):
        """
        An AI Tool to help an agent to scrape a web page

        Example:
        web_scraping_tool(
            page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
        )
        """
        details = scraper_client.smartscraper(
            website_url=page_url,
            user_prompt="Extract ```json\n" + SingleExtractedProduct.schema_json() + "```\n From the web page"
        )

        return {
            "page_url": page_url,
            "details": details
        }

    scraping_agent = Agent(
        role="Web scraping agent",
        goal="To extract details from any website",
        backstory="The agent is designed to help in looking for required values from any website url. These details will be used to decide which best product to buy.",
        llm=basic_llm,
        tools=[web_scraping_tool],
        verbose=True,
    )

    scraping_task = Task(
        description="\n".join([
            "The task is to extract product details from any ecommerce store page url.",
            "The task has to collect results from multiple pages urls.",
            "Collect the best {top_recommendations_no} products from the search results.",
        ]),
        expected_output="A JSON object containing products details",
        output_json=AllExtractedProducts,
        output_file=os.path.join(output_dir, "step_3_search_results.json"),
        agent=scraping_agent
    )