FROM jetpackio/devbox:latest

USER root:root

# 1. Ensure /homeless-shelter is gone and
# 2. Set sandbox to false (Docker already provides its own isolation)
RUN rm -rf /homeless-shelter && \
    mkdir -p /etc/nix && \
    echo "sandbox = false" > /etc/nix/nix.conf && \
    echo "build-users-group =" >> /etc/nix/nix.conf

# 3. Redirect HOME so tools don't try to recreate /homeless-shelter
ENV HOME=/tmp

ADD ci/ /app/ci
ADD scripts/ /app/scripts
ADD devbox.json /app/devbox.json
ADD devbox.lock /app/devbox.lock
ADD uv.lock /app/uv.lock
ADD pyproject.toml /app/pyproject.toml

WORKDIR /app

# Ensure permissions are correct if you added files as root
RUN chown -R devbox:devbox /app

USER devbox

RUN devbox run install

ADD . /app
