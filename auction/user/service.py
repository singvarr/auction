from auction.user.models import User


class UserService:
    def get_details_for_notifications(self, user: User):
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": user.avatar.path,
        }
