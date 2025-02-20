from src.main import app
from os import cpu_count
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080,workers=cpu_count()-1)