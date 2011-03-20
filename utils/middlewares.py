import re
from utils import get_stats
from django.template.loader import render_to_string as render_template

class StatsMiddleware(object):
    def process_response(self, request, response):
        path_info = request.META.get('PATH_INFO')
        if not request.is_ajax() and not re.findall(r'(ico|css|png|js|site_media)', path_info) and response.status_code == 200:
            stats_content = render_template('stats.html', {'stats':get_stats()})
            response.content = re.sub(r'<body>', '<body>%s' % stats_content, response.content)
        return response