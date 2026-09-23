FROM python:3.12-slim

# 避免生成 .pyc、日志实时输出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 先装依赖，充分利用镜像层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY bot.py .

# 非 root 用户运行
RUN useradd --create-home botuser
USER botuser

CMD ["python", "bot.py"]
