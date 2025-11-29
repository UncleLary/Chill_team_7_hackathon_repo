from models.user import User
from schemas.user import UserRead

def user_to_user_read(user : User) -> UserRead:
    user_dict = {
        'id' : user.id,
        'email' : user.email,
        'full_name' : user.full_name,
        'profile_picture_url' : user.profile_picture_url,
        'is_active' : user.is_active,
        'is_superuser' : user.is_superuser,
        'is_verified' : user.is_verified,
        'is_profile_complete' : user.is_profile_complete,
        'rec_date' : user.rec_date,
    }
    return UserRead.validate(user_dict)
