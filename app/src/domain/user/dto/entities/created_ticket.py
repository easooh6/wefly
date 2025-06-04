from pydantic import BaseModel

class CreatedTicketDTO(BaseModel):
    id: int
    user_id: int
    status: bool = True