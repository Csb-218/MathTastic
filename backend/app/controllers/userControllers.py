from app.models.user import User, UserRole


async def get_users():
    users = await User.find_all().to_list()
    return {"users": users}