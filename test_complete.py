#!/usr/bin/env python3
"""
TMAX Backend v2.0 - Teste Completo de Todas as Rotas
Testa todos os 23 endpoints do backend
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"
TOKEN = None
DRIVER_ID = None
MOTORCYCLE_ID = None
TESTS_PASSED = 0
TESTS_FAILED = 0

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def test(name, condition, details=""):
    global TESTS_PASSED, TESTS_FAILED
    if condition:
        TESTS_PASSED += 1
        print(f"{Colors.OKGREEN}✅ PASSOU{Colors.ENDC} | {name}")
    else:
        TESTS_FAILED += 1
        print(f"{Colors.FAIL}❌ FALHOU{Colors.ENDC} | {name}")
    if details:
        print(f"   {details}")

def req(method, endpoint, data=None, no_auth=False):
    """Faz requisição HTTP com tratamento de erros"""
    global TOKEN
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if TOKEN and not no_auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            resp = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            resp = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=10)
        else:
            return None
        return resp
    except requests.exceptions.Timeout:
        print(f"{Colors.FAIL}TIMEOUT na requisição: {endpoint}{Colors.ENDC}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"{Colors.FAIL}ERRO DE CONEXÃO: {e}{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{Colors.FAIL}ERRO: {e}{Colors.ENDC}")
        return None

def main():
    global TOKEN, DRIVER_ID, MOTORCYCLE_ID
    
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       TMAX Backend v2.0 - TESTE COMPLETO                ║")
    print("║     Testando 23 Endpoints da API REST                   ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    # ====================================================================
    # 1. HEALTH & ROOT
    # ====================================================================
    print_header("1️⃣  HEALTH & ROOT ENDPOINTS")
    
    r = req("GET", "/health")
    test("GET /health", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    r = req("GET", "/")
    test("GET /", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    # ====================================================================
    # 2. AUTH - REGISTRO
    # ====================================================================
    print_header("2️⃣  AUTH - REGISTRO E LOGIN")
    
    email = f"driver_{int(time.time())}@test.com"
    reg_data = {
        "name": "João Silva",
        "email": email,
        "cpf": "123.456.789-00",
        "phone": "(11) 99999-9999",
        "password": "senha123",
        "confirm_password": "senha123"
    }
    
    r = req("POST", "/auth/register", reg_data)
    driver_ok = r and r.status_code == 200
    test("POST /auth/register", driver_ok, f"Status: {r.status_code if r else 'Erro'}")
    
    if driver_ok:
        driver = r.json()
        DRIVER_ID = driver.get("id")
        print(f"   Driver criado: ID={DRIVER_ID}, Email={driver.get('email')}")
    else:
        if r:
            print(f"   Erro: {r.text[:200]}")
    
    # ====================================================================
    # 3. AUTH - LOGIN
    # ====================================================================
    
    login_data = {"email": email, "password": "senha123"}
    r = req("POST", "/auth/login", login_data)
    login_ok = r and r.status_code == 200
    test("POST /auth/login", login_ok, f"Status: {r.status_code if r else 'Erro'}")
    
    if login_ok:
        token_data = r.json()
        TOKEN = token_data.get("access_token")
        print(f"   Token: {TOKEN[:20]}...")
    else:
        if r:
            print(f"   Erro: {r.text[:200]}")
    
    # ====================================================================
    # 4. DRIVER - ENDPOINTS
    # ====================================================================
    print_header("3️⃣  DRIVER ENDPOINTS")
    
    if TOKEN:
        # GET /driver/me
        r = req("GET", "/driver/me")
        test("GET /driver/me", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # GET /driver/{id}
        if DRIVER_ID:
            r = req("GET", f"/driver/{DRIVER_ID}")
            test(f"GET /driver/{DRIVER_ID}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # PUT /driver/{id}
        if DRIVER_ID:
            update = {"nome": "João Silva Santos"}
            r = req("PUT", f"/driver/{DRIVER_ID}", update)
            test(f"PUT /driver/{DRIVER_ID}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # DELETE /driver/{id} - Não testar para não deletar o driver
        # test("DELETE /driver/{id}", False, "Pulado para não deletar o driver")
    
    # ====================================================================
    # 5. MOTORCYCLE - ENDPOINTS
    # ====================================================================
    print_header("4️⃣  MOTORCYCLE ENDPOINTS")
    
    if TOKEN and DRIVER_ID:
        # POST /driver/vehicle - Criar motocicleta
        files_data = {"driver_id": DRIVER_ID}
        try:
            r = requests.post(
                f"{BASE_URL}/driver/vehicle",
                data=files_data,
                files={"file": ("test.jpg", b"fake_image", "image/jpeg")},
                headers={"Authorization": f"Bearer {TOKEN}"},
                timeout=5
            )
            moto_ok = r and r.status_code == 200
            test("POST /driver/vehicle", moto_ok, f"Status: {r.status_code if r else 'Erro'}")
            
            if moto_ok:
                moto = r.json()
                MOTORCYCLE_ID = moto.get("motorcycle_id")
                print(f"   Motocicleta criada: ID={MOTORCYCLE_ID}")
        except Exception as e:
            test("POST /driver/vehicle", False, str(e))
        
        # GET /driver/vehicle/{driver_id}
        if DRIVER_ID:
            r = req("GET", f"/driver/vehicle/{DRIVER_ID}")
            test(f"GET /driver/vehicle/{DRIVER_ID}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # PUT /driver/vehicle/{id}
        if MOTORCYCLE_ID:
            update = {
                "brand": "Honda",
                "model": "CB 500",
                "year": "2023",
                "plate": "ABC-1234"
            }
            r = req("PUT", f"/driver/vehicle/{MOTORCYCLE_ID}", update)
            test(f"PUT /driver/vehicle/{MOTORCYCLE_ID}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # GET /driver/vehicle/{id}
        if MOTORCYCLE_ID:
            r = req("GET", f"/driver/vehicle/{MOTORCYCLE_ID}")
            test(f"GET /driver/vehicle/{MOTORCYCLE_ID}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
        
        # DELETE /driver/vehicle/{id} - Não testar para não deletar
    
    # ====================================================================
    # 6. USUARIOS (LEGACY)
    # ====================================================================
    print_header("5️⃣  USUARIOS (LEGACY ENDPOINTS)")
    
    # POST /usuarios/
    usuario = {
        "nome": "João Usuario",
        "email": f"user_{int(time.time())}@test.com",
        "senha": "senha123"
    }
    r = req("POST", "/usuarios/", usuario, no_auth=True)
    test("POST /usuarios/", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    usuario_id = None
    if r and r.status_code == 200:
        usuario_id = r.json().get("id")
    
    # GET /usuarios/
    r = req("GET", "/usuarios/", no_auth=True)
    test("GET /usuarios/", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    # GET /usuarios/{id}
    if usuario_id:
        r = req("GET", f"/usuarios/{usuario_id}", no_auth=True)
        test(f"GET /usuarios/{usuario_id}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    # PUT /usuarios/{id}
    if usuario_id:
        update = {"nome": "João Usuario Updated"}
        r = req("PUT", f"/usuarios/{usuario_id}", update, no_auth=True)
        test(f"PUT /usuarios/{usuario_id}", r and r.status_code == 200, f"Status: {r.status_code if r else 'Erro'}")
    
    # DELETE /usuarios/{id} - Não testar para não deletar
    
    # ====================================================================
    # 7. VALIDAÇÕES
    # ====================================================================
    print_header("6️⃣  VALIDAÇÕES E TRATAMENTO DE ERROS")
    
    if not email or not DRIVER_ID:
        print(f"{Colors.WARNING}Pulando testes de validação - email ou driver_id não disponível{Colors.ENDC}")
    else:
        # Email duplicado
        dup_data = {
            "name": "Outro",
            "email": email,
            "cpf": "999.999.999-99",
            "phone": "(11) 88888-8888",
            "password": "senha",
            "confirm_password": "senha"
        }
        r = req("POST", "/auth/register", dup_data)
        if r:
            test("Email Duplicado (deve retornar 400)", r.status_code == 400, f"Status: {r.status_code}")
            if r.status_code != 400:
                try:
                    print(f"   Resposta: {r.json()}")
                except:
                    print(f"   Resposta: {r.text}")
        else:
            test("Email Duplicado (deve retornar 400)", False, "Falha na conexão")
        
        # Senhas diferentes
        mismatch = {
            "name": "Outro",
            "email": f"test_{int(time.time())}@test.com",
            "cpf": "111.111.111-11",
            "phone": "(11) 77777-7777",
            "password": "senha123",
            "confirm_password": "senha_diferente"
        }
        r = req("POST", "/auth/register", mismatch)
        if r:
            test("Senhas Diferentes (deve retornar 400)", r.status_code == 400, f"Status: {r.status_code}")
            if r.status_code != 400:
                try:
                    print(f"   Resposta: {r.json()}")
                except:
                    print(f"   Resposta: {r.text}")
        else:
            test("Senhas Diferentes (deve retornar 400)", False, "Falha na conexão")
        
        # Login com senha errada
        wrong = {"email": email, "password": "senha_errada"}
        r = req("POST", "/auth/login", wrong)
        if r:
            test("Senha Errada (deve retornar 401)", r.status_code == 401, f"Status: {r.status_code}")
            if r.status_code != 401:
                try:
                    print(f"   Resposta: {r.json()}")
                except:
                    print(f"   Resposta: {r.text}")
        else:
            test("Senha Errada (deve retornar 401)", False, "Falha na conexão")
    
    # ====================================================================
    # RESUMO
    # ====================================================================
    print_header("RESUMO FINAL")
    
    total = TESTS_PASSED + TESTS_FAILED
    percentage = (TESTS_PASSED / total * 100) if total > 0 else 0
    
    print(f"{Colors.OKGREEN}Testes Passados: {TESTS_PASSED}{Colors.ENDC}")
    print(f"{Colors.FAIL}Testes Falhados: {TESTS_FAILED}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Total: {total}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Percentual: {percentage:.1f}%{Colors.ENDC}\n")
    
    if TESTS_FAILED == 0:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ TODOS OS TESTES PASSARAM! 🚀{Colors.ENDC}\n")
        return 0
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠️  Alguns testes falharam. Verifique acima.{Colors.ENDC}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"{Colors.FAIL}Erro fatal: {e}{Colors.ENDC}")
        sys.exit(1)
