import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"
        assert "timestamp" in data
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Sistema de Gestão para Profissional Liberal"
        assert data["version"] == "2.0.0"
        assert data["status"] == "online"


class TestAuthenticationAPI:
    """Test authentication API endpoints"""
    
    def test_login_valid_credentials(self, client: TestClient):
        """Test login with valid credentials"""
        login_data = {
            "email": "joao@exemplo.com",
            "senha": "123456"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        login_data = {
            "email": "joao@exemplo.com",
            "senha": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        
        data = response.json()
        assert "message" in data
        assert data["success"] is False
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent user"""
        login_data = {
            "email": "nonexistent@example.com",
            "senha": "password"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_login_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format"""
        login_data = {
            "email": "invalid-email",
            "senha": "password"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_current_user(self, client: TestClient, auth_headers):
        """Test getting current user info"""
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["user_id"] == "test-user-id"
        assert data["authenticated"] is True
    
    def test_get_current_user_without_token(self, client: TestClient):
        """Test getting current user without token"""
        response = client.get("/auth/me")
        assert response.status_code == 403  # No authorization header


class TestClienteAPI:
    """Test client API endpoints"""
    
    def test_get_clientes_empty(self, client: TestClient, auth_headers):
        """Test getting clients when database is empty"""
        response = client.get("/clientes", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_create_cliente_valid(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test creating a valid client"""
        response = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nome"] == sample_cliente_data["nome"]
        assert data["telefone"] == sample_cliente_data["telefone"]
        assert data["email"] == sample_cliente_data["email"]
        assert data["etiquetas"] == sample_cliente_data["etiquetas"]
        assert "id" in data
        assert "data_criacao" in data
    
    def test_create_cliente_invalid_data(self, client: TestClient, auth_headers):
        """Test creating client with invalid data"""
        invalid_data = {
            "nome": "A",  # Too short
            "telefone": "123",  # Too short
            "email": "invalid-email"
        }
        
        response = client.post("/clientes", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error
    
    def test_create_cliente_duplicate_email(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test creating client with duplicate email"""
        # Create first client
        response1 = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        assert response1.status_code == 200
        
        # Try to create second client with same email
        response2 = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        assert response2.status_code == 400
        
        data = response2.json()
        assert "Email já cadastrado" in data["message"]
    
    def test_get_clientes_with_data(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test getting clients after creating some"""
        # Create a client first
        create_response = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        assert create_response.status_code == 200
        
        # Get clients
        response = client.get("/clientes", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["nome"] == sample_cliente_data["nome"]
    
    def test_get_cliente_by_id(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test getting specific client by ID"""
        # Create a client first
        create_response = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        created_client = create_response.json()
        client_id = created_client["id"]
        
        # Get client by ID
        response = client.get(f"/clientes/{client_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == client_id
        assert data["nome"] == sample_cliente_data["nome"]
    
    def test_get_cliente_nonexistent(self, client: TestClient, auth_headers):
        """Test getting nonexistent client"""
        response = client.get("/clientes/nonexistent-id", headers=auth_headers)
        assert response.status_code == 404
        
        data = response.json()
        assert "Cliente não encontrado" in data["message"]
    
    def test_update_cliente(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test updating a client"""
        # Create a client first
        create_response = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        created_client = create_response.json()
        client_id = created_client["id"]
        
        # Update client
        update_data = {"nome": "João Santos", "telefone": "+5511888888888"}
        response = client.put(f"/clientes/{client_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nome"] == "João Santos"
        assert data["telefone"] == "+5511888888888"
        assert data["email"] == sample_cliente_data["email"]  # Should remain unchanged
    
    def test_update_cliente_nonexistent(self, client: TestClient, auth_headers):
        """Test updating nonexistent client"""
        update_data = {"nome": "João Santos"}
        response = client.put("/clientes/nonexistent-id", json=update_data, headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_cliente(self, client: TestClient, auth_headers, sample_cliente_data):
        """Test deleting a client"""
        # Create a client first
        create_response = client.post("/clientes", json=sample_cliente_data, headers=auth_headers)
        created_client = create_response.json()
        client_id = created_client["id"]
        
        # Delete client
        response = client.delete(f"/clientes/{client_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Cliente removido com sucesso"
        assert data["success"] is True
        
        # Verify client is deleted
        get_response = client.get(f"/clientes/{client_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_cliente_nonexistent(self, client: TestClient, auth_headers):
        """Test deleting nonexistent client"""
        response = client.delete("/clientes/nonexistent-id", headers=auth_headers)
        assert response.status_code == 404
    
    def test_search_clientes(self, client: TestClient, auth_headers):
        """Test searching clients"""
        # Create test clients
        client1_data = {
            "nome": "João Silva",
            "telefone": "+5511999999999",
            "email": "joao@teste.com",
            "etiquetas": ["vip"]
        }
        client2_data = {
            "nome": "Maria Santos",
            "telefone": "+5511888888888",
            "email": "maria@teste.com",
            "etiquetas": ["novo"]
        }
        
        client.post("/clientes", json=client1_data, headers=auth_headers)
        client.post("/clientes", json=client2_data, headers=auth_headers)
        
        # Search by name
        response = client.get("/clientes?busca=João", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nome"] == "João Silva"
        
        # Search by email
        response = client.get("/clientes?busca=maria@teste.com", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["nome"] == "Maria Santos"
    
    def test_get_etiquetas(self, client: TestClient, auth_headers):
        """Test getting client tags"""
        # Create clients with tags
        client1_data = {
            "nome": "João Silva",
            "telefone": "+5511999999999",
            "email": "joao@teste.com",
            "etiquetas": ["vip", "regular"]
        }
        client2_data = {
            "nome": "Maria Santos",
            "telefone": "+5511888888888",
            "email": "maria@teste.com",
            "etiquetas": ["novo", "vip"]
        }
        
        client.post("/clientes", json=client1_data, headers=auth_headers)
        client.post("/clientes", json=client2_data, headers=auth_headers)
        
        # Get tags
        response = client.get("/clientes/etiquetas", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "etiquetas" in data
        etiquetas = data["etiquetas"]
        assert "vip" in etiquetas
        assert "regular" in etiquetas
        assert "novo" in etiquetas
        assert len(set(etiquetas)) == len(etiquetas)  # No duplicates


class TestAuthorizationRequired:
    """Test that endpoints require authorization"""
    
    def test_clientes_requires_auth(self, client: TestClient):
        """Test that client endpoints require authentication"""
        # GET /clientes
        response = client.get("/clientes")
        assert response.status_code == 403
        
        # POST /clientes
        response = client.post("/clientes", json={})
        assert response.status_code == 403
        
        # GET /clientes/{id}
        response = client.get("/clientes/some-id")
        assert response.status_code == 403
        
        # PUT /clientes/{id}
        response = client.put("/clientes/some-id", json={})
        assert response.status_code == 403
        
        # DELETE /clientes/{id}
        response = client.delete("/clientes/some-id")
        assert response.status_code == 403

