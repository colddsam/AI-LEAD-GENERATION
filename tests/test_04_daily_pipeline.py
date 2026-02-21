import pytest
from unittest.mock import patch, MagicMock
from app.tasks.daily_pipeline import (
    run_discovery_task,
    run_qualification_task,
    run_personalization_task,
    run_outreach_send_task,
    run_daily_report_task,
    _mock_pipeline_step
)

@pytest.mark.asyncio
async def test_mock_pipeline_step():
    with patch("app.tasks.daily_pipeline.send_telegram_alert") as mock_alert:
        await _mock_pipeline_step("Test Step")
        mock_alert.assert_called_once_with("🚀 Running Pipeline Step: Test Step")

def test_run_discovery_task():
    with patch("app.tasks.daily_pipeline._mock_pipeline_step") as mock_step:
        run_discovery_task()
        # Note: Since it uses run_async, we are just mocking the inner call here
        assert mock_step.called

def test_run_qualification_task():
    with patch("app.tasks.daily_pipeline._mock_pipeline_step") as mock_step:
        run_qualification_task()
        assert mock_step.called

def test_run_personalization_task():
    with patch("app.tasks.daily_pipeline._mock_pipeline_step") as mock_step:
        run_personalization_task()
        assert mock_step.called

def test_run_outreach_send_task():
    with patch("app.tasks.daily_pipeline._mock_pipeline_step") as mock_step:
        run_outreach_send_task()
        assert mock_step.called

def test_run_daily_report_task():
    with patch("app.tasks.daily_pipeline._mock_pipeline_step") as mock_step:
        run_daily_report_task()
        assert mock_step.called
