import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
from tools.ToolExecutor import ToolExecutor
from tools.search import search
from tools.cmd import cmd
from models.HelloAgentLLM import HelloAgentsLLM
from agents.ReActAgent import ReActAgent
# 加载 .env 文件中的环境变量
load_dotenv()

if __name__ == '__main__':
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    cmd_desc = "一个命令执行工具。当你需要执行命令行命令，应使用此工具。"
    tool_executor.registerTool("Search", search_desc, search)
    tool_executor.registerTool("Cmd", cmd_desc, cmd)
    agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
    question = "windows环境下，解决当前文件夹下test文件夹中question.md文件里的问题，答案写在test文件夹里的result.md文件"
    agent.run(question)
