import threading
import uvicorn
import webview
from fastapi import FastAPI, Request, Form, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
# This tells FastAPI to serve anything in /static at the URL path /static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Add this route to your FastAPI app
@app.post("/list-datastores")
async def list_datastores(request: Request):
    body = await request.json()
    u_id = body.get("universe_id")
    key = body.get("api_key")

    # Roblox Cloud v2 API for listing DataStores
    url = f"https://apis.roblox.com/cloud/v2/universes/{u_id}/data-stores"
    r = requests.get(url, headers={"x-api-key": key})

    if r.status_code == 200:
        # Returns a list of DataStore objects
        print(r)
        return r.json().get('dataStores', [])
    return {"error": r.text, "status": r.status_code}


@app.post("/list-entries")
async def list_entries(request: Request):
    body = await request.json()
    u_id = body.get("universe_id")
    ds_name = body.get("datastore_name")
    key = body.get("api_key")

    url = f"https://apis.roblox.com/cloud/v2/universes/{u_id}/data-stores/{ds_name}/scopes/global/entries"
    r = requests.get(url, headers={"x-api-key": key})

    if r.status_code == 200:
        return r.json().get('dataStoreEntries', [])
    return {"error": r.text, "status": r.status_code}


@app.post("/get-entry")
async def get_entry(request: Request):
    body = await request.json()
    url = f"https://apis.roblox.com/cloud/v2/universes/{body['universe_id']}/data-stores/{body['datastore_name']}/entries/{body['key_id']}"
    r = requests.get(url, headers={"x-api-key": body['api_key']})
    return r.json().get('value', {})


@app.post("/create-entry")
async def create_entry(request: Request):
    body = await request.json()
    u_id = body['universe_id']
    ds_name = body['datastore_name']
    key_id = body['key_id']

    # URL for creating: POST to /entries?id={key_id}
    url = f"https://apis.roblox.com/cloud/v2/universes/{u_id}/data-stores/{ds_name}/scopes/global/entries"

    params = {"id": key_id}
    headers = {"x-api-key": body['api_key']}
    payload = {"value": body['data']}

    r = requests.post(url, headers=headers, params=params, json=payload)

    # 200 OK or 201 Created are both success
    return {"success": r.status_code in [200, 201], "error": r.text if r.status_code not in [200, 201] else None}

@app.post("/save-entry")
async def save_entry(request: Request):
    body = await request.json()
    url = f"https://apis.roblox.com/cloud/v2/universes/{body['universe_id']}/data-stores/{body['datastore_name']}/entries/{body['key_id']}"
    r = requests.patch(url, headers={"x-api-key": body['api_key']}, json={"value": body['data']})
    return {"success": r.status_code == 200}


@app.post("/delete-entry")
async def delete_entry(request: Request):
    body = await request.json()
    # Construct the Cloud v2 URL for the specific entry
    url = f"https://apis.roblox.com/cloud/v2/universes/{body['universe_id']}/data-stores/{body['datastore_name']}/entries/{body['key_id']}"

    r = requests.delete(url, headers={"x-api-key": body['api_key']})

    # 204 No Content is the standard success code for DELETE in Cloud v2
    return {"success": r.status_code in [200, 204]}

if __name__ == "__main__":
    # 1. Start FastAPI in a background thread
    t = threading.Thread(target=run_fastapi, daemon=True)
    t.start()

    # 2. Create a dedicated window pointing to your FastAPI server
    webview.create_window("Roblox Datastore Navigator", "http://127.0.0.1:8000")

    # 3. Start the GUI loop
    webview.start()