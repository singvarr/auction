import os
import pusher

pusher_client = pusher.Pusher(
    app_id=os.environ["PUSHER_APP_ID"],
    key=os.environ["PUSHER_APP_KEY"],
    secret=os.environ["PUSHER_SECRET_KEY"],
    cluster=os.environ["PUSHER_CLUSTER"],
)
