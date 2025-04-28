from fastapi import APIRouter, Depends, status
from modules.user.dto import (
    CreateUserRequest,
    CreateUserResponse,
    ListUsersResponse,
    SigninUserRequest,
    SigninUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
)
from modules.user.application.create_customer_use_case import (
    CreateUserInput,
    CreateUserUseCase,
)
from modules.user.application.list_users_use_case import (
    ListUsersOutput,
    ListUsersUseCase,
)
from modules.user.application.signin_user_use_case import (
    SigninUserInput,
    SigninUserUseCase,
)
from modules.user.application.update_user_use_case import (
    UpdateUserInput,
    UpdateUserUseCase,
)
from modules.user.providers import UserModuleProviders


user_router = APIRouter(prefix="/api/v1/user", tags=["User"])


@user_router.get(
    "/",
    response_model=list[ListUsersResponse],
    summary="List all users",
    description="Retrieve a list of all registered users in the system",
    status_code=status.HTTP_200_OK,
    response_description="List of users successfully retrieved",
)
async def list_users(
    use_case: ListUsersUseCase = Depends(
        UserModuleProviders.use_cases.get_list_users_use_case
    ),
) -> list[ListUsersResponse]:
    """
    Retrieve a list of all users.

    Returns:
        list[ListUsersResponse]: A list of user data objects
    """
    users: list[ListUsersOutput] = await use_case.handle()
    return [
        ListUsersResponse(
            id=user.id,
            name=user.name,
            email=user.email,
        )
        for user in users
    ]


@user_router.post(
    "/",
    response_model=CreateUserResponse,
    summary="Create a new user",
    description="Register a new user in the system with name, email and password",
    status_code=status.HTTP_201_CREATED,
    response_description="User successfully created",
)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(
        UserModuleProviders.use_cases.get_create_user_use_case
    ),
):
    """
    Create a new user.

    Args:
        request (CreateUserRequest): The user data for registration

    Returns:
        CreateUserResponse: The created user data
    """
    input = CreateUserInput(
        name=request.name,
        email=request.email,
        password=request.password,
    )
    user = await use_case.handle(input)
    return user


@user_router.put(
    "/{user_id}",
    response_model=UpdateUserResponse,
    summary="Update a user",
    description="Update an existing user's information by user ID",
    status_code=status.HTTP_200_OK,
    response_description="User successfully updated",
)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    use_case: UpdateUserUseCase = Depends(
        UserModuleProviders.use_cases.get_update_user_use_case
    ),
):
    """
    Update an existing user.

    Args:
        user_id (str): The ID of the user to update
        request (UpdateUserRequest): The user data to update

    Returns:
        UpdateUserResponse: The updated user data
    """
    input = UpdateUserInput(
        id=user_id,
        name=request.name,
        email=request.email,
    )
    user = await use_case.handle(input)
    return user


@user_router.post(
    "/signin",
    response_model=SigninUserResponse,
    tags=["Auth"],
    summary="Authenticate a user",
    description="Authenticate a user with email and password and return a token",
    status_code=status.HTTP_200_OK,
    response_description="User successfully authenticated",
)
async def sign_in_user(
    request: SigninUserRequest,
    use_case: SigninUserUseCase = Depends(
        UserModuleProviders.use_cases.get_signin_user_use_case
    ),
):
    """
    Authenticate a user and return an access token.

    Args:
        request (SigninUserRequest): The user credentials for authentication

    Returns:
        SigninUserResponse: The authentication token
    """
    input = SigninUserInput(
        email=request.email,
        password=request.password,
    )
    user = await use_case.handle(input)
    return SigninUserResponse(
        token=user.token,
    )
