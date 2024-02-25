


from collections import defaultdict
from itertools import chain
from django.db.models import Count
from easyaudit.models import RequestEvent, LoginEvent

def run():
    qs1 =RequestEvent.objects.filter(user_id=1).values('datetime__date').annotate(id_count=Count('id', distinct=True))
    qs2 = LoginEvent.objects.filter(user_id=1).values('datetime__date').annotate(count_login=Count('id', distinct=True))
    




    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    user_activity = list(collector.values())

    for c in user_activity:
        print(c)