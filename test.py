import unittest
import bookmarks, chartGenerator, tweetFetcher
import coinbase.wallet.error
import os

class TestTweets(unittest.TestCase):
    #string over 128-character limit for Tweets
    tooLongString = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'

    def testConnectToEndpoint(self):
        with self.assertRaises(tweetFetcher.requests.exceptions.MissingSchema):
            tweetFetcher.connectToEndpoint('')
        with self.assertRaises(tweetFetcher.requests.exceptions.InvalidURL):
            tweetFetcher.connectToEndpoint('https://')
        with self.assertRaises(Exception):
            tweetFetcher.connectToEndpoint('https://api.twitter.com')

    def testTweetCount(self):
        self.assertIsInstance(tweetFetcher.tweetCount('all'),int)

        with self.assertRaises(Exception):
            tweetFetcher.tweetCount('')
            tweetFetcher.tweetCount('#')
            tweetFetcher.tweetCount(tooLongString)

    def testLatestTweet(self):
        self.assertIsInstance(tweetFetcher.recentTweet('all'),str)

        with self.assertRaises(Exception):
            tweetFetcher.recentTweet('')
            tweetFetcher.recentTweet('#')
            tweetFetcher.recentTweet(tooLongString)

class TestChart(unittest.TestCase):
    def testGenerateChart(self):
        with self.assertRaises(coinbase.wallet.error.NotFoundError):
            chartGenerator.generateChart(1)
            chartGenerator.generateChart('1')

        self.assertFalse(os.path.exists('chart.png'))
        self.assertFalse(os.path.exists('chart.svg'))
        chartGenerator.generateChart('BTC')
        self.assertTrue(os.path.exists('chart.png'))
        self.assertTrue(os.path.exists('chart.svg'))
        os.remove('chart.png')
        os.remove('chart.svg')
        self.assertFalse(os.path.exists('chart.png'))
        self.assertFalse(os.path.exists('chart.svg'))

class TestBookmarks(unittest.TestCase):
    b1 = bookmarks(1) #sample user ID; impossible for any user to have this ID as Discord IDs are 18 characters

    def testConstructor(self):
        with self.assertRaises(TypeError):
            b2 = bookmarks()

    def testAddBookmark(self):
        assertEqual(b1.addBookmark('a'),'currency added successfully')
        assertEqual(b1.addBookmark('a'),"can't add as already in bookmarks")

    def testRemoveBookmark(self):
        assertEqual(b1.removeBookmark('a'),'successfully removed from bookmarks')
        assertEqual(b1.removeBookmark('a'),'unable to find currency to remove')

    def testGetBookmarks(self):
        assertEqual(b1.getBookmark(),[])
