# Guia de Integração Frontend-Backend TMAX

## 🚀 Visão Geral

O backend TMAX v2.0 foi desenvolvido para suportar todas as funcionalidades do frontend TMAX, incluindo:

- Autenticação JWT
- Gerenciamento de drivers (motoristas)
- Upload de imagens (foto de perfil, RG, moto)
- Gerenciamento de motocicletas

## 📋 Setup do Backend

### 1. Instalar Dependências
```bash
cd tmax-backend
pip install -r requirements.txt
```

### 2. Executar o Backend
```bash
uvicorn main:app --reload
```

Acesse: `http://localhost:8000/docs` para ver a documentação interativa.

## 🔗 Integração com Frontend

### 1. Configurar URL da API

No frontend, a URL da API já está configurada como `http://localhost:8000`. Se precisar alterar, use variável de ambiente:

```javascript
// .env (na pasta do frontend)
VITE_API_URL=http://localhost:8000
```

### 2. Fluxo de Registro

**Frontend → Backend:**
1. Usuário preenche formulário de registro com: nome, email, cpf, phone, password
2. Frontend chama `POST /auth/register`
3. Backend valida dados e cria driver no banco de dados
4. Backend retorna dados do driver criado

**Código no Frontend:**
```javascript
import { authService } from "../services/api";

const handleRegister = async () => {
  try {
    const response = await authService.register({
      name: name,
      email: email,
      cpf: cpf,
      phone: phone,
      password: password,
      confirm_password: confirmPassword
    });
    
    // Salvar token
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("driver_id", response.data.id);
    
    navigate("/driver-registration");
  } catch (error) {
    alert(error.response.data.detail);
  }
};
```

### 3. Fluxo de Login

**Frontend → Backend:**
1. Usuário insere email e senha
2. Frontend chama `POST /auth/login`
3. Backend valida credenciais e retorna JWT token
4. Frontend armazena token no localStorage

**Código no Frontend:**
```javascript
import { authService } from "../services/api";

const handleLogin = async () => {
  try {
    const response = await authService.login(email, password);
    
    // Salvar token
    localStorage.setItem("access_token", response.data.access_token);
    
    // Obter dados do driver
    const driverResponse = await driverService.getMe();
    localStorage.setItem("currentUser", JSON.stringify(driverResponse.data));
    
    navigate("/RoutesToDo");
  } catch (error) {
    alert("Email ou senha incorretos");
  }
};
```

### 4. Upload de Foto de Perfil

**Frontend → Backend:**
1. Usuário seleciona arquivo de foto
2. Frontend converte para base64 e envia via `POST /driver/upload/profile`
3. Backend armazena imagem no banco de dados

**Código no Frontend:**
```javascript
import { driverService } from "../services/api";

const handlePhotoUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const driverId = JSON.parse(localStorage.getItem("currentUser"))?.id;
    await driverService.uploadProfilePhoto(driverId, file);
    
    // Recarregar dados do driver
    const response = await driverService.getDriver(driverId);
    localStorage.setItem("currentUser", JSON.stringify(response.data));
    
    alert("Foto atualizada com sucesso!");
  } catch (error) {
    console.error("Erro ao fazer upload:", error);
  }
};
```

### 5. Upload de Fotos de RG

**Frontend → Backend:**
1. Usuário seleciona até 2 fotos de RG
2. Frontend envia arquivo via `POST /driver/upload/rg`
3. Backend armazena múltiplas imagens

**Código no Frontend:**
```javascript
import { driverService } from "../services/api";

const handleRgUpload = async (files) => {
  try {
    const driverId = JSON.parse(localStorage.getItem("currentUser"))?.id;
    await driverService.uploadRG(driverId, files);
    alert("RG enviado com sucesso!");
  } catch (error) {
    console.error("Erro ao fazer upload:", error);
  }
};
```

### 6. Upload de Imagem da Motocicleta

**Frontend → Backend:**
1. Usuário seleciona foto da moto
2. Frontend envia via `POST /driver/vehicle`
3. Backend cria ou atualiza registro de motocicleta

**Código no Frontend:**
```javascript
import { motorcycleService } from "../services/api";

const handleSubmit = async () => {
  try {
    const driverId = JSON.parse(localStorage.getItem("currentUser"))?.id;
    
    if (motorcycleImage) {
      await motorcycleService.uploadImage(motorcycleImage, driverId);
    }
    
    alert("Motocicleta registrada com sucesso!");
    navigate("/next-page");
  } catch (error) {
    console.error("Erro ao fazer upload:", error);
  }
};
```

## 🔐 Autenticação JWT

### Como Funciona

1. **Login**: Frontend envia credenciais → Backend retorna JWT token
2. **Requisições Autenticadas**: Frontend envia token no header `Authorization: Bearer {token}`
3. **Validação**: Backend valida token em cada requisição

### Token JWT

O token contém:
- Email do driver
- Data de expiração (30 minutos)
- Assinatura criptográfica

### Exemplo de Requisição Autenticada

```javascript
// Automaticamente adicionado pelo interceptor
const config = {
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
};

api.get("/driver/me", config);
```

## 📦 Estrutura de Dados

### Registro de Driver (Response)
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "cpf": "123.456.789-00",
  "phone": "(11) 99999-9999",
  "is_active": true,
  "created_at": "2025-12-04T10:00:00",
  "updated_at": "2025-12-04T10:00:00"
}
```

### Token de Login (Response)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Upload de Imagem (Response)
```json
{
  "message": "Imagem da motocicleta atualizada com sucesso",
  "motorcycle_id": 1,
  "driver_id": 1
}
```

## 🐛 Tratamento de Erros

O backend retorna erros HTTP com mensagens descritivas:

```javascript
try {
  await authService.register(data);
} catch (error) {
  // error.response.status: código HTTP (400, 401, 404, etc)
  // error.response.data.detail: mensagem de erro
  console.error(error.response.data.detail);
}
```

### Códigos HTTP Comuns

- **400 Bad Request**: Dados inválidos (email duplicado, senhas diferentes, etc)
- **401 Unauthorized**: Token inválido ou expirado
- **403 Forbidden**: Sem permissão para acessar recurso
- **404 Not Found**: Recurso não encontrado

## ✅ Checklist de Integração

- [ ] Backend rodando em `http://localhost:8000`
- [ ] Frontend consegue acessar `/health`
- [ ] Registro de novo driver funciona
- [ ] Login funciona e retorna token
- [ ] Upload de foto de perfil funciona
- [ ] Upload de RG funciona
- [ ] Upload de imagem de moto funciona
- [ ] Obtém dados do driver logado com `GET /driver/me`
- [ ] Logout remove token do localStorage

## 🔧 Troubleshooting

### CORS Error
Se receber erro de CORS, verifique:
- Backend rodando com CORS habilitado (está)
- URL da API correta no frontend

### Token Expirado
Se receber erro 401:
- Verificar se token está no localStorage
- Verificar se token ainda é válido (30 minutos)
- Fazer novo login para obter novo token

### Imagem não salva
- Verificar se arquivo é válido
- Verificar se driver_id está correto
- Ver logs do backend

## 📚 Documentação da API

Acesse `http://localhost:8000/docs` para:
- Testar endpoints interativamente
- Ver modelos de dados
- Ver respostas esperadas

## 🚀 Deploy

Em produção:
1. Alterar `SECRET_KEY` em `app/auth.py`
2. Usar variáveis de ambiente para configurações
3. Implementar HTTPS
4. Limitar CORS a domínios específicos
5. Usar banco de dados PostgreSQL em vez de SQLite
