from notificationapi_python_server_sdk import notificationapi

async def send_notification(user_id, email, number, comment, commentId):
    notificationapi.init(
        "xt3qwed47a8vfyqdztff1qg973",  # clientId
        "13izvwd9hda0txf2tkla7p9rklyrly8pcip88vrogn578nhi8rys7qxqrb" # clientSecret
    )

    await notificationapi.send({
        "notificationId": "trove",
        "user": {
        "id": email,
        "email": email,
        "number": number
        },
        "mergeTags": {
        "comment": comment,
        "commentId": commentId
        }
    })