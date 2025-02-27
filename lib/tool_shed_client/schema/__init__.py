from typing import (
    List,
    Union,
)

from pydantic import BaseModel


class Repository(BaseModel):
    id: str
    name: str
    owner: str


class Category(BaseModel):
    id: str
    name: str


class ValidRepostiroyUpdateMessage(BaseModel):
    message: str


class FailedRepositoryUpdateMessage(BaseModel):
    err_msg: str


class GetOrderedInstallableRevisionsRequest(BaseModel):
    name: str
    owner: str


class OrderedInstallableRevisions(BaseModel):
    __root__: List[str]


class RepositoryUpdate(BaseModel):
    __root__: Union[ValidRepostiroyUpdateMessage, FailedRepositoryUpdateMessage]

    @property
    def is_ok(self):
        return isinstance(self.__root__, ValidRepostiroyUpdateMessage)


class ResetMetadataOnRepositoryRequest(BaseModel):
    repository_id: str


class ResetMetadataOnRepositoryResponse(BaseModel):
    status: str  # TODO: enum...
    repository_status: List[str]
    start_time: str
    stop_time: str
