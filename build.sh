curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
psql -a -d $DATABASE_URL -f database.sql
