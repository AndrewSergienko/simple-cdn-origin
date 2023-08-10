from dataclasses import dataclass


@dataclass
class FileInfo:
    file_name: str
    origin_url: str


@dataclass
class Server:
    name: str
    ip: str
    zone: str


@dataclass
class FileStatus:
    duration: int
    time: int


@dataclass
class FileSavedStatus(FileStatus):
    file_info: FileInfo
    server: Server


@dataclass
class FileReplicatedStatus(FileStatus):
    file_info: FileInfo
    from_server: Server
    to_server: Server

