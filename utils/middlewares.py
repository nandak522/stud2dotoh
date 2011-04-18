import re
from django.template.loader import render_to_string as render_template
from users.models import College, Group, Company

class StatsMiddleware(object):
    def process_response(self, request, response):
        path_info = request.META.get('PATH_INFO')
        if not request.is_ajax() and not re.findall(r'(ico|css|png|js|site_media)', path_info) and response.status_code == 200:
            stats_content = render_template('stats.html', {'stats':get_stats()})
            response.content = re.sub(r'<body>', '<body>%s' % stats_content, response.content)
        return response
    
def get_stats():
    stats = {'colleges_count':College.objects.count(),
             'students_count':Group.objects.get(name='Student').user_set.count(),
             'companies_count':Company.objects.count(),
             'employees_count':Group.objects.get(name='Employee').user_set.count()}
    return stats