from fastapi import FastAPI,HTTPException
from copykitt import generate_branding_snippet, generate_keywords
from typing import List


MAX_LENGTH = 32

app = FastAPI()


@app.get("/generate-snippet")
async def generate_snippet_api(prompt:str):
    validate_input_length(prompt)
    snippet = generate_branding_snippet(prompt)
    return {"snippet": snippet, "keywords": None}

@app.get("/generate-keywords")
async def generate_keywords_api(keyword:str) -> List[str]:
    validate_input_length(keyword)
    keywords = generate_keywords(keyword)
    return {"snippet": None, "keywords": keywords}


@app.get('/generate-snippets-and-keywords')
async def generate_snippets_and_keywords_api(prompt:str):
    validate_input_length(prompt)
    snippet = generate_branding_snippet(prompt)
    keywords = generate_keywords(prompt)
    return {"snippet": snippet, "keywords": keywords}


def validate_input_length(prompt:str):
    if len(prompt) > MAX_LENGTH:
        raise HTTPException(status_code=404, detail="Lengthy string")