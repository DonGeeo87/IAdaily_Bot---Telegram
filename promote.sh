#!/bin/bash
# 🚀 MASTER SCRIPT - Automatización completa de promoción
# Ejecutar: bash promote.sh

set -e

echo "╔═══════════════════════════════════════════════╗"
echo "   🚀 IA Daily - Sistema de Promoción Automática"
echo "╚═══════════════════════════════════════════════╝"
echo ""

cd ~/telegram-ia-bot

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}▶ $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Paso 1: Generar kit de promoción
print_step "1/4 Generando kit de promoción..."
python auto_promotion.py
print_success "Kit de promoción generado"
echo ""

# Paso 2: Generar posts para redes
print_step "2/4 Generando posts para redes sociales..."
python social_poster.py
print_success "Posts para redes generados"
echo ""

# Paso 3: Verificar crecimiento
print_step "3/4 Verificando crecimiento del canal..."
python growth_tracker.py
echo ""

# Paso 4: Mostrar resumen
print_step "4/4 Resumen de promoción"
echo ""
echo "📊 ARCHIVOS GENERADOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh promotion_kit.json 2>/dev/null && echo ""
ls -lh social_posts/ 2>/dev/null && echo ""
ls -lh posts/ 2>/dev/null && echo ""

echo ""
echo "🔗 ENLACES PARA COMPARTIR:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "WhatsApp:  https://wa.me/?text=Únete%20a%20https://t.me/IADailyChannel"
echo "Twitter:   https://twitter.com/intent/tweet?text=Únete%20a%20https://t.me/IADailyChannel"
echo "Facebook:  https://www.facebook.com/sharer/sharer.php?u=https://t.me/IADailyChannel"
echo "LinkedIn:  https://www.linkedin.com/sharing/share-offsite/?url=https://t.me/IADailyChannel"
echo ""

echo "╔═══════════════════════════════════════════════╗"
echo "   ✅ ¡Promoción completada!"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo ""
echo "1. Comparte los enlaces en tus redes personales"
echo "2. Publica en Reddit (r/IA, r/InteligenciaArtificial)"
echo "3. Únete a grupos de Facebook de IA"
echo "4. Crea 1-2 TikToks usando los guiones generados"
echo "5. Programa los posts con Buffer o Hootsuite"
echo ""
echo "📖 Guía completa: PROMOTION_GUIDE.md"
echo ""
