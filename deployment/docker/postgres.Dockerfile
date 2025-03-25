FROM postgres:15-alpine

# Environment variables for database initialization
ENV POSTGRES_USER=llmchat
ENV POSTGRES_PASSWORD=postgres_password
ENV POSTGRES_DB=llmchat_db

# Add custom initialization scripts if needed
COPY deployment/docker/postgres/init.sql /docker-entrypoint-initdb.d/

# Set the data directory
VOLUME ["/var/lib/postgresql/data"]

# Expose the PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB} || exit 1