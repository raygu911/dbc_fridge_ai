# Session 1 Validation Guide

Use this guide during the Session 1 lecture to demonstrate how the terminal, Streamlit, FastAPI, PostgreSQL, FastEmbed, and Qdrant work together.

## Learning Objectives

Trainees will learn to:

- Start and inspect the complete Session 1 environment.
- Create, browse, and search for recipes through Streamlit.
- Test the same operations directly through FastAPI.
- Explain the different responsibilities of PostgreSQL and Qdrant.
- Inspect service health, structured records, vectors, and logs.
- Run automated quality checks.

## Architecture

```text
User → Streamlit → FastAPI
                    ├── PostgreSQL
                    └── FastEmbed → Qdrant
```

- **Streamlit** is the user-facing application.
- **FastAPI** validates requests and coordinates operations.
- **PostgreSQL** is the source of truth for complete recipes.
- **FastEmbed** converts recipe content and queries into vectors.
- **Qdrant** stores vectors and returns semantically similar recipe IDs.

## 1. Start the Environment

From the repository root:

```bash
cd base/session-1-application-and-search
cp .env.example .env
docker compose up --build -d
docker compose ps
```

Wait for `database`, `qdrant`, `api`, and `web` to be running or healthy.

Verify the API:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "fridge-ai-api",
  "environment": "development"
}
```

Open:

- Streamlit: <http://localhost:8501>
- FastAPI documentation: <http://localhost:8000/docs>
- Qdrant dashboard: <http://localhost:6333/dashboard>

## 2. Create Recipes in Streamlit

Open Streamlit and confirm that the sidebar displays **API connected**. Select **Add a recipe**.

### Quick Vegetable Fried Rice

| Field | Value |
| --- | --- |
| Recipe name | Quick Vegetable Fried Rice |
| Description | A fast meal using leftover rice and vegetables. |
| Cooking time | 15 |
| Dietary tags | vegetarian, quick |

Enter one ingredient per line:

```text
cooked rice
carrot
peas
soy sauce
sesame oil
```

Enter one instruction per line:

```text
Heat the sesame oil
Cook the carrot and peas
Add the rice and soy sauce
Stir until hot
```

Click **Add recipe** and confirm the success message.

### Creamy Tomato Pasta

| Field | Value |
| --- | --- |
| Recipe name | Creamy Tomato Pasta |
| Description | A comforting pasta dish with tomato and cream. |
| Cooking time | 25 |
| Dietary tags | vegetarian, comfort food |

Ingredients:

```text
pasta
tomato sauce
cream
garlic
parmesan
```

Instructions:

```text
Boil the pasta
Cook the garlic and tomato sauce
Add the cream
Combine with the pasta
```

Add the second recipe.

### Teaching Point

Creating a recipe performs two related operations:

```text
Structured recipe record → PostgreSQL
Recipe embedding         → Qdrant
```

PostgreSQL remains authoritative. Qdrant supports semantic retrieval and links to recipes by ID.

## 3. Browse and Search in Streamlit

### Browse

1. Select **Browse recipes**.
2. Click **Load recipes**.
3. Confirm that both recipes appear.
4. Expand them and inspect their fields.

This proves that Streamlit retrieves structured records through FastAPI and PostgreSQL.

### Semantic Search

Select **Semantic search** and submit:

```text
a fast meal using leftover grains
```

The fried-rice recipe should rank highly without an exact recipe-name match.

Try:

```text
comforting Italian food with a creamy sauce
```

The tomato-pasta recipe should rank highly. The first search may be slower while FastEmbed downloads and initializes its model.

## 4. Test FastAPI

Open <http://localhost:8000/docs>.

### List Recipes

1. Expand `GET /api/v1/recipes`.
2. Click **Try it out**, then **Execute**.
3. Confirm HTTP `200` and both recipes in the response.

### Retrieve One Recipe

1. Note a recipe `id` from the list response.
2. Expand `GET /api/v1/recipes/{recipe_id}`.
3. Enter the ID and execute the request.
4. Confirm HTTP `200` and the correct recipe.

### Run Semantic Search

1. Expand `GET /api/v1/recipes/search`.
2. Enter `quick dinner made from rice` for `query`.
3. Enter `5` for `limit`.
4. Execute the request.

The response should contain the recipe and a similarity score. Exact IDs and scores may differ:

```json
[
  {
    "recipe": {
      "id": 1,
      "name": "Quick Vegetable Fried Rice"
    },
    "score": 0.8
  }
]
```

### Test Validation

Expand `POST /api/v1/recipes` and submit:

```json
{
  "name": "Invalid Recipe",
  "description": "",
  "ingredients": [],
  "instructions": [],
  "cooking_time_minutes": 10,
  "dietary_tags": []
}
```

The API should return HTTP `422`, demonstrating FastAPI and Pydantic validation.

## 5. Inspect Qdrant

Open <http://localhost:6333/dashboard>.

1. Select **Collections**.
2. Open the `recipes` collection.
3. Inspect its configuration and points.
4. Find point IDs corresponding to PostgreSQL recipe IDs.

If the collection is absent, create a recipe and refresh the dashboard.

Explain the retrieval flow:

```text
Natural-language query
        ↓
FastEmbed creates a query vector
        ↓
Qdrant finds similar recipe IDs
        ↓
FastAPI loads full records from PostgreSQL
        ↓
Streamlit displays ranked recipes
```

## 6. Validate Through the Terminal

List recipes:

```bash
curl -s http://localhost:8000/api/v1/recipes | jq
```

If `jq` is unavailable, omit `-s` and `| jq`.

Run semantic search:

```bash
curl --get http://localhost:8000/api/v1/recipes/search \
  --data-urlencode "query=a quick meal made with leftover grains" \
  --data-urlencode "limit=5"
```

Inspect the Qdrant collection:

```bash
curl http://localhost:6333/collections/recipes
```

Count vector points:

```bash
curl http://localhost:6333/collections/recipes/points/count \
  -H "Content-Type: application/json" \
  -d '{"exact":true}'
```

Inspect PostgreSQL:

```bash
docker compose exec database \
  psql -U fridge_ai -d fridge_ai -c \
  "SELECT id, name, cooking_time_minutes FROM recipes ORDER BY id;"
```

Compare PostgreSQL recipe IDs with Qdrant point IDs.

Show recent logs:

```bash
docker compose logs --tail=100 api web qdrant
```

Follow logs live:

```bash
docker compose logs -f api web
```

Press `Ctrl+C` to stop following logs without stopping the application.

## 7. Run Automated Verification

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -v
docker compose config --quiet
```

Expected result: `8 passed`.

## Completion Checklist

- [ ] All four services are running or healthy.
- [ ] The health endpoint returns HTTP `200`.
- [ ] Streamlit reports that the API is connected.
- [ ] Two recipes can be created and browsed.
- [ ] Semantic queries return meaningfully related recipes.
- [ ] FastAPI lists and retrieves recipes.
- [ ] Invalid input returns HTTP `422`.
- [ ] PostgreSQL contains complete recipe records.
- [ ] Qdrant contains the `recipes` collection and vector points.
- [ ] PostgreSQL recipe IDs correspond to Qdrant point IDs.
- [ ] Ruff and pytest pass.
- [ ] The trainee can explain the complete retrieval flow.

## Shut Down

Preserve the data and stop the environment:

```bash
docker compose down
```

Do not use `docker compose down --volumes` unless you intentionally want to delete PostgreSQL records, Qdrant vectors, and the model cache.

## Troubleshooting

### Streamlit reports that the API is unavailable

```bash
docker compose ps
docker compose logs --tail=100 api web
```

### Semantic search is slow the first time

FastEmbed may be downloading its model. Follow the API logs:

```bash
docker compose logs -f api
```

### The Qdrant collection does not exist

Create a valid recipe, wait for the request to finish, and refresh Qdrant.

### Tests cannot connect to PostgreSQL

```bash
docker compose ps database
docker compose logs --tail=100 database
```
