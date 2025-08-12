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
from .agent_A import AGNET_A
from .agent_B import AGNET_B
from .agent_C import AGNET_C
from .agent_D import AGNET_D


import os
import json


rankyx_crew = Crew(
    agents=[AGNET_A.search_quieries_agent, 
            AGNET_B.search_engine_agent,
            AGNET_C.scraping_agent,
            AGNET_D.procurement_report_author_agent
            ],
    

    tasks=[AGNET_A.search_quieries_task, 
           AGNET_B.search_engine_task,
           AGNET_C.scraping_task,
           AGNET_D.procurement_report_author_task
           ],
    process = Process.sequential
)


crew_results = rankyx_crew.kickoff(
    inputs={
        "product_name": "coffee machine for the office",
        "websites_list": ["www.amazon.eg", "www.jumia.com.eg", "www.noon.com/egypt-en"],
        "country_name": "Egypt",
        "no_keywords": 10,
        "language": "english",
        "score_th": 0.3,
        "top_recommendations_no": 10

    }
)