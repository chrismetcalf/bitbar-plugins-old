#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>TravisCI Check</bitbar.title>
# <bitbar.version>v1.1</bitbar.version>
# <bitbar.author>Chris Tomkins-Tinch</bitbar.author>
# <bitbar.author.github>tomkinsc</bitbar.author.github>
# <bitbar.desc>This plugin displays the build status of repositories listed on TravisCI.</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/53064/12126193/a775fada-b3bd-11e5-9ae2-091c9c38b1da.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

# Chris Tomkins-Tinch
# github.com/tomkinsc

# Keith Cirkel
# github.com/keithamus

# version history
# 1.0
#   initial commit
# 1.1
#   refactor by @keithamus to remove travispy dependency

# Dependencies:
#   travis API key

import json
import urllib2
import os

# You need to set your TRAVIS_KEY to an API key for travis.
# -- Please note that this IS NOT the 'Token' listed on the Travis CI website
# -- Again, this is NOT the token on https://travis-ci.org/profile/your-name
# The easiest way to get this key is to use the official travis client
# (`gem install travis`), and run `travis_token`.
TRAVIS_KEY = os.getenv( 'TRAVIS_KEY', 'TOKENGOESHERE' )

# If you don't want to check all repos, then specify the ones you do wish to
# check here, and this plugin will only get the details of these repos.
# If you do not specify the `repos_to_check` option - it will fetch all repos
# available in your account.
# If you do not include the 'branches' key, then only the master branch
# will be checked.
# repos_to_check = [
#         {'name':'socrata/dev.socrata.com', 'branches' : 'gh-pages'},
# ]

# If you set INCLUDE_PULL_REQUESTS to `True`, then this script will get the
# status of both pull requests and commits. By default, it only gets the status
# of commits (pushes).
INCLUDE_PULL_REQUESTS = True

# SUPER SECRET FEATURE!
# Instead of listing the repos you want to check in an array above, you can
# use a hidden feature of Travis v3 - stars. Repositories can be starred,
# and if SECRET_FILTER_BY_STAR is set to `True` then this script will only
# show the starred repositories.
# How do you star a repository? As of writing Travis has no UI for it (check
# their roadmap (http://next.travis-ci.com/) to see when it might be
# implemented). The only way to star a repository right now, is to curl the
# v3 api, like so:
# curl -X POST https://api.travis-ci.org/repo/ACCOUNT%2FREPO/star -H "Accept: application/vnd.travis-ci.3+json" -H "Authorization: token YOUR_TOKEN"
# (Pay particular attention to the headers, and replace
# ACCOUNT, REPO and YOUR_TOKEN as necessary)
SECRET_FILTER_BY_STAR = False

# You may need to change the TRAVIS_URL if you're using travis enterprise or
# private travis. For private travis, change the .org to .com
TRAVIS_URL = 'http://api.travis-ci.org/'

# ======================================

SYMBOLS = {
    'passed': u'✔︎',
    'failed': u'✘',
    'errored': u'⚠',
    'cancelled': u' ⃠',
}
COLORS = {
    'passed': 'green',
    'failed': 'red',
    'errored': 'yellow',
    'cancelled': 'grey',
}
NO_SYMBOL = u'❂'


def request(uri):
    request = urllib2.Request(TRAVIS_URL + uri, headers={
        'Authorization': 'token ' + TRAVIS_KEY,
        'Accept': 'application/vnd.travis-ci.3+json'
    })
    response = urllib2.urlopen(request)
    return json.load(response)


def get_all_repos_for_account():
    url = 'repos?repository.active=true&sort_by=name&limit=200'
    if SECRET_FILTER_BY_STAR:
        url += '&starred=true'
    repos = request(url)
    all_repos = []
    for repo in repos['repositories']:
        if repo and 'slug' in repo:
            all_repos.append({'name': repo['slug']})

    return all_repos


def update_statuses(repos):
    output = []
    fail_count = 0

    output.append(u'{} | color=green'.format(SYMBOLS['passed']))
    output.append('---')

    for repo in repos:
        if 'branches' in repo and len(repo['branches']):
            branch_list = repo['branches']
        else:
            branch_list = ['master']

        for branch_name in branch_list:
            url = 'repo/' + urllib2.quote(repo['name'], safe='') + '/builds?limit=1&branch.name=' + branch_name
            if not INCLUDE_PULL_REQUESTS:
                url += '&event_type=push'
            build = request(url)
            if 'builds' in build and len(build['builds']):
                build = build['builds'][0]
                color = 'color={}'.format(COLORS[build['state']]) if COLORS[build['state']] else ''
                symbol = SYMBOLS[build['state']] or NO_SYMBOL
                href = 'href=https://travis-ci.org/{}/builds/{}'.format(repo['name'], build['id'])
                output_msg = u'{symbol} {repo_name} ({branch_name}) {status}'.format(symbol=symbol, repo_name=repo['name'], branch_name=branch_name, status=build['state'])
                output.append(u'{} | {} {}'.format(output_msg, href, color))

                if build['state'] != "passed":
                    fail_count += 1

    if fail_count > 0:
        output[0] = u'{}{} | color=red'.format(SYMBOLS['failed'], fail_count)

    for line in output:
        print line.encode('utf-8')


if __name__ == '__main__':
    try:
        repos_to_check
    except NameError:
        repos_to_check = get_all_repos_for_account()

    update_statuses(repos_to_check)
