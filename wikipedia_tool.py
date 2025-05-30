from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import wikipedia

app = FastAPI()

@app.get("/wikipedia")
def get_wikipedia_summary(query: str = Query(..., description="Search term for Wikipedia")):
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return JSONResponse(content={"error": f"No results found for '{query}'"}, status_code=404)

        best_match = search_results[0]
        page = wikipedia.page(best_match)
        return {"summary": page.summary, "title": page.title, "url": page.url}

    except wikipedia.exceptions.DisambiguationError as e:
        return JSONResponse(content={"error": f"Query was ambiguous. Options: {e.options[:5]}"}, status_code=400)

    except wikipedia.exceptions.PageError:
        return JSONResponse(content={"error": f"No Wikipedia page found for '{query}'"}, status_code=404)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
