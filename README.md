# Local Setup instructions

1) Install [npm](https://nodejs.org/en/download/)

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

# Docker instructions

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