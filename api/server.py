"""
股票分析API服务器
提供REST API接口供Web界面调用
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import asyncio

# 添加项目路径到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 导入工作流
from src.graphs.graph import main_graph
from coze_coding_utils.runtime_ctx.context import new_context

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 静态文件服务
@app.route('/')
def index():
    """返回主页面"""
    return send_from_directory('assets', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """提供静态文件"""
    return send_from_directory('assets', path)


@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """
    股票分析API
    POST /api/analyze
    Body: {
        "user_input": "分析贵州茅台",
        "send_channel": "feishu",
        "email_recipients": ["user@example.com"]
    }
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data or 'user_input' not in data:
            return jsonify({
                'success': False,
                'error': '缺少user_input字段'
            }), 400
        
        user_input = data.get('user_input', '')
        send_channel = data.get('send_channel', 'feishu')
        email_recipients = data.get('email_recipients', [])
        
        # 准备输入数据
        input_data = {
            'user_input': user_input,
            'send_channel': send_channel,
            'email_recipients': email_recipients
        }
        
        # 调用工作流
        ctx = new_context(method="invoke")
        result = main_graph.invoke(input_data, context=ctx)
        
        # 返回结果
        return jsonify({
            'success': True,
            'result': result.get('result', ''),
            'details': {
                'intent': result.get('intent', ''),
                'stock_codes': result.get('stock_codes', []),
                'formatted_result': result.get('formatted_result', ''),
                'email_send_result': result.get('email_send_result', ''),
                'feishu_send_result': result.get('feishu_send_result', '')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'stock-analysis-api'
    })


@app.route('/api/stocks/search', methods=['GET'])
def search_stocks():
    """
    股票搜索API
    GET /api/stocks/search?q=茅台
    """
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': '请提供搜索关键词'
        }), 400
    
    # 股票数据库
    stock_database = [
        { 'code': '600519', 'name': '贵州茅台', 'pinyin': 'GZMT' },
        { 'code': '000858', 'name': '五粮液', 'pinyin': 'WLY' },
        { 'code': '600036', 'name': '招商银行', 'pinyin': 'ZSYH' },
        { 'code': '000001', 'name': '平安银行', 'pinyin': 'PAYH' },
        { 'code': '600276', 'name': '恒瑞医药', 'pinyin': 'HRYY' },
        { 'code': '000333', 'name': '美的集团', 'pinyin': 'MDJT' },
        { 'code': '600900', 'name': '长江电力', 'pinyin': 'CJDL' },
        { 'code': '601318', 'name': '中国平安', 'pinyin': 'ZGPA' },
        { 'code': '000063', 'name': '中兴通讯', 'pinyin': 'ZXTX' },
        { 'code': '600030', 'name': '中信证券', 'pinyin': 'ZXZQ' },
        { 'code': '601012', 'name': '隆基绿能', 'pinyin': 'LJLN' },
        { 'code': '300750', 'name': '宁德时代', 'pinyin': 'NDS D' },
        { 'code': '002415', 'name': '海康威视', 'pinyin': 'HKWS' },
        { 'code': '600050', 'name': '中国联通', 'pinyin': 'ZGLT' },
        { 'code': '000651', 'name': '格力电器', 'pinyin': 'GLDQ' },
        { 'code': '600887', 'name': '伊利股份', 'pinyin': 'YLGF' },
        { 'code': '601888', 'name': '中国中免', 'pinyin': 'ZGZM' },
        { 'code': '300015', 'name': '爱尔眼科', 'pinyin': 'AEYK' },
        { 'code': '002594', 'name': '比亚迪', 'pinyin': 'BYD' },
        { 'code': '600031', 'name': '三一重工', 'pinyin': 'SYZG' },
        { 'code': '000002', 'name': '万科A', 'pinyin': 'WK' },
        { 'code': '600048', 'name': '保利发展', 'pinyin': 'BLFZ' },
        { 'code': '601390', 'name': '中国中铁', 'pinyin': 'ZGZT' },
        { 'code': '601186', 'name': '中国铁建', 'pinyin': 'ZGTJ' },
        { 'code': '600585', 'name': '海螺水泥', 'pinyin': 'HLSN' },
        { 'code': '601899', 'name': '紫金矿业', 'pinyin': 'ZJKY' },
        { 'code': '000568', 'name': '泸州老窖', 'pinyin': 'LZLJ' },
        { 'code': '600809', 'name': '山西汾酒', 'pinyin': 'SXFJ' },
        { 'code': '603259', 'name': '药明康德', 'pinyin': 'YMKD' }
    ]
    
    lower_query = query.lower()
    results = [
        stock for stock in stock_database
        if query in stock['code'] or
           query in stock['name'] or
           lower_query in stock['pinyin'].lower() or
           lower_query in stock['pinyin'].lower().replace(' ', '')
    ]
    
    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
