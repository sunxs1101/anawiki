#!/bin/bash

ps axu | grep concept_extract | awk '{print $2}' | grep -v "grep" | xargs kill -9
