# -*- mode: python -*- -*- coding: utf-8 -*-
import json
import os
import pathlib
import re
import urllib.request

from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = pathlib.Path(APP_DIR).parent
HUGO_CONTENT_DIR = os.path.join(PROJECT_DIR, 'content', 'post')

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
          posts {
            id
            title
            slug
            date
            eyecatch {
              url
            }
            body
            tag
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

    def gen_hugo_contents(self, payload):
        result = list()

        data = (payload.get('data'))
        for model, content_list in data.items():
            for x in content_list:
                data_map = dict()
                front_matter = f'title: "{x["title"]}"\n'
                front_matter = f'slug: "{x["slug"]}"\n'
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

                result.append(data_map)
        return result

    def write(self, data):
        for x in data:
            fullpath = os.path.join(HUGO_CONTENT_DIR, x['filepath'])
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)

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
