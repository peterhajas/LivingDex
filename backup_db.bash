#!/bin/bash

heroku pgbackups:capture
curl -o latest.dump `heroku pgbackups:url`
