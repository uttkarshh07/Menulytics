from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class SearchRequest(BaseModel):
    restaurant_name: str