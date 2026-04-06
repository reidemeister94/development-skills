# Setting Up GitHub Actions CI/CD Pipeline

It's important to note that GitHub Actions provides a powerful way to automate your CI/CD workflow. Let me break this down for you.

Furthermore, here is the complete workflow configuration:

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v4

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:${{ github.sha }} .
      - run: docker push registry.example.com/myapp:${{ github.sha }}
      - run: kubectl set image deployment/myapp myapp=registry.example.com/myapp:${{ github.sha }}
```

It's worth mentioning that the `test` job runs on every push and PR. Moreover, the `deploy` job only runs on `main` branch pushes, due to the fact that the `if` condition filters for `refs/heads/main`.

Additionally, it should be noted that the PostgreSQL service container is available at `localhost:5432` with password `test`. In order to connect from your test code, use:

```python
DATABASE_URL = "postgresql://postgres:test@localhost:5432/postgres"
```

In conclusion, this pipeline provides comprehensive CI/CD automation for testing and deployment.
