import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
from pathlib import Path
from tools.registry import ToolRegistry
from tools.utils.cmd import cmd
from tools.utils.file import read_file
from tools.utils.binwalk import BinwalkExtractTool
from core.llm import HelloAgentsLLM
from agents.ReActAgent import ReActAgent
# 加载 .env 文件中的环境变量
load_dotenv()

if __name__ == '__main__':
    llm = HelloAgentsLLM()
    tool_executor = ToolRegistry()
    binwalk = BinwalkExtractTool(workspace=Path("./workspace").resolve())
    cmd_desc = "一个命令执行工具。当你需要执行命令行命令，应使用此工具。"
    #read_desc = "一个读取文件的工具，当你要读取文件时，首先尝试用这个工具"
    tool_executor.register_function("Cmd", cmd_desc, cmd)
    #tool_executor.register_function("Read", read_desc, read_file)
    tool_executor.register_tool(binwalk)
    agent = ReActAgent(name="test", llm=llm, tool_registry=tool_executor)
    question = "分析workspace/firmware文件夹下的固件漏洞"
    agent.run(question)
