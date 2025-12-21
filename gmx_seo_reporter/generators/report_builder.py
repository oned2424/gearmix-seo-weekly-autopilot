"""
Report Builder
HTMLレポートを生成するモジュール
"""

import os
from datetime import datetime
from typing import Dict, List

from jinja2 import Template


class GmxReportBuilder:
    """レポート構築クラス"""
    
    HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - {{ date }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meirio', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        header {
            border-bottom: 3px solid #2E86AB;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #2E86AB;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
        }
        
        .date {
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        h2 {
            color: #2E86AB;
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        
        h3 {
            color: #555;
            font-size: 1.3em;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        .summary {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #2E86AB;
        }
        
        .summary p {
            margin-bottom: 10px;
        }
        
        .graph {
            margin: 30px 0;
            text-align: center;
        }
        
        .graph img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #2E86AB;
            color: white;
            font-weight: bold;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .metric-positive {
            color: #06A77D;
            font-weight: bold;
        }
        
        .metric-negative {
            color: #C73E1D;
            font-weight: bold;
        }
        
        .metric-neutral {
            color: #666;
        }
        
        footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <div class="subtitle">{{ subtitle }}</div>
            <div class="date">レポート期間: {{ date }}</div>
        </header>
        
        <section class="summary">
            {{ executive_summary|safe }}
        </section>
        
        {% if graphs %}
        <section class="graphs">
            <h2>📊 グラフ</h2>
            {% for graph in graphs %}
            <div class="graph">
                <h3>{{ graph.title }}</h3>
                <img src="{{ graph.path }}" alt="{{ graph.title }}">
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if top_queries %}
        <section class="data-tables">
            <h2>🔍 トップ検索クエリ</h2>
            <table>
                <thead>
                    <tr>
                        <th>順位</th>
                        <th>検索クエリ</th>
                        <th>クリック数</th>
                        <th>表示回数</th>
                        <th>CTR</th>
                        <th>平均掲載順位</th>
                    </tr>
                </thead>
                <tbody>
                    {% for query in top_queries %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ query.query }}</td>
                        <td>{{ query.clicks|int }}</td>
                        <td>{{ query.impressions|int }}</td>
                        <td>{{ "%.2f"|format(query.ctr * 100) }}%</td>
                        <td>{{ "%.1f"|format(query.position) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% endif %}
        
        <footer>
            <p>Generated by GearMix SEO Weekly Autopilot</p>
            <p>© {{ year }} GearMix. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
    """
    
    def __init__(self, config: Dict = None):
        """
        初期化
        
        Args:
            config: レポート設定
        """
        self.config = config or {}
        self.template = Template(self.HTML_TEMPLATE)
    
    def build_report(
        self,
        executive_summary: str,
        graphs: List[Dict],
        top_queries: List[Dict],
        output_path: str,
        title: str = None,
        subtitle: str = None
    ) -> str:
        """
        HTMLレポートを構築
        
        Args:
            executive_summary: エグゼクティブサマリー(Markdown)
            graphs: グラフ情報のリスト [{'title': str, 'path': str}, ...]
            top_queries: トップクエリのリスト
            output_path: 出力パス
            title: レポートタイトル
            subtitle: サブタイトル
            
        Returns:
            str: 保存したファイルパス
        """
        # Markdownを簡易的にHTMLに変換
        executive_summary_html = self._markdown_to_html(executive_summary)
        
        # テンプレートに値を埋め込み
        html = self.template.render(
            title=title or self.config.get('title', 'GearMix週次SEOレポート'),
            subtitle=subtitle or self.config.get('subtitle', '検索パフォーマンス分析'),
            date=datetime.now().strftime('%Y年%m月%d日'),
            year=datetime.now().year,
            executive_summary=executive_summary_html,
            graphs=graphs,
            top_queries=top_queries
        )
        
        # ファイルに保存
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    @staticmethod
    def _markdown_to_html(markdown_text: str) -> str:
        """
        簡易的なMarkdown→HTML変換
        
        Args:
            markdown_text: Markdownテキスト
            
        Returns:
            str: HTMLテキスト
        """
        html = markdown_text
        
        # 見出し
        html = html.replace('# ', '<h2>').replace('\n\n', '</h2>\n\n')
        html = html.replace('## ', '<h3>').replace('\n\n', '</h3>\n\n')
        
        # 太字
        import re
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # 段落
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for p in paragraphs:
            if p.strip():
                if not p.strip().startswith('<h'):
                    html_paragraphs.append(f'<p>{p}</p>')
                else:
                    html_paragraphs.append(p)
        
        html = '\n'.join(html_paragraphs)
        
        # 改行
        html = html.replace('\n', '<br>\n')
        
        return html
