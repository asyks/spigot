from asyncio import StreamReader, StreamWriter
from unittest.mock import AsyncMock, Mock, patch

import pytest

from spigot.connection import Connection


@pytest.mark.asyncio
@patch("spigot.connection.open_connection", return_type=AsyncMock)
class TestConnectionOpen:
    async def test_calls_asyncio_open_connection(
        self, mock_asyncio_open_connection: AsyncMock
    ) -> None:
        mock_asyncio_open_connection.return_value = (
            Mock(spec=StreamReader),
            Mock(spec=StreamWriter),
        )
        connection = Connection(hostname="foobar", port=80)

        await connection.open()

        assert mock_asyncio_open_connection.call_count == 1


@pytest.mark.asyncio
@patch("spigot.connection.open_connection", return_type=AsyncMock)
class TestConnectionSend:
    async def test_sends_str_data_and_collects_response(
        self,
        mock_asyncio_open_connection: AsyncMock,
    ) -> None:
        response_data = b"some arbirary response data"
        mock_stream_reader = AsyncMock(
            spec=StreamReader, readline=AsyncMock(side_effect=[response_data, ""])
        )

        mock_asyncio_open_connection.return_value = (
            mock_stream_reader,
            Mock(spec=StreamWriter),
        )
        connection = Connection(hostname="foobar", port=80)

        await connection.open()

        response = await connection.send(b"some arbitrary request data")

        assert response.content_bytes == response_data
