# Tweet Catcher

[![Build Status](https://travis-ci.com/so07/TweetCatcher.svg?token=CFvNdbNXiYKX1TcDAvWp&branch=master)](https://travis-ci.com/so07/TweetCatcher)

## Install

```
git clone https://github.com/so07/TweetCatcher.git
cd TweetCatcher
pip install . -r requirements.txt
```

## Tweets Catcher

Download tweets with a pattern in a date range and save output as csv format in a directory

```
tweet_catcher --pattern MickJagger --from 2014-12-31T23:00:00 --to 2015-01-01T01:00:00 --output mick
```


## Tweets Cleaner


Clean tweets from duplicates and filter by language

```
tweet_cleaner --path mick --language en --output mick_clean --freq 1D
```


## Tweets Uniquer

Get only unique tweets from reference path

```
tweet_unique --path mick_unique --reference-path mick
```

