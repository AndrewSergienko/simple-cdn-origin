from src.abstract import AContext
from src.domain import FileInfo, FileStatus


async def subscribe_to_file_status(context: AContext, file: FileInfo, *args, **kwargs):
    """
    Subscribe the user to file status updates
    :param context: Context object
    :param file: file info
    """
    await context.sockets.subscribe_to_file_status(file, *args, **kwargs)


async def unsubscribe_to_file_status(
    context: AContext, file: FileInfo, *args, **kwargs
):
    """
    Unsubscribe the user to file status updates
    :param context: Context object
    :param file: file info
    """
    await context.sockets.unsubscribe_to_file_status(file, *args, **kwargs)


async def send_file_status(context: AContext, status: FileStatus):
    """
    Send a WebSocket message about the file status.
    :param context: Context object
    :param status: instance of a child class of the FileStatus
    """
    await context.sockets.send_file_status(status)
