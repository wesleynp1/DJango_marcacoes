#!/bin/sh

daphne -b 0.0.0.0 -p 8000 wnp_exe.asgi:application