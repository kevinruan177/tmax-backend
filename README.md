# TMAX Backend API v2.0

Backend FastAPI completo com autenticação JWT, CRUD de usuários, drivers, e upload de imagens para o frontend TMAX.

## Estrutura do Projeto

```
tmax-backend/
├── app/
│   ├── auth.py                  # Autenticação JWT
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py          # Configuração SQLite
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py           # Model Usuario
│   │   ├── driver.py            # Models Driver e Motorcycle
│   │   └── schemas.py           # Schemas Pydantic
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── usuario_controller.py
│   │   └── driver_controller.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── usuario_routes.py
│   │   ├── auth_routes.py
│   │   └── driver_routes.py
│   └── __init__.py
├── main.py                      # Aplicação principal
├── requirements.txt             # Dependências
└── README.md
```

## Instalação

```bash
pip install -r requirements.txt
```

## Executar

```bash
uvicorn main:app --reload
```

API disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

## Endpoints Principais

### Health Check
- **GET** `/` - Raiz da API
- **GET** `/health` - Status da API

### Autenticação
- **POST** `/auth/register` - Registrar novo driver
- **POST** `/auth/login` - Fazer login do driver

### Drivers
- **GET** `/driver/me` - Obter dados do driver logado
- **GET** `/driver/{driver_id}` - Obter dados de um driver
- **PUT** `/driver/{driver_id}` - Atualizar dados do driver
- **POST** `/driver/upload/profile` - Upload de foto de perfil
- **POST** `/driver/upload/rg` - Upload de fotos de RG

### Veículos
- **POST** `/driver/vehicle` - Upload de imagem da moto
- **GET** `/driver/vehicle/{driver_id}` - Obter dados da moto
- **PUT** `/driver/vehicle/{motorcycle_id}` - Atualizar dados da moto

### Usuários (Legacy)
- **POST** `/usuarios/` - Criar usuário
- **GET** `/usuarios/` - Listar usuários
- **GET** `/usuarios/{usuario_id}` - Buscar usuário
- **PUT** `/usuarios/{usuario_id}` - Atualizar usuário
- **DELETE** `/usuarios/{usuario_id}` - Deletar usuário

## Models de Dados

### Driver (Motorista)
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "cpf": "123.456.789-00",
  "phone": "(11) 99999-9999",
  "password": "hashed_password",
  "profile_image": "base64_string",
  "rg_images": "json_array_base64",
  "address_proof": "endereço",
  "is_active": true,
  "created_at": "2025-12-04T10:00:00",
  "updated_at": "2025-12-04T10:00:00"
}
```

### Motorcycle (Motocicleta)
```json
{
  "id": 1,
  "driver_id": 1,
  "brand": "Honda",
  "model": "CB 500",
  "year": "2023",
  "plate": "ABC-1234",
  "image": "base64_string",
  "is_active": true,
  "created_at": "2025-12-04T10:00:00",
  "updated_at": "2025-12-04T10:00:00"
}
```

## Recursos Implementados

✅ CRUD completo (Create, Read, Update, Delete)
✅ Autenticação JWT
✅ Hash de senha com bcrypt
✅ Upload de imagens (base64)
✅ Validação com Pydantic
✅ Email e CPF únicos no banco
✅ Tratamento de erros HTTP
✅ CORS habilitado
✅ Documentação automática Swagger
✅ Models para Driver e Motorcycle
✅ Separação por padrão MVC

## Exemplo de Uso

### Registrar Driver
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "cpf": "123.456.789-00",
    "phone": "(11) 99999-9999",
    "password": "senha123",
    "confirm_password": "senha123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### Upload de Foto de Perfil
```bash
curl -X POST http://localhost:8000/driver/upload/profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "driver_id=1" \
  -F "file=@/path/to/photo.jpg"
```

### Upload de Imagem da Moto
```bash
curl -X POST http://localhost:8000/driver/vehicle \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/motorcycle.jpg"
```

## Integração com Frontend

O backend está pronto para ser integrado com o frontend TMAX. Os endpoints estão configurados para:

1. **Registro de motoristas** com validação de email e CPF
2. **Login com JWT** para autenticação
3. **Upload de imagens** em base64
4. **Gerenciamento de dados** de drivers e motos
5. **CORS habilitado** para chamadas do frontend

Base URL do frontend: `http://localhost:8000`

## Segurança

⚠️ **IMPORTANTE**: Em produção:
- Mudar `SECRET_KEY` em `app/auth.py`
- Usar variáveis de ambiente para configurações sensíveis
- Implementar HTTPS
- Limitar CORS a domínios específicos
- Adicionar rate limiting
- Implementar logging de segurança

## Próximas Melhorias

- [ ] Testes unitários
- [ ] Logging estruturado
- [ ] Refresh tokens
- [ ] Roles e permissões
- [ ] Compressão de imagens
- [ ] Integração com serviço de SMS para OTP
- [ ] Documentação de API avançada
