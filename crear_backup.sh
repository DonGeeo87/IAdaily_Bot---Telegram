#!/bin/bash
# 📦 Script de Backup para Migración
# Ejecutar en el móvil antes de migrar a laptop

echo "📦 IA Daily Bot - Backup para Migración"
echo "========================================"
echo ""

# Directorios
BACKUP_DIR=~/telegram-ia-bot-backup
PROJECT_DIR=~/telegram-ia-bot

# Crear directorio de backup
echo "📁 Creando directorio de backup..."
mkdir -p $BACKUP_DIR

# Copiar archivos de código
echo "📋 Copiando archivos de código..."
cp -r $PROJECT_DIR/*.py $BACKUP_DIR/ 2>/dev/null
cp -r $PROJECT_DIR/*.sh $BACKUP_DIR/ 2>/dev/null
cp -r $PROJECT_DIR/*.md $BACKUP_DIR/ 2>/dev/null
cp -r $PROJECT_DIR/*.json $BACKUP_DIR/ 2>/dev/null
cp -r $PROJECT_DIR/*.modelfile $BACKUP_DIR/ 2>/dev/null

# Copiar directorios importantes
echo "📂 Copiando directorios..."
cp -r $PROJECT_DIR/triggers $BACKUP_DIR/ 2>/dev/null
cp -r $PROJECT_DIR/social_posts $BACKUP_DIR/ 2>/dev/null

# NO copiar: logs, posts, campaign, __pycache__

# Crear archivo de instrucciones
cat > $BACKUP_DIR/LEERME.txt << 'EOF'
📦 BACKUP DE IA DAILY BOT
=========================

Este backup contiene:
✅ Todo el código Python (.py)
✅ Scripts de shell (.sh)
✅ Documentación (.md)
✅ Archivos de configuración (.json)

⚠️ IMPORTANTE:
Los archivos de configuración contienen datos sensibles:
- config.json: Token del bot
- apis_config.json: API keys
- security.json: Usuarios y permisos

📋 PRÓXIMOS PASOS:

1. Transferir esta carpeta a tu laptop:
   - USB
   - Google Drive
   - SCP/SFTP
   - Email (si no es muy grande)

2. En la laptop:
   a) Crear entorno virtual: python -m venv venv
   b) Activar: source venv/bin/activate
   c) Instalar: pip install -r requirements.txt
   d) Configurar archivos .json con tus credenciales

3. Para subir a GitHub:
   cd telegram-ia-bot-backup
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin TU_REPO_URL
   git push -u origin main

📞 Tu chat_id: 2036304183

EOF

# Crear lista de archivos
echo "📝 Creando lista de archivos..."
ls -la $BACKUP_DIR/ > $BACKUP_DIR/FILES.txt

# Mostrar resumen
echo ""
echo "✅ Backup completado!"
echo ""
echo "📁 Ubicación: $BACKUP_DIR"
echo ""
echo "📊 Archivos copiados:"
ls -1 $BACKUP_DIR | wc -l
echo ""
echo "📦 Tamaño total:"
du -sh $BACKUP_DIR
echo ""
echo "🔤 Para transferir:"
echo "   - USB: Conectá el móvil y copiá la carpeta"
echo "   - Google Drive: Subí $BACKUP_DIR"
echo "   - SCP: scp -r $BACKUP_DIR user@laptop:~/projects/"
echo ""
echo "⚠️  NO OLVIDES:"
echo "   - config.json tiene tu token del bot"
echo "   - apis_config.json tiene la API key de GNews"
echo "   - security.json tiene tu chat_id: 2036304183"
echo ""
