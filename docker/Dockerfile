FROM mcr.microsoft.com/playwright:v1.41.0-focal
ARG VERSION

RUN mkdir /tests && chown pwuser /tests

USER pwuser

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="$PATH:/home/pwuser/.local/bin"

RUN uv tool install --with pytest-playwright,tursu==$VERSION pytest

RUN uvx tursu init -o /tests --overwrite

CMD ["uvx", "pytest", "-sv", "/tests"]
