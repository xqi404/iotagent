import os
import subprocess

def cmd(command: str, cwd: str = "", timeout: int = 30) -> dict:
    """
    执行 shell 命令工具

    Args:
        command: shell 命令字符串
        timeout: 超时时间（秒）

    Returns:
        dict: 执行结果
    """

    cwd = cwd or os.getcwd()
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        cwd=cwd,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return {"output": result.stdout, "returncode": result.returncode}
