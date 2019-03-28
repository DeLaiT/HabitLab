from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
import json
import requests

from utils.config import CONFIG


class GitlabEvents(APIView):
    config = CONFIG.get_config()
    gitlab_habit = config['commit_habit']
    api_key = config['api_key']
    user_id = config['user_id']
    gitlab_username = config['gitlab_username']
    habit_url = 'https://habitica.com/api/v3/tasks/' + gitlab_habit + '/score/up'
    new_task_url = 'https://habitica.com/api/v3/tasks/user'

    def post(self, request):
        data = request.body.decode('utf-8')

        try:
            json_data = json.loads(data)
        except:
            return HttpResponse('invalid request body', status=status.HTTP_400_BAD_REQUEST)

        event = str(json_data['event_type'])

        if event == "push":
            username = str(json_data['user_username'])
            commits = json_data['total_commits_count']
            if username == self.gitlab_username:
                print("Updating habit " + str(commits) + " times up")
                for i in range(commits):
                    s = self.create_session()
                    r = s.post(self.habit_url)
                    print('[' + str(i) + ']' + str(r.status_code))
        elif event == 'issue':
            prev = json_data['changes']['assignees']['previous']
            current = json_data['changes']['assignees']['current']
            is_prev = False
            is_current = False
            close = json_data['object_attributes']['action'] == 'close'
            title = json_data['object_attributes']['title']
            desc = str(json_data['object_attributes']['description'])
            url = str(json_data['object_attributes']['url'])
            alias = str(json_data['object_attributes']['id'])

            for user in prev:
                if user['username'] == self.gitlab_username:
                    is_prev = True
                    break

            if not is_prev:
                for user in current:
                    if user['username'] == self.gitlab_username:
                        is_current = True
                        break

            if close and is_current:
                self.close_task(alias)
            elif not close and is_prev:
                self.delete_task(alias)
            elif not close and is_current:
                self.add_task(title, alias, desc + '\n' + url)

        return HttpResponse('VRGZ noob', status=status.HTTP_200_OK)

    def close_task(self, alias):
        s = self.create_session()
        r = s.post('https://habitica.com/api/v3/tasks/' + alias + '/score/up')
        print(str(r.status_code))
        s = self.create_session()
        r = s.delete('https://habitica.com/api/v3/tasks/' + alias)
        print(str(r.status_code))
        pass

    def delete_task(self, alias):
        s = self.create_session()
        r = s.delete('https://habitica.com/api/v3/tasks/' + alias)
        print(str(r.status_code))
        pass

    def add_task(self, title, alias, desc):
        print('creating task with title: ' + title)
        s = self.create_session()
        data = {
            'text': title,
            'type': "todo",
            'priority': 1.5,
            'alias': alias,
            'notes': desc
        }
        r = s.post(self.new_task_url, data=data)
        print(str(r.status_code))
        pass

    def create_session(self):
        s = requests.Session()
        s.headers.update({'x-api-key': self.api_key})
        s.headers.update({'x-api-user': self.user_id})
        return s
