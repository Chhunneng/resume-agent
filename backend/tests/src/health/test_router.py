"""Unit tests for health check router."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import status
from fastapi.responses import JSONResponse
from pytest_mock import MockerFixture

from src.health.constants import DatabaseStatus, HealthStatus
from src.health.router import health_check, health_check_detailed
from src.health.schemas import HealthStatusResponse


@pytest.mark.unit
class TestHealthCheck:
    """Test health_check function."""

    @pytest.mark.asyncio
    async def test_returns_health_status_response(self, mocker: MockerFixture) -> None:
        """Test that function returns HealthStatusResponse."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        result = await health_check()

        assert isinstance(result, HealthStatusResponse)

    @pytest.mark.asyncio
    async def test_returns_healthy_status(self, mocker: MockerFixture) -> None:
        """Test that function returns healthy status."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        result = await health_check()

        assert result.status == HealthStatus.HEALTHY

    @pytest.mark.asyncio
    async def test_returns_correct_version(self, mocker: MockerFixture) -> None:
        """Test that function returns correct version."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        result = await health_check()

        assert result.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_uses_current_datetime(self, mocker: MockerFixture) -> None:
        """Test that function uses get_current_utc_datetime."""
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mock_get_datetime = mocker.patch(
            "src.health.router.get_current_utc_datetime",
            return_value=mock_datetime,
        )

        await health_check()

        mock_get_datetime.assert_called_once()

    @pytest.mark.asyncio
    async def test_sets_timestamp_from_datetime(self, mocker: MockerFixture) -> None:
        """Test that timestamp is set from get_current_utc_datetime."""
        mock_datetime = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        result = await health_check()

        assert result.timestamp == mock_datetime


@pytest.mark.unit
class TestHealthCheckDetailed:
    """Test health_check_detailed function."""

    @pytest.mark.asyncio
    async def test_returns_json_response(self, mocker: MockerFixture) -> None:
        """Test that function returns JSONResponse."""
        self._setup_mocks_for_connected_db(mocker)

        result = await health_check_detailed()

        assert isinstance(result, JSONResponse)

    @pytest.mark.asyncio
    async def test_returns_200_when_database_connected(self, mocker: MockerFixture) -> None:
        """Test that function returns 200 status when database is connected."""
        self._setup_mocks_for_connected_db(mocker)

        result = await health_check_detailed()

        assert result.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_returns_503_when_database_disconnected(self, mocker: MockerFixture) -> None:
        """Test that function returns 503 status when database is disconnected."""
        self._setup_mocks_for_disconnected_db(mocker)

        result = await health_check_detailed()

        assert result.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

    @pytest.mark.asyncio
    async def test_sets_healthy_status_when_database_connected(self, mocker: MockerFixture) -> None:
        """Test that function sets healthy status when database is connected."""
        self._setup_mocks_for_connected_db(mocker)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"status":"healthy"' in content

    @pytest.mark.asyncio
    async def test_sets_unhealthy_status_when_database_disconnected(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Test that function sets unhealthy status when database is disconnected."""
        self._setup_mocks_for_disconnected_db(mocker)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"status":"unhealthy"' in content

    @pytest.mark.asyncio
    async def test_sets_database_connected_when_db_available(self, mocker: MockerFixture) -> None:
        """Test that function sets database status to connected when available."""
        self._setup_mocks_for_connected_db(mocker)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"database":"connected"' in content

    @pytest.mark.asyncio
    async def test_sets_database_disconnected_when_db_unavailable(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Test that function sets database status to disconnected when unavailable."""
        self._setup_mocks_for_disconnected_db(mocker)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"database":"disconnected"' in content

    @pytest.mark.asyncio
    async def test_calculates_uptime_correctly(self, mocker: MockerFixture) -> None:
        """Test that function calculates uptime correctly."""
        mock_start_time = 1000.0
        mock_current_time = 1360.5  # 360.5 seconds later
        mocker.patch("src.health.router.APP_START_TIME", mock_start_time)
        mocker.patch("time.time", return_value=mock_current_time)
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        # Mock database connection
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=AsyncMock())
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)
        mocker.patch("src.health.router.engine", mock_engine)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"uptime_seconds":360.5' in content

    @pytest.mark.asyncio
    async def test_rounds_uptime_to_two_decimals(self, mocker: MockerFixture) -> None:
        """Test that function rounds uptime to two decimal places."""
        mock_start_time = 1000.0
        mock_current_time = 1360.555555  # Should round to 360.56
        mocker.patch("src.health.router.APP_START_TIME", mock_start_time)
        mocker.patch("time.time", return_value=mock_current_time)
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        # Mock database connection
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=AsyncMock())
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)
        mocker.patch("src.health.router.engine", mock_engine)

        result = await health_check_detailed()
        content = result.body.decode()
        assert '"uptime_seconds":360.56' in content

    @pytest.mark.asyncio
    async def test_uses_current_datetime_for_timestamp(self, mocker: MockerFixture) -> None:
        """Test that function uses get_current_utc_datetime for timestamp."""
        mock_datetime = datetime(2024, 1, 1, 12, 30, 45, tzinfo=UTC)
        mock_get_datetime = mocker.patch(
            "src.health.router.get_current_utc_datetime",
            return_value=mock_datetime,
        )
        self._setup_mocks_for_connected_db(mocker, skip_datetime=True)

        await health_check_detailed()

        mock_get_datetime.assert_called_once()

    @pytest.mark.asyncio
    async def test_checks_database_connection(self, mocker: MockerFixture) -> None:
        """Test that function checks database connection."""
        mock_conn = AsyncMock()
        mock_execute = AsyncMock()
        mock_conn.execute = mock_execute
        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=AsyncMock())
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)
        mocker.patch("src.health.router.engine", mock_engine)
        mocker.patch("time.time", return_value=1000.0)
        mocker.patch("src.health.router.APP_START_TIME", 1000.0)
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

        await health_check_detailed()

        mock_execute.assert_called_once()

    def _setup_mocks_for_connected_db(
        self,
        mocker: MockerFixture,
        skip_datetime: bool = False,
    ) -> None:
        """Helper method to set up mocks for connected database scenario."""
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=AsyncMock())
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)
        mocker.patch("src.health.router.engine", mock_engine)
        mocker.patch("time.time", return_value=1000.0)
        mocker.patch("src.health.router.APP_START_TIME", 1000.0)
        if not skip_datetime:
            mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

    def _setup_mocks_for_disconnected_db(self, mocker: MockerFixture) -> None:
        """Helper method to set up mocks for disconnected database scenario."""
        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(side_effect=Exception("Database connection failed"))
        mocker.patch("src.health.router.engine", mock_engine)
        mocker.patch("time.time", return_value=1000.0)
        mocker.patch("src.health.router.APP_START_TIME", 1000.0)
        mock_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        mocker.patch("src.health.router.get_current_utc_datetime", return_value=mock_datetime)

