import asyncio

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


async def servers_ping_to_host(context: AContext, host: str) -> dict[str, float]:
    """
    Getting ping for each server to the host.

    :param context: Context object
    :param host: host domain
    :return: ping time in seconds
    """
    servers = await context.servers.get_servers(context.ROOT_DIR)
    tasks = [
        context.web.get_ping_to_host(f"http://{server['ip']}", host)
        for server in servers
    ]
    servers_ping = {}
    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            servers_ping[result["url"]] = result["ping"]
    return servers_ping


async def send_download_link(context: AContext, url: str, link: str) -> dict:
    """
    Sending a request to download the file and returning the response.

    :param context: Context instance
    :param url: server url
    :param link: link to file
    :return: downloaded file info
    """
    return await context.web.send_download_link(url, link)
