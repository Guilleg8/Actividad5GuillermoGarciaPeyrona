import uvicorn
import sys
import asyncio

# --- FIX CRÍTICO PARA WINDOWS ---
if sys.platform == "win32":
    # Esto evita conflictos con el bucle de eventos
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# --------------------------------

if __name__ == "__main__":
    # run.py
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)