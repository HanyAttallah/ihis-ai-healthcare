# iHIS Public Educational Demo Deployment

This branch (`deployment/public-demo`) is derived from the frozen academic source at commit `dbe68c20a090e5b192bc82d607dfc57e83925f50` and adds only deployment support for an educational public demo.

## Important scope

- Synthetic educational data only.
- Not clinically validated.
- Not a medical device.
- Do not enter real patient information.
- Do not commit `.env` or any real API key.

## Render deployment

The repository includes `render.yaml` for a Render web-service deployment.

Required secret environment values:

- `IHIS_DEMO_PASSWORD`: create a strong password of at least 12 characters.
- `GROQ_API_KEY`: optional for live Groq generation; if unavailable, the Week 5 module retains its local grounded fallback behavior.

The deployment automatically:

1. installs dependencies;
2. applies database migrations;
3. seeds the standard roles;
4. creates/refreshes a synthetic Administrator demo account;
5. creates a synthetic respiratory demo patient with MRN `IHIS-DEMO-0001`;
6. starts the Flask application with Gunicorn.

The default demo username is `demo`. The password is supplied only through the Render environment and is never stored in the repository.

## Public-demo database behavior

The public demo uses SQLite for simplicity and semester-project demonstration purposes. On an ephemeral hosting tier, demo data may reset when the service is rebuilt or restarted. This is acceptable for the educational demonstration and must not be treated as persistent clinical storage.

## Local deployment-branch check

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
flask --app run.py db upgrade
python -m scripts.seed_roles
$env:IHIS_DEMO_PASSWORD="choose-a-strong-demo-password"
python -m scripts.seed_public_demo
pytest -q
flask --app run.py run --debug
```

Open `http://127.0.0.1:5000` and sign in with username `demo` and the password you set above.
