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
    file_info: FileInfo
    duration: int
    time: int


@dataclass
class FileSavedStatus(FileStatus):
    server: Server


@dataclass
class FileReplicatedStatus(FileStatus):
    from_server: Server
    to_server: Server
