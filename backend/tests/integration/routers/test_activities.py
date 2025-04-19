import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.routers.activities import get_activities, get_activity, create_activity, update_activity, delete_activity
from app.models.activity import Activity
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate, ActivityResponse

@pytest.fixture
def sample_activity_data():
    """Fixture for sample activity data"""
    return {
        "level": 1,
        "target": 10,
        "addends": [5, 5],
        "addends_size": 2,
        "time_limit": 60,
        "hints": ["Think about equal numbers"],
        "points": 10,
        "success_feedback": "Great job!",
        "failure_feedback": "Try again!"
    }

@pytest.mark.asyncio
async def test_get_activities_success(mocker):
    """Test successful retrieval of all activities"""
    # Mock data
    mock_activities = [
        Activity(**{
            "id": "507f1f77bcf86cd799439011",
            "level": 1,
            "target": 10,
            "addends": [5, 5],
            "addends_size": 2,
            "time_limit": 60,
            "hints": ["Think about equal numbers"],
            "points": 10,
            "success_feedback": "Great job!",
            "failure_feedback": "Try again!"
        })
    ]

    # Mock Activity.find_all().to_list()
    mock_find = mocker.patch('app.models.activity.Activity.find_all')
    mock_find.return_value.to_list = AsyncMock(return_value=mock_activities)

    # Call the function
    result = await get_activities()

    # Assertions
    assert len(result) == 1
    assert result[0].target == 10
    assert result[0].level == 1
    mock_find.assert_called_once()

@pytest.mark.asyncio
async def test_get_activity_success(mocker):
    """Test successful retrieval of single activity"""
    activity_id = "507f1f77bcf86cd799439011"
    mock_activity = Activity(**{
        "id": activity_id,
        "level": 1,
        "target": 10,
        "addends": [5, 5],
        "addends_size": 2,
        "time_limit": 60,
        "hints": ["Think about equal numbers"],
        "points": 10,
        "success_feedback": "Great job!",
        "failure_feedback": "Try again!"
    })

    # Mock validate_object_id
    mocker.patch('app.routers.activities.validate_object_id', return_value=activity_id)

    # Mock Activity.get()
    mock_get = mocker.patch('app.models.activity.Activity.get')
    mock_get.return_value = mock_activity  # Remove AsyncMock wrapper

    # Call the function
    result = await get_activity(activity_id)

    # Assertions
    assert result.id == activity_id
    assert result.target == 10
    assert result.level == 1
    mock_get.assert_called_once_with(activity_id)

@pytest.mark.asyncio
async def test_create_activity_success(mocker):
    """Test successful activity creation"""
    
    # Create activity data using ActivityCreate schema
    activity_data = ActivityCreate(
        level=1,
        target=10,
        addends=[5, 5],
        addends_size=2,
        time_limit=60,
        hints=["Think about equal numbers"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Mock Activity.insert()
    mock_insert = mocker.patch.object(Activity, 'insert')
    mock_insert.return_value = AsyncMock()()

    # Call the function
    result = await create_activity(activity_data)

    # Assertions
    assert result.target == activity_data.target
    assert result.level == activity_data.level
    assert result.addends == activity_data.addends
    mock_insert.assert_called_once()

@pytest.mark.asyncio
async def test_update_activity_success(mocker):
    """Test successful activity update"""
    activity_id = "507f1f77bcf86cd799439011"
    # Create update data
    update_data = ActivityUpdate(
        level=1,
        target=15,
        addends=[7, 8],
        addends_size=2,
        time_limit=60,
        hints=["Think about pairs that add up to 15"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Create mock activity
    mock_activity = Activity(
        id=activity_id,
        level=1,
        target=15,
        addends=[7, 8],
        addends_size=2,
        time_limit=60,
        hints=["Think about pairs that add up to 15"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Mock validate_object_id
    mocker.patch('app.routers.activities.validate_object_id', return_value=activity_id)

    # Mock Activity.get()
    mock_get = mocker.patch('app.models.activity.Activity.get')
    mock_get.return_value = mock_activity

    # Mock Activity.update()
    mock_update = mocker.patch.object(Activity, 'update', new_callable=AsyncMock)

    # Call the function
    result = await update_activity(activity_id, update_data)

    # Assertions
    assert result.level == update_data.level
    assert result.target == update_data.target
    assert result.addends == update_data.addends
    # mock_get.assert_called_once()
    mock_update.assert_called_once()

@pytest.mark.asyncio
async def test_delete_activity_success(mocker):
    """Test successful activity deletion"""
    activity_id = "507f1f77bcf86cd799439011"
    
    mock_activity = Activity(
        id=activity_id,
        level=1,
        target=10,
        addends=[5, 5],
        addends_size=2,
        time_limit=60,
        hints=["Think about equal numbers"],
        points=10,
        success_feedback="Great job!",
        failure_feedback="Try again!"
    )

    # Mock validate_object_id
    mocker.patch('app.routers.activities.validate_object_id', return_value=activity_id)

    # Mock Activity.get()
    mock_get = mocker.patch('app.models.activity.Activity.get')
    mock_get.return_value = mock_activity

    # Mock Document.delete method
    mock_delete = mocker.patch.object(Activity, 'delete', new_callable=AsyncMock)

    # Call the function
    result = await delete_activity(activity_id)

    # Assertions
    assert result["message"] == "Activity deleted successfully"
    mock_get.assert_called_once_with(activity_id)
    mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_get_activity_not_found(mocker):
    """Test get activity with non-existent ID"""
    activity_id = "507f1f77bcf86cd799439011"
    
    # Mock validate_object_id
    mocker.patch('app.routers.activities.validate_object_id', return_value=activity_id)

    # Mock Activity.get() to return None
    mock_get = mocker.patch('app.models.activity.Activity.get')
    mock_get.return_value = None

    # Test that it raises HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await get_activity(activity_id)
    
    assert exc_info.value.status_code == 404
    assert "Activity not found" in str(exc_info.value.detail)
    mock_get.assert_called_once_with(activity_id)