#!/usr/bin/env python3
"""
wrapper: запускает мигратор (migrations/*) вместо выполнения одиночного sql
"""
from scripts import migrate


if __name__ == "__main__":
    migrate.main()
