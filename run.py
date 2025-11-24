import uvicorn

if __name__ == "__main__":
    # Reload=True permite ver cambios en vivo si editas código
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)