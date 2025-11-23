#!/bin/bash

# Define port
PORT=8000

echo "--- Iniciando Servidor de Desarrollo ---"

# Check if port is in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  El puerto $PORT está ocupado. Matando proceso anterior..."
    fuser -k $PORT/tcp >/dev/null 2>&1
    sleep 1
    echo "✅ Puerto liberado."
fi

# Change to public directory
cd public

# Start server
echo "🚀 Servidor corriendo en http://localhost:$PORT"
echo "Presiona Ctrl+C para detener."
python3 -m http.server $PORT
