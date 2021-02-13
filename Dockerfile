ARG PYTHON_VERSION=3.9
ARG CI_COMMIT_SHORT_SHA=NOPE
ARG CI_COMMIT_MESSAGE=HELLO
# ==============================================================================
FROM python:${PYTHON_VERSION}-slim-buster
# ================================== ENV =======================================
ENV COMMIT_HASH ${CI_COMMIT_SHORT_SHA}
ENV COMMIT_MESSAGE ${CI_COMMIT_MESSAGE}
ENV PYTHONPATH /app
# ================================== BUILDER ===================================

COPY ./requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt 


COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN ["chmod", "+x", "/app/docker-entrypoint.sh"]
COPY ./mock_services /app/mock_services
COPY ./profiles /app/profiles
COPY ./specs /app/specs
# ================================================================
WORKDIR /app
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
