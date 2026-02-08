from pathlib import Path

WORKSPACE = Path("./workspace").resolve()

def read_file(
    path: str,
    max_chars: int = 4000
) -> str:
    """
    读取文件工具

    Args:
        path: 文件路径
        max_chars: 最大内容

    Returns:
        content: 文件内容
    """
    file_path = (WORKSPACE / path).resolve()

    # 安全检查：防止路径逃逸
    if not file_path.is_file() or WORKSPACE not in file_path.parents:
        return f"[ERROR] File not found or access denied: {path}"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)

        if len(content) == max_chars:
            content += "\n...[TRUNCATED]"

        return content
    except Exception as e:
        return f"[ERROR] Failed to read file: {e}"

if __name__ == '__main__':
    print(Path("./workspace").resolve())
