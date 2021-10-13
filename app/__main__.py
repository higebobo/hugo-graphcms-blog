# -*- mode: python -*- -*- coding: utf-8 -*-
import datetime
import json
import os
import pathlib
import re
import urllib.request

from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = pathlib.Path(APP_DIR).parent
HUGO_CONTENT_DIR = os.path.join(PROJECT_DIR, 'content')
HUGO_POST_DIRNAME = 'post'
UPDATE_SEC = int(os.getenv('UPDATE_SEC', '300'))

dotenv_path = os.path.join(PROJECT_DIR, '.env')
load_dotenv(dotenv_path)


class GraphcmsManager(object):
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.headers = {'Authorization': f'Bearer {token}'}

    def __format_query(self, s):
        s = re.sub(r'\s+', '' ' ', s).replace('\n', ' ')
        return {'query': f'{s}'}

    def __query_statement(self):
        return '''\
        {
          posts(locales: [ja, en], orderBy: updatedAt_DESC) {
            localizations(includeCurrent: true) {
              id
              title
              slug
              date
              eyecatch {
                url
              }
              body
              tag
              locale
              invalidLocale
              updatedAt
            }
          }
        }'''

    def query(self, data=None, is_raw=True):
        if not data:
            data = self.__query_statement()
        if is_raw:
            data = self.__format_query(data)

        req = urllib.request.Request(self.endpoint,
                                     data=json.dumps(data).encode(),
                                     headers=self.headers)
        status_code = 500
        try:
            with urllib.request.urlopen(req) as response:
                payload = json.loads(response.read())
                status_code = response.getcode()
        except urllib.error.HTTPError as e:
            payload = {'error': e.reason}
        except urllib.error.URLError as e:
            payload = {'error': e.reason}
        except Exception as e:
            payload = {'error': str(e)}
        return status_code, payload

    def __time_diff(self, date_str, fmt='%Y-%m-%dT%H:%M:%S.%f+00:00'):
        updatetime = datetime.datetime.strptime(date_str, fmt)
        return (datetime.datetime.now() - datetime.timedelta(hours=9) - updatetime).seconds

    def gen_hugo_contents(self, payload):
        result = list()

        data = (payload.get('data'))
        for model, content_list in data.items():
            for content in content_list:
                for x in content.get('localizations'):
                    data_map = dict()
                    locale = x['locale']
                    if locale == x.get('validLocale')
                        print(f'Pass language code {locale} for content {x["id"]}')
                        continue
                    front_matter = f'title: "{x["title"]}"\n'
                    front_matter += f'slug: "{x["slug"]}"\n'
                    front_matter += f'date: {x["date"]}\n'
                    eyecatch = x.get('eyecatch')
                    if eyecatch:
                        front_matter += f'featured_image: {eyecatch["url"]}\n'
                    tag = x.get('tag')
                    if tag:
                        front_matter += f'tags: {str(tag)}\n'

                    data_map['front_matter'] = front_matter
                    data_map['body'] = x['body']
                    data_map['filepath'] = f'{x["id"]}.md'
                    data_map['update_sec'] = self.__time_diff(x['updatedAt'])
                    data_map['locale'] = locale

                    result.append(data_map)

        return result

    def write(self, data, update_sec=UPDATE_SEC):
        for x in data:
            fullpath = os.path.join(HUGO_CONTENT_DIR, x['locale'],
                                    HUGO_POST_DIRNAME,  x['filepath'])
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)

            if os.path.exists(fullpath) and x["update_sec"] > update_sec:
                # skip old posts
                continue

            with open(fullpath, 'w') as f:
                text = f'---\n{x["front_matter"]}---\n{x["body"]}'
                f.write(text)


def main():
    endpoint = os.getenv('GRAPHCMS_ENDPOINT', 'http://localhost')
    token = os.getenv('GRAPHCMS_TOKEN', 'my-token')
    G = GraphcmsManager(endpoint=endpoint, token=token)
    status_code, payload = G.query()
    if status_code != 200:
        print(payload)
        return
    data = G.gen_hugo_contents(payload)
    G.write(data)


if __name__ == "__main__":
    main()
