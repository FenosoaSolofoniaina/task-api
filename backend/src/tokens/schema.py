from pydantic import BaseModel, ConfigDict



# ================================================================================ #
# Login account
# ================================================================================ #
class TokenOut(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")
    
    access_token: str
    token_type: str =  "bearer"