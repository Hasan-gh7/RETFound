FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend /app/backend
COPY frontend /app/frontend
COPY run_demo.py /app/run_demo.py
EXPOSE 8001
ENV EYE_AI_HOST=0.0.0.0 EYE_AI_PORT=8001 EYE_AI_NO_BROWSER=1
CMD ["python", "run_demo.py"]
