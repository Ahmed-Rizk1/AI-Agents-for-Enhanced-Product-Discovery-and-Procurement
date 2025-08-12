from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from google.colab import userdata
from pydantic import BaseModel, Field
from typing import List
from tavily import TavilyClient
from scrapegraph_py import Client

import os
import json




os.environ["OPENAI_API_KEY"] = os.get('openai-colab')
os.environ["AGENTOPS_API_KEY"] = userdata.get('agentops-colab')

agentops.init(
    api_key=userdata.get('agentops-colab'),
    skip_auto_end_session=True,
)

class Basic:
    basic_llm = LLM(model='gpt-4o', temperature=0.0)

    output_dir = './ai_agent_output'
    os.makedirs(output_dir, exist_ok=True)

