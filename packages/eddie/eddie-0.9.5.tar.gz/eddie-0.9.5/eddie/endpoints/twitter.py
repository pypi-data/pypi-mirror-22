""" Twitter endpoint for a eddie bot, use this to connect your bot to
    Twitter.

    This module needs `tweepy` library.
"""

from __future__ import absolute_import
import json

import tweepy


class MyStreamListener(tweepy.StreamListener):
    """ This class will listen for `on_data` events on the twitter stream and
        then it will dispatch them to the endpoint.the
    """

    def set_endpoint(self, endpoint):
        """ Sets the endpoint instance to use when an event happens """
        self.endpoint = endpoint

    def on_data(self, raw_data):
        """ Called when data arrives this method dispatch the event
            to the right endpoint's method.
        """
        data = json.loads(raw_data)

        if 'direct_message' in data:
            direct_message = data['direct_message']
            if direct_message['sender']['id'] != self.endpoint._api.me().id:
                return self.endpoint.process_new_direct_message(direct_message)

        elif data.get('event', '') == 'follow':
            return self.endpoint.process_new_follower(data['source'])


class TwitterEndpoint(object):
    """ Twitter endpoint for a eddie bot.

        Example usage:

            >>> ep = TwitterEndpoint(
            ...     consumer_key='consumer_key',
            ...     consumer_secret='consumer_secret',
            ...     access_token='access_token',
            ...     access_token_secret='access_token_secret'
            ... )
            >>> bot.add_endpoint(ep)
            >>> bot.run()

    """

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret,):
        self._bot = None
        self._last_processed_dm = 0
        self._polling_should_run = False
        self._polling_is_running = False

        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self._auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(self._auth)

        self._stream = None

    def set_bot(self, bot):
        """ Sets the main bot, the bot must be an instance of
            `eddie.bot.Bot`.

            TwitterEndpoint will use the bot to know how to behave.
        """
        self._bot = bot

    def run(self):
        """Starts the polling for new DMs."""

        self.check_new_followers()

        self._polling_should_run = True
        self.start_polling()

    def stop(self):
        """Make the polling for new DMs stop."""

        self._polling_should_run = False
        self._stream.disconnect()

    def start_polling(self):
        """ Strats an infinite loop to see if there are new events.

            The loop ends when the `self._polling_should_run` will be false
            (set `True` by `self.run` and `False` by `self.stop`)
        """

        stream_listener = MyStreamListener()
        stream_listener.set_endpoint(self)
        self._stream = tweepy.Stream(
            auth=self._api.auth,
            listener=stream_listener
        )

        self._stream.userstream(async=True)

        self._polling_is_running = True

    def process_new_direct_message(self, direct_message):
        """ Method called for each new DMs arrived.
        """

        if direct_message['id'] > self._last_processed_dm:
            response = self._bot.process(in_message=direct_message['text'])

            self._api.send_direct_message(
                text=response,
                user_id=direct_message['sender']['id']
            )

            self._last_processed_dm = direct_message['id']

        return True

    def process_new_follower(self, user):
        """ Follow the user if it isn't already followed.
            This method should be called at startup for all the followers and
            when a new user follow us.
        """
        already_friends = self._api.friends_ids()
        if user['id'] not in already_friends:
            self._api.create_friendship(user_id=user['id'])

            self._api.send_direct_message(
                text=self._bot.start(),
                user_id=user['id']
            )

        return True

    def check_new_followers(self):
        """ For each follower (not friend) process it (follow and start bot).
        """
        [
            self.process_new_follower({'id': uid})
            for uid in self._api.followers_ids()
        ]
