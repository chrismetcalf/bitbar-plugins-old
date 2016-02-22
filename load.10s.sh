#!/bin/bash

# Load Level
# BitBar plugin
#
# by Chris Metcalf <chris@chrismetcalf.net>
#
# Just displays the system load level

uptime | awk '{ print $9 }'
echo "---"
uptime
