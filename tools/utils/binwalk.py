import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List
from tools.base import Tool, ToolParameter


class BinwalkExtractTool(Tool):
    """
    使用 binwalk 提取固件文件系统的最小工具
    """

    def __init__(self, workspace : str = Path("./workspace").resolve()):
        super().__init__(
            name="binwalk_extract",
            description="使用 binwalk 提取固件文件系统，并返回文件系统目录"
        )

        self.workspace = Path("./").resolve()
        self.tmp_dir = self.workspace / "workspace" / "tmp"
        self.fs_root = self.workspace / "workspace" / "filesystem"

        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.fs_root.mkdir(parents=True, exist_ok=True)

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="firmware_path",
                type="string",
                description="固件文件路径（相对或绝对路径）",
                required=True
            )
        ]

    def run(self, parameters: Dict[str, Any]) -> str:
        if "firmware_path" not in parameters:
            raise ValueError("parameter 'firmware_path' is required")

        firmware_path = self._normalize_path(parameters["firmware_path"])

        if not firmware_path.exists():
            raise FileNotFoundError(f"firmware not found: {firmware_path}")

        # 确保 tmp 存在（不清空）
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

        # binwalk 默认输出目录
        extract_dir = self.tmp_dir / f"_{firmware_path.name}.extracted"

        # 如果之前解包过，可以直接复用（可选）
        if not extract_dir.exists():
            cmd = ["binwalk", "-e", "-M", str(firmware_path)]
            result = subprocess.run(
                cmd,
                cwd=str(self.tmp_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"binwalk failed:\n{result.stderr}")

        if not extract_dir.exists():
            raise RuntimeError("binwalk finished but no extracted directory found")

        # 查找文件系统目录
        fs_dir = self._find_filesystem_dir(extract_dir)
        if fs_dir is None:
            raise RuntimeError("no filesystem directory found")

        # 复制到 workspace/filesystem
        target_dir = self.fs_root / firmware_path.stem
        if target_dir.exists():
            shutil.rmtree(target_dir)

        shutil.copytree(fs_dir, target_dir, symlinks=True)

        return str(target_dir)


    # ------------------------
    # internal helpers
    # ------------------------

    def _normalize_path(self, path: str) -> Path:
        p = Path(path)
        if p.is_absolute():
            return p.resolve()
        return (self.workspace / p).resolve()

    def _remove_empty_dirs(self, root: Path):
        for d in sorted(root.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()

    def _find_filesystem_dir(self, extract_root: Path) -> Path | None:
        """
        在 extracted 目录中查找文件系统根目录
        判定标准：包含 bin/、etc/、sbin 中任意一个
        """
        for d in extract_root.rglob("*"):
            if not d.is_dir():
                continue

            if any((d / x).is_dir() for x in ("bin", "etc", "sbin")):
                return d

        return None

