#!/bin/sh
alembic upgrade head
exec python bot/main.py
