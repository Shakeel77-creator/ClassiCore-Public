FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app

# ✅ Copy requirements first to ensure change triggers re-install
COPY backend/requirements.txt ./backend/requirements.txt

# ✅ Install Python + pip + dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r backend/requirements.txt

# ✅ Now copy the rest of the app
COPY . .

# ✅ Set PYTHONPATH
ENV PYTHONPATH=/app

# ✅ Start the app
CMD ["uvicorn", "backend.fastapi_app:app", "--host", "0.0.0.0", "--port", "5000"]
