#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import argparse
import datetime
import os

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONTENT_DIR = os.path.join(ROOT_DIR, 'content', 'post')

def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', default='My Post', help='blog title')
    parser.add_argument('-i', '--image', help='featured image')
    parser.add_argument('--tags', help='blog tags')

    return parser.parse_args()

def main(content_dir=CONTENT_DIR):
    args = check_args()
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%dT%H%M%S')
    # ファイル名をタイムスタンプで生成
    filepath = os.path.join(content_dir, f'{timestamp}.md')
    if os.path.exists(filepath):
        # 同一ファイル名が存在する場合は終了
        print(f'{filepath} is exists')
        return
    # フロントマターのメタ情報設定
    front_matter_map = {
        'title': f'"{args.title}"',
        'date': now.strftime('%Y-%m-%dT%H:%M:%S+09:00'),
    }
    # カバー写真の処理
    if args.image:
        front_matter_map.update({"featured_image": f'"{args.image}"'})
    # タグの処理
    if args.tags:
        front_matter_map.update({"tags": str(args.tags.split(','))})
    # 出力内容の生成
    output = '---\n'
    for k, v in front_matter_map.items():
        output += f'{k}: {v}\n'
    output += '---\n\n<!--more-->\n'
    # ファイルへの書き込み
    with open(filepath, 'w') as f:
        f.write(output)

    print(f'create {filepath}')

if __name__ == "__main__":
    main()
##### __main__.py ends here
