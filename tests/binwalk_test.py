from pathlib import Path
import sys
from tools.utils.binwalk import BinwalkExtractTool

if __name__ == '__main__':

    print(sys.path)
    binwalk = BinwalkExtractTool()
    print(binwalk)
    binwalk.run({
    "firmware_path": "/home/xq/MyAgent/workspace/firmware/US_AC15V1.0BR_V15.03.05.19_multi_TD01.bin"
})
    print(Path("workspace/firmware/US_AC15V1.0BR_V15.03.05.19_multi_TD01.bin").resolve())