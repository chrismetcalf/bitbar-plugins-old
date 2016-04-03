#!/bin/bash

# <bitbar.title>Homebrew Cask Updater</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Srdgh</bitbar.author>
# <bitbar.author.github>srdgh</bitbar.author.github>
# <bitbar.desc>List out-of-date apps i.e. apps for whch a newer Homebrew cask exists. Click menu item to install cask.</bitbar.desc>
# <bitbar.image>http://i.imgur.com/kBf90TB.png?1</bitbar.image>

#I've taken the next six lines from the brew update plugin.
exit_with_error() {
  echo "err | color=red";
  exit 1;
}

/usr/local/bin/brew update &> /dev/null || exit_with_error; 

brew_cask_list=$(/usr/local/bin/brew cask ls -1 | sed 's_(!)__g' | xargs /usr/local/bin/brew cask info | grep -A 1 'Not installed' | sed -e 's_Not installed__g' -e 's_https://github\.com/caskroom/homebrew-cask/blob/master/Casks/__g' -e 's_\.rb__g');
brew_cask_count=$(for line in $brew_cask_list; do echo "$line" | grep "[a-z]" ; done | wc -w | xargs);

brew_list=$(/usr/local/bin/brew outdated --verbose);
brew_count=$(echo "$UPDATES" | grep -c '[^[:space:]]');

total=`expr $brew_cask_count + $brew_count`

if [[ "${total}" != "0" ]]; then
  if [[ "${total}" == "1" ]]; then
    echo "🍺"
  else
    echo "🍻"
  fi
  echo "---"
  echo "$brew_count package(s) to update"
  echo "---"
  for line in $brew__list; do echo "$line" | grep "[a-z]" | sed 's_\(.*\)_Update & | bash=\"brew install &\" terminal=true refresh=_g' ; done
  echo "---"
  echo "$brew_cask_count cask(s) to update"
  echo "---"
  for line in $brew_cask_list; do echo "$line" | grep "[a-z]" | sed 's_\(.*\)_Update & | bash=\"brew cask install &\" terminal=true refresh=_g' ; done
  echo "---"
  echo "Refresh | refresh="
fi
