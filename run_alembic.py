import subprocess

res = subprocess.run(['venv/Scripts/alembic', 'upgrade', 'head'], capture_output=True, text=True)
with open('alembic_error.txt', 'w') as f:
    f.write(res.stdout)
    f.write("\n---\n")
    f.write(res.stderr)
