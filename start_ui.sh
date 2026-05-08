#!/usr/bin/env bash
docker run --rm -v "$HOME/data:/data" -v "$PWD/hiddencostreport/.env:/hiddencostreport/.env" hiddencostreport:latest ui

