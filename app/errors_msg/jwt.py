from fastapi import HTTPException, status



ERROR_CREDENTIALS_JWT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Invalids Credentials",
    headers={"WWW-Authenticate":"Bearer"}
)