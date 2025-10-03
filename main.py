from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import logging

app = FastAPI()

# Enable CORS for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging agent runs
logging.basicConfig(filename="agent_runs.log", level=logging.INFO)

@app.get("/task")
def run_task(q: str = Query(..., description="Task description")):
    try:
        # Run Aider CLI with the task query
        result = subprocess.run(
            ["aider", "run", q],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        output = str(e)

    logging.info(f"TASK: {q} | OUTPUT: {output}")

    return {
        "task": q,
        "agent": "aider",
        "output": output,
        "email": "23f3004431@ds.study.iitm.ac.in"
    }
