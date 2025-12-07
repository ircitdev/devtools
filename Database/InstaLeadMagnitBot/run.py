"""Entry point for InstaLeadMagnitBot."""

import asyncio
import sys
from pathlib import Path

# Add project root to path so 'src' package can be found
sys.path.insert(0, str(Path(__file__).parent))

from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
