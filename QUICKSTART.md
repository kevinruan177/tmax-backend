# ⚡ Quick Start - TMAX Backend v2.0

## 🚀 30 Segundos para Rodar

```bash
# 1. Ir para pasta
cd tmax-backend

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar backend
uvicorn main:app --reload
```

✅ Backend rodando em `http://localhost:8000`

---

## 🔗 Acessar Documentação

```
http://localhost:8000/docs
```

Nesta página você pode:
- ✅ Ver todos os endpoints
- ✅ Testar requisições
- ✅ Ver modelos de dados
- ✅ Ver responses esperadas

---

## 🧪 Testar Rápido

### 1. Registrar Driver
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João",
    "email": "joao@test.com",
    "cpf": "123.456.789-00",
    "phone": "(11)99999-9999",
    "password": "senha123",
    "confirm_password": "senha123"
  }'
```

### 2. Fazer Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@test.com",
    "password": "senha123"
  }'
```

Copiar o `access_token` da resposta.

### 3. Testar Endpoint Protegido
```bash
curl -X GET http://localhost:8000/driver/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## 📁 Arquivos Principais

```
main.py                    ← Aplicação principal
app/
  ├── auth.py              ← JWT
  ├── config/database.py   ← Banco de dados
  ├── models/              ← Entidades
  ├── controllers/         ← Lógica de negócio
  └── routes/              ← Endpoints
```

---

## 🔧 Configurar Frontend

No arquivo `services/api.js` do frontend, já está configurado:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

Se mudar a porta, altere aqui também.

---

## 🆘 Problemas Comuns

### Porta 8000 já está em uso
```bash
# Use outra porta
uvicorn main:app --reload --port 8001
```

### ModuleNotFoundError
```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### CORS Error (Acesso negado)
- Certificar que backend está rodando
- Certificar que URL está correta em api.js

### Banco não existir
- Será criado automaticamente na primeira execução
- Arquivo `tmax.db` será criado na raiz

---

## 📚 Ler Documentação Completa

1. **README.md** - Visão geral
2. **INTEGRATION_GUIDE.md** - Integrar frontend
3. **DEPLOYMENT_GUIDE.md** - Deploy em produção

---

## ✅ Checklist Rápido

- [ ] Backend rodando
- [ ] Acessar `/docs` funcionando
- [ ] Registrar driver funcionando
- [ ] Login funcionando
- [ ] Token sendo gerado
- [ ] Frontend consegue chamar API

---

## 🎉 Pronto!

Seu backend TMAX v2.0 está 100% funcional! 🚀

Próximo passo: Testar com o frontend TMAX e começar a desenvolver novos features.

---

**Dúvidas? Acesse `http://localhost:8000/docs` para tester tudo interativamente!**
