from datetime import datetime
from unittest.mock import AsyncMock
from fastapi import HTTPException
import pytest
from app.routers.users import get_users, register_user , login_user
from app.models.user import User, UserRole 
from app.schemas.user_schema import UserCreate ,UserLogin

@pytest.mark.asyncio
async def test_get_users_success(mocker):
    """Test successful retrieval of all users"""
    # Mock data
    mock_users = [
        User(
            name="Test User 1",
            email="test1@example.com",
            uid="test-uid-1",
            role=UserRole.STUDENT,
            created_at=datetime.utcnow()
        ),
        User(
            name="Test User 2",
            email="test2@example.com",
            uid="test-uid-2",
            role=UserRole.EDUCATOR,
            created_at=datetime.utcnow()
        )
    ]
    
    # Mock User.find_all().to_list()
    mock_find = mocker.patch('app.models.user.User.find_all')
    mock_find.return_value.to_list = AsyncMock(return_value=mock_users)
    
    # Call the function
    result = await get_users()
    
    # Assertions
    assert len(result) == 2
    assert result[0].email == "test1@example.com"
    assert result[1].email == "test2@example.com"
    mock_find.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_success(mocker):
    """Test successful user registration"""
    # Mock data
    token_data = {"uid": "test-uid-1"}
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        role=UserRole.STUDENT
    )

    # Mock User.find_one() to return None (no existing user)
    mock_find_one = mocker.patch('app.models.user.User.find_one')
    mock_find_one.return_value = AsyncMock(return_value=None)()

    # Mock User.insert()
    mock_insert = mocker.patch('app.models.user.User.insert')
    mock_insert.return_value = AsyncMock()()

    # Call the function
    result = await register_user(user_data, token_data)

    # Assertions
    assert result.name == user_data.name
    assert result.email == user_data.email
    assert result.uid == token_data["uid"]
    assert result.role == user_data.role
    mock_find_one.assert_called_once_with({"email": user_data.email})
    mock_insert.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_duplicate_email(mocker):
    """Test registration with duplicate email"""
    # Mock data
    token_data = {"uid": "test-uid-1"}
    user_data = UserCreate(
        name="Test User",
        email="existing@example.com",
        role=UserRole.STUDENT
    )

    # Mock User.find_one() to return existing user
    existing_user = User(
        name="Existing User",
        email="existing@example.com",
        uid="existing-uid",
        role=UserRole.STUDENT,
        created_at=datetime.utcnow()
    )
    mock_find_one = mocker.patch('app.models.user.User.find_one')
    mock_find_one.return_value = AsyncMock(return_value=existing_user)()

    # Test that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await register_user(user_data, token_data)
    
    assert exc_info.value.status_code == 400
    assert "Email already registered" in str(exc_info.value.detail)
    mock_find_one.assert_called_once_with({"email": user_data.email})

@pytest.mark.asyncio
async def test_login_user_success(mocker):
    """Test successful user login"""
    # Mock data
    user_data = UserLogin(
        email="xyz@example.com",
        uid="test-uid-1"
    )

     # Mock User.find_one() to return existing user
    existing_user = User(
        name="Existing User",
        email="xyz@example.com",
        uid="test-uid-1",
        role=UserRole.STUDENT,
        created_at=datetime.utcnow()
    )

    token_data = {"uid": "test-uid-1"}
     # Mock User.find_one() to return None (no existing user)
    mock_find_one = mocker.patch('app.models.user.User.find_one')
    mock_find_one.return_value = AsyncMock(return_value=existing_user)()

    # Call the function
    result = await login_user(user_data, token_data)

    # Assertions
    assert result.email == user_data.email
    assert result.uid == token_data["uid"]
    mock_find_one.assert_called_once_with({"email": user_data.email, "uid": user_data.uid})

