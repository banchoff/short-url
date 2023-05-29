#!/bin/env bash
# Based on https://stackoverflow.com/questions/21306515/how-to-curl-an-authenticated-django-app
PORT="$1"
USER="$2"
PASS="$3"

LOGIN_URL="http://127.0.0.1:$PORT/shortener/login/"
TEST_URL="http://127.0.0.1:$PORT/shortener/about"
YOUR_USER="$USER"
YOUR_PASS="$PASS"
COOKIES=`mktemp`

CURL_BIN="curl -s -c $COOKIES -b $COOKIES -e $LOGIN_URL"

# echo -n "Django Auth: get csrftoken ..."
$CURL_BIN $LOGIN_URL > /dev/null
DJANGO_TOKEN="csrfmiddlewaretoken=$(grep csrftoken $COOKIES | sed 's/^.*csrftoken\s*//')"

# echo -n " perform login ..."
$CURL_BIN \
    -d "$DJANGO_TOKEN&username=$YOUR_USER&password=$YOUR_PASS" \
    -X POST $LOGIN_URL > /dev/null

#echo -n " do something while logged in ..."
$CURL_BIN \
    -d "$DJANGO_TOKEN&..." \
    -X GET $TEST_URL | grep About > /dev/null

RESULT="$?"
#echo " logout"
rm $COOKIES
exit $RESULT
