import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from datetime import datetime
from app.routers.games import get_games, get_game, create_game, update_game, delete_game
from app.models.game import Game
from app.models.user import User
from app.models.activity import Activity
from app.schemas.game_schema import GameCreate, GameUpdate, GameResponse
from beanie import PydanticObjectId, Link
from unittest.mock import Mock

@pytest.fixture
def sample_game_data():
    """Fixture for sample game data"""
    return {
        "id": "507f1f77bcf86cd799439011",
        "title": "Test Game",
        "creator": "507f1f77bcf86cd799439012",
        "activities": [],
        "target_range": [0, 10],
        "max_time_allowed": 60,
        "total_points": 100,
        "template": False
    }

@pytest.fixture
def sample_activity_data():
    """Fixture for sample activity data"""
    return {
        "id": "507f1f77bcf86cd799439013",
        "level": 1,
        "target": 10,
        "addends": [5, 5],
        "addends_size": 2,
        "time_limit": 30,
        "hints": ["Think about equal numbers"],
        "points": 10,
        "success_feedback": "Great job!",
        "failure_feedback": "Try again!"
    }

@pytest.fixture
def mock_user():
    """Fixture for mock user"""
    return User(
        id=PydanticObjectId("507f1f77bcf86cd799439012"),
        name="Test User",
        email="test@example.com",
        uid="test-uid",
        role="admin",
        created_at=datetime.now()
    )

@pytest.mark.asyncio
async def test_get_games_success(mocker, mock_user):
    """Test successful retrieval of all games"""
    # Create mock Link for creator
    creator_link = Mock(spec=Link)
    creator_link.id = mock_user.id
    creator_link.fetch = AsyncMock(return_value=mock_user)

    # Create mock game
    mock_game = Game(
        id="507f1f77bcf86cd799439011",
        title="Test Game",
        creator=creator_link,
        activities=[],
        target_range=[0, 10],
        max_time_allowed=60,
        total_points=100,
        template=False
    )

    # Mock Game.find_all().to_list()
    mock_find = mocker.patch('app.models.game.Game.find_all')
    mock_find.return_value.to_list = AsyncMock(return_value=[mock_game])

    # Call the function
    result = await get_games()

    # Assertions
    assert len(result) == 1
    assert result[0].title == "Test Game"
    assert result[0].creator == str(mock_user.id)
    mock_find.assert_called_once()

@pytest.mark.asyncio
async def test_get_game_success(mocker, mock_user, sample_game_data, sample_activity_data):
    """Test successful retrieval of single game"""
    # Create mock Link for creator
    creator_link = Mock(spec=Link)
    creator_link.id = PydanticObjectId("507f1f77bcf86cd799439012")
    creator_link.fetch = AsyncMock(return_value=mock_user)

    # Create mock activity
    mock_activity = Activity(
        id=PydanticObjectId("507f1f77bcf86cd799439013"),
        level=1,
        target=10,
        addends=[5, 5],
        addends_size=2,
        time_limit=30,
        hints=["Think about equal numbers"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Create activity link
    activity_link = Mock(spec=Link)
    activity_link.id = mock_activity.id
    activity_link.fetch = AsyncMock(return_value=mock_activity)

    # Mock Game methods with correct Link for activity
    mock_game = Game(
        id=PydanticObjectId("507f1f77bcf86cd799439011"),
        title="Test Game",
        creator=mock_user,  # This should be a Link too
        activities=[],  # Use Link instead of direct Activity
        target_range=[0, 10],
        max_time_allowed=60,
        total_points=100,
        template=False
    )

    # Create creator link
    creator_link = Mock(spec=Link)
    creator_link.id = mock_user.id
    creator_link.fetch = AsyncMock(return_value=mock_user)

    # Update mock_game creator
    mock_game.creator = creator_link

    # Mock validate_object_id and Game.get()
    game_id = "507f1f77bcf86cd799439011"
    mocker.patch('app.routers.games.validate_object_id', return_value=game_id)
    mock_get = mocker.patch('app.models.game.Game.get')
    mock_get.return_value = AsyncMock(return_value=mock_game)()

    # Call the function
    result = await get_game(game_id)

    # Assertions
    assert result.id == str(game_id)
    assert result.title == "Test Game"
    assert result.creator == str(creator_link.id)
    assert len(result.activities) == 1
    assert isinstance(result.activities[0], Activity)
    assert result.activities[0].id == str(mock_activity.id)
    assert result.target_range == [0, 10]
    assert result.max_time_allowed == 60
    assert result.total_points == 100
    assert result.template is False
    mock_get.assert_called_once_with(game_id)

@pytest.mark.asyncio
async def test_create_game_success(mocker, mock_user):
    """Test successful game creation"""
    creator_id = "507f1f77bcf86cd799439012"
    activity_id = "507f1f77bcf86cd799439013"

    creator_link = Mock(spec=Link)
    creator_link.id = PydanticObjectId(creator_id)
    creator_link.fetch = AsyncMock(return_value=mock_user)

    # Create game data
    game_data = GameCreate(
        title="New Game",
        creator_id=creator_id,
        activity_ids=[activity_id],
        template=False
    )

    # Create mock activity
    mock_activity = Activity(
        id=PydanticObjectId(activity_id),
        level=1,
        target=10,
        addends=[5, 5],
        addends_size=2,
        time_limit=30,
        hints=["Think about equal numbers"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Mock validations and database operations
    mocker.patch('app.routers.games.validate_object_id', return_value=creator_id)
    mock_get_user = mocker.patch('app.models.user.User.get')
    mock_get_user.return_value = mock_user

    mock_get_activity = mocker.patch('app.models.activity.Activity.get')
    mock_get_activity.return_value = mock_activity

    # Mock Game methods
    mock_game = Game(
        id="507f1f77bcf86cd799439011",
        title="Test Game",
        creator=creator_link,
        activities=[mock_activity],
        target_range=[0, 10],
        max_time_allowed=60,
        total_points=100,
        template=False
    )

    mock_insert = mocker.patch.object(Game, 'insert')
    mock_insert.return_value = None

    mock_update_stats = mocker.patch.object(Game, 'update_stats')
    mock_update_stats.return_value = None

    mock_save = mocker.patch.object(Game, 'save')
    mock_save.return_value = None

    # Create a mock for the new game instance
    mocker.patch('app.models.game.Game', return_value=mock_game)

    # Call the function
    result = await create_game(game_data)

    # Assertions
    assert result.title == game_data.title
    assert result.creator == creator_id
    assert len(result.activities) == 1
    assert isinstance(result.activities[0], Activity)
    assert result.activities[0].id == str(mock_activity.id)
    assert result.template is False

    # Verify method calls
    mock_get_user.assert_called_once_with(creator_id)
    mock_get_activity.assert_called_once_with(activity_id)
    mock_insert.assert_called_once()
    mock_update_stats.assert_called_once()
    mock_save.assert_called_once()

@pytest.mark.asyncio
async def test_update_game_success(mocker):
    """Test successful game update"""
    game_id = "507f1f77bcf86cd799439011"
    update_data = GameUpdate(
        title="Updated Game",
        activity_ids=["507f1f77bcf86cd799439013"],
        template=True
    )

    mock_game = Game(
        id=game_id,
        title="Old Title",
        creator=User(id="507f1f77bcf86cd799439012", name="Test User"),
        activities=[],
        template=False
    )

    # Mock validations and database operations
    mocker.patch('app.routers.games.validate_object_id', return_value=game_id)
    mock_get = mocker.patch('app.models.game.Game.get', return_value=mock_game)
    mock_save = mocker.patch.object(Game, 'save')

    # Call the function
    result = await update_game(game_id, update_data)

    # Assertions
    assert result.title == "Updated Game"
    assert result.template == True
    mock_get.assert_called_once_with(game_id)
    mock_save.assert_called_once()

@pytest.mark.asyncio
async def test_delete_game_success(mocker):
    """Test successful game deletion"""
    game_id = "507f1f77bcf86cd799439011"
    mock_game = Game(
        id=game_id,
        title="Test Game",
        creator=User(id="507f1f77bcf86cd799439012", name="Test User")
    )

    # Mock validations and database operations
    mocker.patch('app.routers.games.validate_object_id', return_value=game_id)
    mock_get = mocker.patch('app.models.game.Game.get', return_value=mock_game)
    mock_delete = mocker.patch.object(Game, 'delete')

    # Call the function
    result = await delete_game(game_id)

    # Assertions
    assert result["message"] == "Game deleted successfully"
    mock_get.assert_called_once_with(game_id)
    mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_get_game_not_found(mocker):
    """Test get game with non-existent ID"""
    game_id = "507f1f77bcf86cd799439011"
    
    # Mock validate_object_id and Game.get()
    mocker.patch('app.routers.games.validate_object_id', return_value=game_id)
    mock_get = mocker.patch('app.models.game.Game.get', return_value=None)

    # Test that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await get_game(game_id)
    
    assert exc_info.value.status_code == 404
    assert "Game not found" in str(exc_info.value.detail)