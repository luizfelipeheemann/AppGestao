import pytest
from datetime import datetime, timedelta
from jose import jwt
from auth import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, verify_token, authenticate_user,
    auth_rate_limiter
)
from config import settings


class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Verification should work
        assert verify_password(password, hashed) is True
        
        # Wrong password should fail
        assert verify_password("WrongPassword", hashed) is False
    
    def test_different_hashes_for_same_password(self):
        """Test that same password generates different hashes"""
        password = "TestPassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different (due to salt)
        assert hash1 != hash2
        
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestTokenGeneration:
    """Test JWT token generation and verification"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_access_token(data)
        
        # Token should be a string
        assert isinstance(token, str)
        
        # Token should be decodable
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == "123"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_refresh_token(data)
        
        # Token should be a string
        assert isinstance(token, str)
        
        # Token should be decodable
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == "123"
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload
    
    def test_create_token_with_custom_expiration(self):
        """Test token creation with custom expiration"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta)
        
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp_time = datetime.fromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + expires_delta
        
        # Should expire in approximately 5 minutes (allow 1 second tolerance)
        assert abs((exp_time - expected_exp).total_seconds()) < 1


class TestTokenVerification:
    """Test JWT token verification"""
    
    def test_verify_valid_access_token(self):
        """Test verification of valid access token"""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_access_token(data)
        
        payload = verify_token(token, "access")
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == "123"
        assert payload["type"] == "access"
    
    def test_verify_valid_refresh_token(self):
        """Test verification of valid refresh token"""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_refresh_token(data)
        
        payload = verify_token(token, "refresh")
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == "123"
        assert payload["type"] == "refresh"
    
    def test_verify_wrong_token_type(self):
        """Test verification with wrong token type"""
        data = {"sub": "test@example.com"}
        access_token = create_access_token(data)
        
        # Try to verify access token as refresh token
        payload = verify_token(access_token, "refresh")
        assert payload is None
    
    def test_verify_expired_token(self):
        """Test verification of expired token"""
        data = {"sub": "test@example.com"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta)
        
        payload = verify_token(token, "access")
        assert payload is None
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token"""
        invalid_token = "invalid.token.here"
        
        payload = verify_token(invalid_token, "access")
        assert payload is None
    
    def test_verify_token_with_wrong_secret(self):
        """Test verification with wrong secret"""
        data = {"sub": "test@example.com"}
        # Create token with different secret
        wrong_token = jwt.encode(data, "wrong-secret", algorithm=settings.algorithm)
        
        payload = verify_token(wrong_token, "access")
        assert payload is None


class TestUserAuthentication:
    """Test user authentication"""
    
    def test_authenticate_valid_user(self):
        """Test authentication with valid credentials"""
        email = "joao@exemplo.com"
        password = "123456"
        
        user = authenticate_user(email, password)
        assert user is not False
        assert user["email"] == email
        assert user["nome"] == "João Silva"
        assert user["ativo"] is True
        assert "user_id" in user
    
    def test_authenticate_invalid_email(self):
        """Test authentication with invalid email"""
        email = "nonexistent@example.com"
        password = "123456"
        
        user = authenticate_user(email, password)
        assert user is False
    
    def test_authenticate_invalid_password(self):
        """Test authentication with invalid password"""
        email = "joao@exemplo.com"
        password = "wrongpassword"
        
        user = authenticate_user(email, password)
        assert user is False


class TestRateLimiting:
    """Test authentication rate limiting"""
    
    def test_rate_limiter_initial_state(self):
        """Test rate limiter initial state"""
        identifier = "test-ip-1"
        assert auth_rate_limiter.is_rate_limited(identifier) is False
    
    def test_rate_limiter_under_limit(self):
        """Test rate limiter under limit"""
        identifier = "test-ip-2"
        
        # Record attempts under the limit
        for _ in range(4):
            auth_rate_limiter.record_attempt(identifier)
        
        assert auth_rate_limiter.is_rate_limited(identifier) is False
    
    def test_rate_limiter_over_limit(self):
        """Test rate limiter over limit"""
        identifier = "test-ip-3"
        
        # Record attempts over the limit
        for _ in range(6):
            auth_rate_limiter.record_attempt(identifier)
        
        assert auth_rate_limiter.is_rate_limited(identifier) is True
    
    def test_rate_limiter_different_identifiers(self):
        """Test rate limiter with different identifiers"""
        identifier1 = "test-ip-4"
        identifier2 = "test-ip-5"
        
        # Max out first identifier
        for _ in range(6):
            auth_rate_limiter.record_attempt(identifier1)
        
        # Second identifier should not be affected
        assert auth_rate_limiter.is_rate_limited(identifier1) is True
        assert auth_rate_limiter.is_rate_limited(identifier2) is False

