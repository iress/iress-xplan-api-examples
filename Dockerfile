FROM jetpackio/devbox:latest

USER root:root

RUN rm -rf /homeless-shelter && \
    mkdir -p /etc/nix && \
    echo "sandbox = false" > /etc/nix/nix.conf && \
    echo "build-users-group =" >> /etc/nix/nix.conf

ENV HOME=/tmp

WORKDIR /app
RUN chown devbox:devbox /app

USER devbox

# Copy dependency files first for better caching
COPY --chown=devbox:devbox devbox.json devbox.lock ./
COPY --chown=devbox:devbox pyproject.toml uv.lock ./
COPY --chown=devbox:devbox scripts/ ./scripts/

# Install dependencies in separate layer for caching
RUN devbox run install

# Copy remaining files
COPY --chown=devbox:devbox ci/ ./ci/
COPY --chown=devbox:devbox src/ ./src/
