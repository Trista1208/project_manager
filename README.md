# MCP Task Agent (GitHub → Tasks → Calendar)

This agent:

1. Reads issues from a GitHub repo  
2. Breaks them into smaller tasks (using Gemini + Jinja)  
3. Estimates dependencies + durations  
4. Schedules them into your **Google Calendar** (08–12, 14–17, no overlaps, max 5 tasks)

---

## 1. Clone + environment

```bash
git clone https://github.com/Meupi/Devops_and_LLMs.git
cd Devops_and_LLMs

conda env create -f environment.yml
conda activate agent-env
```

---

## 2. .env (API keys)

Create a file `.env` in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

- `GOOGLE_API_KEY`: Gemini 2.5 Flash API key  
- `GITHUB_TOKEN`: GitHub personal access token with `repo` scope

---

## 3. Google Calendar setup (each dev uses their own account)

Each developer does this once:

1. Go to **Google Cloud Console**  
2. Create or select a project  
3. Enable **Google Calendar API**  
4. Go to **APIs & Services → Credentials**  
   - Create **OAuth client ID → Desktop app**  
   - Download the `credentials.json`
5. Put **your** `credentials.json` into the project root  
6. Make sure there is **no** `token.json` yet  
7. Run:

   ```bash
   conda activate agent-env
   python src/tests/test_calendar_direct.py
   ```

8. A browser opens → log into **your** Google account  
   - This creates **your personal** `token.json`  
   - From now on, events go to **your calendar**

> `credentials.json` and `token.json` are git-ignored and stay local.

---

## 4. Start MCP server

Terminal 1:

```bash
conda activate agent-env
python src/tools/mcp_server.py
```

MCP server runs on `http://127.0.0.1:5000/mcp`.

---

## 5. Run the agent

Terminal 2:

```bash
conda activate agent-env
python src/core/run_agent.py
```

The agent will:

- Fetch issues from the configured GitHub repo  
- Use Gemini to break them into tasks with dependencies + durations  
- Schedule tasks in **08:00–12:00 and 14:00–17:00**, no overlaps, max 5 tasks  
- Create the corresponding events in **your Google Calendar**
