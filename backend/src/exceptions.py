from typing import Any
from fastapi import HTTPException



class APIException(HTTPException):
    """ """
    
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        type: str,
    ) -> None:
        
        self.error_response: dict[str, Any] = {
            "success": False,
            "response": None,
            "error": {
                "type": type,
                "code": code,
                "message": message,
            },
        }

        super().__init__(
            status_code=status_code,
            detail=self.error_response,
        )



class RequestHeaderException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="REQUEST_HEADER_ERROR"
        )


class RessourceNotFoundException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="RESSOURCE_ERROR"
        )



class DataBaseException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="DATABASE_ERROR"
        )


class DataValueException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="VALUE_ERROR"
        )



class ClientBehaviourException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="CLIENT_ERROR"
        )



class CredentialsException(APIException) :
    """ """


    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None :
        """ """

        super().__init__(
            status_code=status_code,
            code=code,
            message=message,
            type="CREDENTIAL_ERROR"
        )