from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth
from socialregistration.settings import SESSION_KEY
import urlparse

class Twitter(OAuth):
    api_key = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    auth_url = 'https://api.twitter.com/oauth/authenticate'
    
    info_url = 'https://api.twitter.com/1/account/verify_credentials.json'

    def get_callback_url(self, **kwargs):
        if self.is_https():
            return urlparse.urljoin(
                'https://%s' % Site.objects.get_current().domain,
                reverse('socialregistration:twitter:callback'))
        return urlparse.urljoin(
            'http://%s' % Site.objects.get_current().domain,
            reverse('socialregistration:twitter:callback'))
    
    def get_user_info(self):
        return self.request(self.info_url)

    @staticmethod
    def get_session_key():
        return '%stwitter' % SESSION_KEY

