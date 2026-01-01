FROM python:3.9-slim

WORKDIR /app/browser
RUN apt update && \
  apt install -y tk \
  fontconfig \
  fonts-liberation \
  fonts-dejavu-core \
  fonts-freefont-ttf \
  fonts-ipafont  \
  fonts-noto-cjk \
  fonts-noto-color-emoji \
  fonts-takao \
  build-essential \
  libgl1 \
  libgl1-mesa-dri \
  libglx-mesa0 \
  mesa-utils
# フォント設定をコピー
COPY docker/local.conf /etc/fonts/local.conf
RUN fc-cache -fv

ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --frozen --no-dev

ENTRYPOINT ["uv", "run", "main.py"]
