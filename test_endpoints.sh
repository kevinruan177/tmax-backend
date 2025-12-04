#!/bin/bash
# Script de teste dos endpoints da API TMAX

BASE_URL="http://localhost:8000"

echo "===== TMAX API - Teste de Endpoints ====="
echo ""

# 1. Health Check
echo "1. Health Check"
curl -s -X GET "$BASE_URL/health" | jq .
echo ""

# 2. Registrar novo driver
echo "2. Registrar novo driver"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "cpf": "123.456.789-00",
    "phone": "(11) 98765-4321",
    "password": "senha123",
    "confirm_password": "senha123"
  }')
echo "$REGISTER_RESPONSE" | jq .
DRIVER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.id')
echo "Driver ID criado: $DRIVER_ID"
echo ""

# 3. Login
echo "3. Login do driver"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@example.com",
    "password": "senha123"
  }')
echo "$LOGIN_RESPONSE" | jq .
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')
echo "Token: $TOKEN"
echo ""

# 4. Obter dados do driver logado
echo "4. Obter dados do driver logado"
curl -s -X GET "$BASE_URL/driver/me" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 5. Obter driver específico
echo "5. Obter driver específico"
curl -s -X GET "$BASE_URL/driver/$DRIVER_ID" | jq .
echo ""

# 6. Atualizar driver
echo "6. Atualizar dados do driver"
curl -s -X PUT "$BASE_URL/driver/$DRIVER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Santos",
    "phone": "(11) 99999-8888"
  }' | jq .
echo ""

# 7. Criar arquivo de teste para upload
echo "7. Criando arquivo de teste para upload..."
echo "fake image data" > /tmp/test_image.txt
echo ""

# 8. Upload de imagem de moto
echo "8. Upload de imagem da moto"
curl -s -X POST "$BASE_URL/driver/vehicle" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_image.txt" \
  -F "driver_id=$DRIVER_ID" | jq .
echo ""

# 9. Obter motocicleta do driver
echo "9. Obter dados da motocicleta do driver"
curl -s -X GET "$BASE_URL/driver/vehicle/$DRIVER_ID" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 10. Listar usuários (endpoint legado)
echo "10. Listar usuários (endpoint legado)"
curl -s -X GET "$BASE_URL/usuarios/" | jq .
echo ""

echo "===== Testes Concluídos ====="
echo ""
echo "Dica: Acesse http://localhost:8000/docs para tester endpoints interativamente!"
