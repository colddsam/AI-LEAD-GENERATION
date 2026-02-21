import pytest
from unittest.mock import patch
from app.tasks.daily_pipeline import (
    run_discovery_task,
    run_qualification_task,
    run_personalization_task,
    run_outreach_send_task,
    run_daily_report_task,
    run_reply_polling_task
)

def test_run_discovery_task():
    with patch("app.tasks.daily_pipeline._do_discovery") as mock_step:
        run_discovery_task()
        assert mock_step.called

def test_run_qualification_task():
    with patch("app.tasks.daily_pipeline._do_qualification") as mock_step:
        run_qualification_task()
        assert mock_step.called

def test_run_personalization_task():
    with patch("app.tasks.daily_pipeline._do_personalization") as mock_step:
        run_personalization_task()
        assert mock_step.called

def test_run_outreach_send_task():
    with patch("app.tasks.daily_pipeline._do_outreach") as mock_step:
        run_outreach_send_task()
        assert mock_step.called

def test_run_daily_report_task():
    with patch("app.tasks.daily_pipeline._do_daily_report") as mock_step:
        run_daily_report_task()
        assert mock_step.called

def test_run_reply_polling_task():
    with patch("app.tasks.daily_pipeline._do_reply_polling") as mock_step:
        run_reply_polling_task()
        assert mock_step.called
