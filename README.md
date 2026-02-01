# Roblox Datastore Navigator

Roblox Datastore Navigator is a lightweight desktop application designed to help developers browse, edit, and manage their Roblox DataStores using the Roblox Cloud v2 API. Built with FastAPI and pywebview, it provides a clean and intuitive interface for interacting with your game's data.

## Features

- **DataStore Discovery**: Easily list and switch between all available DataStores in your Roblox Universe.
- **Entry Management**: Browse all entries (keys) within a selected DataStore.
- **Search & Filter**: Quickly find specific keys with real-time filtering.
- **JSON Editor**: View and edit DataStore entry values directly in a formatted JSON editor.
- **CRUD Operations**:
  - **Create**: Add new entries with initial data.
  - **Read**: Fetch and display entry values.
  - **Update**: Save changes back to the Roblox Cloud.
  - **Delete**: Remove unwanted entries with a confirmation safety check.

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Frontend**: HTML5, [Tailwind CSS](https://tailwindcss.com/)
- **GUI Layer**: [pywebview](https://pywebview.flowrl.com/)
- **API Communication**: [Requests](https://requests.readthedocs.io/)

## Prerequisites

- **Python 3.x**: Ensure you have Python installed on your system.
- **Roblox Cloud Credentials**:
  - **Universe ID**: The ID of your Roblox game universe.
  - **API Key**: A valid Roblox Cloud API Key with permissions for `DataStore` (at least `Entry List`, `Entry Read`, `Entry Write`, and `DataStore List`).

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd RobloxDatastoreNavigator
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn pywebview requests jinja2
   ```

## Usage

Run the application using Python:

```bash
python app.py
```

Once the window opens:
1. Enter your **Universe ID** and **API Key**.
2. Click **Connect & List** to see your DataStores.
3. Select a DataStore from the dropdown.
4. Browse or search for keys in the left sidebar.
5. Edit the JSON data and click **Save to Cloud** to update, or use the **+** button to create a new entry.
