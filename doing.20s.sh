#!/bin/bash

# Doing
# BitBar plugin
#
# by Chris Metcalf <chris@chrismetcalf.net>
#
# Does shizit with Doing

if [[ `$HOME/bin/doing last` == *"@done"* ]]; then
  echo "💬";
else
  name=`$HOME/bin/doing last | tr -d '\n' | sed 's/ *(at.*//'`;
  start=`grep -o -m 1 "\d*-\d*-\d*\s\d*:\d*\s" $HOME/Dropbox/Notes/00_Doing.md`;
  date1=`date -j -f '%Y-%m-%d %H:%M ' "$start" +"%s"`;
  now=`date -j +"%s"`;
  diff=$(($now-$date1));
  echo "$name 🕗$(printf "%02d" $(($diff / 3600))):$(printf "%02d" $((($diff / 60) % 60)))"
fi
echo "---"
$HOME/bin/doing today | /usr/local/bin/gtac
