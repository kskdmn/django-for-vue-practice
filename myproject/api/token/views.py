from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_info(request):
    """
    Endpoint to retrieve information about the current user's token.
    """
    user = request.user

    token_data = {
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": user.date_joined.isoformat(),
    }

    return Response(token_data)
