
---
## Local Setup

1) Install <a href="https://nodejs.org/en/download/" target="_blank">npm</a>

```bash
npm install -g npm
```

2) Install npx

```bash
npm install -g npx
```

3) Install IDOM

```bash
pip install "idom[stable]"
```

4) Install Tailwind CSS
```bash
npm install -D tailwindcss postcss postcss-cli autoprefixer
npx tailwindcss init
```

5) Install FastAPI

```bash
pip install FastAPI
```

6) Spin up the backend Fastapi dev server

```bash
cd timesheets
uvicorn backend.main:app --reload
```

7) Spin up the frontend IDOM dev server
```bash
cd timesheets/idom_frontend
python3 -m run_reload.py
```
8) Compile the tailwind css file

```bash
cd idom_frontend/tailwind
npm run build
```


## Docker Setup

1) Open a git bash terminal

2) Ensure you are in the root directory of the project

3) Navigate to `frontend/tailwind` and run `npm run build`

```bash
cd frontend/tailwind
npm run build
```

4) Run sh build.sh in home directory
```bash
cd ../..
sh build.sh
```

5) Run docker-compose up
```bash
docker-compose up
```
*If you don't wish to look at the docker logs, run the command `docker-compose up` with the flag `-d` instead of `docker-compose up`*
```bash
docker-compose up -d
```

## Navigating to the application

By default, both the [Local Setup](/timeflow/how-tos/#local-setup) and the [Docker Setup](/timeflow/how-tos/#docker-setup) host the application at `127.0.0.1:8001/client/index.html`.

Thus in order to view the running application, open your favorite web browser, eg. Chrome, FireFox, etc., and enter `127.0.0.1:8001/client/index.html` into the search bar.

<a href="http://127.0.0.1:8001/client/index.html" target="_blank">http://127.0.0.1:8001/client/index.html</a>

## Working on the documentation

Timeflow's documentation has been built with <a href="https://www.mkdocs.org/" target="_blank">MkDocs</a>

The easiest way to update these docs is to host them locally, and write the updates necessary. MkDocs auto-reloads everytime you save changes to a file which allows for quick building and visualization.

```bash
mkdocs serve
```

*If you are having trouble with this step, it may be due to mkdocs auto-loading on port 8000. You may have an app already running on port 8000. If that is the case, enter the following code instead.*

```bash
mkdocs serve -a 127.0.0.1:8003
```

**Note:** *You can substitute port 8003 with any other port that is not currently in use on your system.*