from src.abstract import AContext


async def subscribe_to_file_status(context: AContext, file_name, *args, **kwargs):
    """
    Subscribe the user to file status updates
    :param context: Context object
    :param file_name: file name
    """
    await context.sockets.subscribe_to_file_status(file_name, *args, **kwargs)


async def unsubscribe_to_file_status(context: AContext, file_name: str):
    """
    Unsubscribe the user to file status updates
    :param context: Context object
    :param file_name: file name
    """
    await context.sockets.unsubscribe_to_file_status(file_name)


async def send_file_status(context: AContext, status):
    """
    Send a WebSocket message about the file status.
    :param context: Context object
    :param status: dictionary status
    """
    await context.sockets.send_file_status(status)
