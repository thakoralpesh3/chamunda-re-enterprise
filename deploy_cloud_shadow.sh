#!/usr/bin/env bash
# ==============================================================================
# Chamunda Automobile Enterprise • Project Chhaya (Cloud Shadow Deployment)
# One-click deployment packaging script for 24/7 Standby Cloud Hosting.
# ==============================================================================

set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$BASE_DIR/build_cloud_shadow"

echo "☁️ Packaging Chamunda Cloud Shadow Standby Mirror..."

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/data"

# Copy essential files for cloud mirror
cp "$BASE_DIR/cloud_mirror_server.py" "$BUILD_DIR/main.py"
cp "$BASE_DIR/cloud_shadow_engine.py" "$BUILD_DIR/"
cp "$BASE_DIR/chhaya_agent_gateway.py" "$BUILD_DIR/"
cp "$BASE_DIR/dms_enterprise_suite_engine.py" "$BUILD_DIR/"
cp "$BASE_DIR/kalpavriksha_growth_engine.py" "$BUILD_DIR/"
cp "$BASE_DIR/system_optimizer.py" "$BUILD_DIR/"
cp "$BASE_DIR/whatsapp_dispatch_engine.py" "$BUILD_DIR/"

# Copy static directory (PWA manifest, icons, styling)
cp -r "$BASE_DIR/static" "$BUILD_DIR/"

# Copy data state files
cp "$BASE_DIR/data/cloud_shadow_state.json" "$BUILD_DIR/data/"
cp "$BASE_DIR/data/chhaya_all_agents.json" "$BUILD_DIR/data/" 2>/dev/null || true
cp "$BASE_DIR/data/re_parts_catalog.json" "$BUILD_DIR/data/" 2>/dev/null || true
cp "$BASE_DIR/data/cloudflare_config.json" "$BUILD_DIR/data/" 2>/dev/null || true

# Create Procfile for Heroku / Render / Railway
cat << 'EOF' > "$BUILD_DIR/Procfile"
web: python3 main.py
EOF

# Create requirements.txt
cat << 'EOF' > "$BUILD_DIR/requirements.txt"
fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.6.0
psutil>=5.9.0
python-multipart>=0.0.9
EOF

# Create Dockerfile for Google Cloud Run / Fly.io
cat << 'EOF' > "$BUILD_DIR/Dockerfile"
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD ["python", "main.py"]
EOF

chmod +x "$BUILD_DIR/main.py"
echo "✅ Complete Cloud Shadow Standby Mirror successfully packaged in: $BUILD_DIR"
echo "📲 Ready for 24/7 zero-cost cloud hosting on Render, Railway, Fly.io, or Google Cloud Run."
echo "🌐 This cloud mirror runs 24/7 even when this laptop is completely switched off!"
