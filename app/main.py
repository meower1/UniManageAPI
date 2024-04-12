"""
Startup command for Local enviroment
"""

import uvicorn
from config import app  # pylint: disable=unused-import


if __name__ == "__main__":
    uvicorn.run("config:app", host="127.0.0.1", port=8000, reload=True)
