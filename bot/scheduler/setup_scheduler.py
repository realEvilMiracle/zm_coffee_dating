import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from bot.scheduler.feedback import send_feedback_request, send_second_feedback_request
from bot.scheduler.matching import run_matching


def setup_scheduler(bot):
    env = os.getenv("ENV", "prod").lower()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    if env == "test":
        scheduler.add_job(
            run_matching,
            IntervalTrigger(minutes=2),
            args=[bot],
            id="test_matching",
            misfire_grace_time=None)
        scheduler.add_job(
            send_feedback_request,
            IntervalTrigger(minutes=3),
            args=[bot],
            id="test_feedback",
            misfire_grace_time=None)
        scheduler.add_job(
            send_second_feedback_request,
            IntervalTrigger(minutes=4),
            args=[bot],
            id="test_second_feedback",
            misfire_grace_time=None)
    else:
        scheduler.add_job(
            run_matching,
            CronTrigger(day_of_week="mon", hour=17, minute=0),
            args=[bot],
            id="weekly_matching",
            misfire_grace_time=None
        )

        scheduler.add_job(
            send_feedback_request,
            CronTrigger(day_of_week="thu", hour=17, minute=0),
            args=[bot],
            id="weekly_feedback",
            misfire_grace_time=None
        )

        scheduler.add_job(
            send_second_feedback_request,
            CronTrigger(day_of_week="fri", hour=17, minute=0),
            args=[bot],
            id="weekly_second_feedback",
            misfire_grace_time=None
        )

    scheduler.start()
