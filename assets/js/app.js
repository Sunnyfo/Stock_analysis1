// 智能股票分析系统 - JavaScript 交互逻辑

// 全局状态
let selectedStock = null;
let emailRecipients = [];
let defaultEmails = [];
let stockDatabase = [];

// 股票数据库（示例数据）
function initStockDatabase() {
    stockDatabase = [
        { code: '600519', name: '贵州茅台', pinyin: 'GZMT' },
        { code: '000858', name: '五粮液', pinyin: 'WLY' },
        { code: '600036', name: '招商银行', pinyin: 'ZSYH' },
        { code: '000001', name: '平安银行', pinyin: 'PAYH' },
        { code: '600276', name: '恒瑞医药', pinyin: 'HRYY' },
        { code: '000333', name: '美的集团', pinyin: 'MDJT' },
        { code: '600900', name: '长江电力', pinyin: 'CJDL' },
        { code: '601318', name: '中国平安', pinyin: 'ZGPA' },
        { code: '000063', name: '中兴通讯', pinyin: 'ZXTX' },
        { code: '600030', name: '中信证券', pinyin: 'ZXZQ' },
        { code: '601012', name: '隆基绿能', pinyin: 'LJLN' },
        { code: '300750', name: '宁德时代', pinyin: 'NDS D' },
        { code: '002415', name: '海康威视', pinyin: 'HKWS' },
        { code: '600050', name: '中国联通', pinyin: 'ZGLT' },
        { code: '000651', name: '格力电器', pinyin: 'GLDQ' },
        { code: '600887', name: '伊利股份', pinyin: 'YLGF' },
        { code: '601888', name: '中国中免', pinyin: 'ZGZM' },
        { code: '300015', name: '爱尔眼科', pinyin: 'AEYK' },
        { code: '002594', name: '比亚迪', pinyin: 'BYD' },
        { code: '600031', name: '三一重工', pinyin: 'SYZG' },
        { code: '000002', name: '万科A', pinyin: 'WK' },
        { code: '600048', name: '保利发展', pinyin: 'BLFZ' },
        { code: '601390', name: '中国中铁', pinyin: 'ZGZT' },
        { code: '601186', name: '中国铁建', pinyin: 'ZGTJ' },
        { code: '600585', name: '海螺水泥', pinyin: 'HLSN' },
        { code: '601899', name: '紫金矿业', pinyin: 'ZJKY' },
        { code: '000568', name: '泸州老窖', pinyin: 'LZLJ' },
        { code: '600809', name: '山西汾酒', pinyin: 'SXFJ' },
        { code: '603259', name: '药明康德', pinyin: 'YMKD' }
    ];
    
    // 从localStorage加载保存的数据
    loadSavedData();
}

// 加载保存的数据
function loadSavedData() {
    const savedEmails = localStorage.getItem('defaultEmails');
    if (savedEmails) {
        defaultEmails = JSON.parse(savedEmails);
        renderDefaultEmailList();
    }
}

// 保存数据到localStorage
function saveData() {
    localStorage.setItem('defaultEmails', JSON.stringify(defaultEmails));
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initStockDatabase();
    initTabSwitch();
    initStockSearch();
    initEmailManagement();
    initButtons();
    initChannelToggle();
});

// 选项卡切换
function initTabSwitch() {
    const tabs = document.querySelectorAll('.tab-btn');
    const panels = document.querySelectorAll('.tab-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // 移除所有active类
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            
            // 添加active类
            this.classList.add('active');
            document.getElementById(targetTab + '-panel').classList.add('active');
        });
    });
}

// 股票搜索功能
function initStockSearch() {
    const searchInput = document.getElementById('stock-search');
    const searchResults = document.getElementById('search-results');
    const searchBtn = document.getElementById('search-btn');
    let searchTimeout = null;
    
    // 搜索函数 - 使用API
    async function searchStocks(query) {
        if (!query) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        // 防抖处理
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/api/stocks/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (data.success && data.results.length > 0) {
                    searchResults.innerHTML = data.results.map(stock => `
                        <div class="search-result-item" data-code="${stock.code}" data-name="${stock.name}">
                            <span class="search-result-code">${stock.code}</span>
                            <span class="search-result-name">${stock.name}</span>
                            <span class="search-result-pinyin">${stock.pinyin}</span>
                        </div>
                    `).join('');
                } else {
                    searchResults.innerHTML = '<div class="search-result-item">未找到匹配的股票</div>';
                }
                
                searchResults.style.display = 'block';
            } catch (error) {
                // API调用失败时，使用本地数据
                console.warn('API搜索失败，使用本地数据:', error);
                searchStocksLocal(query);
            }
        }, 300); // 300ms防抖
    }
    
    // 本地搜索（备用）
    function searchStocksLocal(query) {
        const lowerQuery = query.toLowerCase();
        const results = stockDatabase.filter(stock => {
            return query in stock['code'] ||
                   query in stock['name'] ||
                   lowerQuery in stock['pinyin'].lower() ||
                   lowerQuery in stock['pinyin'].lower().replace(' ', '')
        });
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item">未找到匹配的股票</div>';
        } else {
            searchResults.innerHTML = results.map(stock => `
                <div class="search-result-item" data-code="${stock.code}" data-name="${stock.name}">
                    <span class="search-result-code">${stock.code}</span>
                    <span class="search-result-name">${stock.name}</span>
                    <span class="search-result-pinyin">${stock.pinyin}</span>
                </div>
            `).join('');
        }
        
        searchResults.style.display = 'block';
    }
    
    // 搜索输入事件
    searchInput.addEventListener('input', function() {
        searchStocks(this.value);
    });
    
    // 搜索按钮点击
    searchBtn.addEventListener('click', function() {
        searchStocks(searchInput.value);
    });
    
    // 选择股票
    searchResults.addEventListener('click', function(e) {
        const resultItem = e.target.closest('.search-result-item');
        if (resultItem) {
            selectStock(
                resultItem.getAttribute('data-code'),
                resultItem.getAttribute('data-name')
            );
            searchInput.value = '';
            searchResults.style.display = 'none';
        }
    });
    
    // 点击外部关闭搜索结果
    document.addEventListener('click', function(e) {
        if (!searchBox.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

const searchBox = document.querySelector('.search-box');

// 选择股票
function selectStock(code, name) {
    selectedStock = { code, name };
    document.getElementById('stock-code-display').textContent = code;
    document.getElementById('stock-name-display').textContent = name;
    document.getElementById('selected-stock').style.display = 'block';
}

// 清除已选股票
function initButtons() {
    document.getElementById('clear-stock').addEventListener('click', function() {
        selectedStock = null;
        document.getElementById('selected-stock').style.display = 'none';
    });
    
    document.getElementById('diagnose-btn').addEventListener('click', function() {
        handleDiagnosis();
    });
    
    document.getElementById('select-btn').addEventListener('click', function() {
        handleStockSelection();
    });
    
    document.getElementById('save-settings').addEventListener('click', function() {
        saveSettings();
    });
    
    document.getElementById('close-result').addEventListener('click', function() {
        document.getElementById('result-panel').style.display = 'none';
    });
}

// 邮箱管理
function initEmailManagement() {
    // 诊股面板邮箱管理
    initEmailInput('email-input', 'add-email', 'email-list', emailRecipients);
    
    // 选股面板邮箱管理
    const selectionEmailRecipients = [];
    initEmailInput('selection-email-input', 'selection-add-email', 'selection-email-list', selectionEmailRecipients);
    
    // 设置面板默认邮箱管理
    initEmailInput('default-email-input', 'add-default-email', 'default-email-list', defaultEmails);
}

function initEmailInput(inputId, btnId, listId, array) {
    const input = document.getElementById(inputId);
    const btn = document.getElementById(btnId);
    const list = document.getElementById(listId);
    
    function addEmail() {
        const email = input.value.trim();
        if (email && isValidEmail(email) && !array.includes(email)) {
            array.push(email);
            renderEmailList(list, array);
            input.value = '';
        } else if (array.includes(email)) {
            alert('该邮箱已存在');
        } else {
            alert('请输入有效的邮箱地址');
        }
    }
    
    btn.addEventListener('click', addEmail);
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            addEmail();
        }
    });
    
    // 渲染邮箱列表
    list.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-email')) {
            const email = e.target.getAttribute('data-email');
            const index = array.indexOf(email);
            if (index > -1) {
                array.splice(index, 1);
                renderEmailList(list, array);
            }
        }
    });
}

function renderEmailList(listElement, array) {
    listElement.innerHTML = array.map(email => `
        <div class="email-tag">
            ${email}
            <span class="remove-email" data-email="${email}">×</span>
        </div>
    `).join('');
}

function renderDefaultEmailList() {
    renderEmailList(document.getElementById('default-email-list'), defaultEmails);
}

// 验证邮箱格式
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 渠道切换
function initChannelToggle() {
    // 诊股面板
    const channelRadios = document.querySelectorAll('input[name="channel"]');
    const emailRecipientsDiv = document.getElementById('email-recipients');
    
    channelRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'email' || this.value === 'both') {
                emailRecipientsDiv.style.display = 'block';
            } else {
                emailRecipientsDiv.style.display = 'none';
            }
        });
    });
    
    // 选股面板
    const selectionChannelRadios = document.querySelectorAll('input[name="selection-channel"]');
    const selectionEmailRecipientsDiv = document.getElementById('selection-email-recipients');
    
    selectionChannelRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'email' || this.value === 'both') {
                selectionEmailRecipientsDiv.style.display = 'block';
            } else {
                selectionEmailRecipientsDiv.style.display = 'none';
            }
        });
    });
}

// 处理诊股
function handleDiagnosis() {
    if (!selectedStock) {
        alert('请先选择要诊断的股票');
        return;
    }
    
    const channel = document.querySelector('input[name="channel"]:checked').value;
    const recipients = emailRecipients.length > 0 ? emailRecipients : defaultEmails;
    
    const userData = {
        user_input: `分析一下${selectedStock.name}(${selectedStock.code})的投资价值`,
        send_channel: channel,
        email_recipients: recipients
    };
    
    submitAnalysis(userData);
}

// 处理选股
function handleStockSelection() {
    const conditions = buildSelectionConditions();
    
    if (!conditions) {
        return;
    }
    
    const channel = document.querySelector('input[name="selection-channel"]:checked').value;
    const recipients = Array.from(document.querySelectorAll('#selection-email-list .email-tag'))
        .map(tag => tag.textContent.replace('×', '').trim());
    
    const userData = {
        user_input: conditions,
        send_channel: channel,
        email_recipients: recipients.length > 0 ? recipients : defaultEmails
    };
    
    submitAnalysis(userData);
}

// 构建选股条件
function buildSelectionConditions() {
    let conditions = [];
    
    const industry = document.getElementById('industry-select').value;
    if (industry) {
        conditions.push(`行业：${industry}`);
    }
    
    const minMarketCap = document.getElementById('min-market-cap').value;
    const maxMarketCap = document.getElementById('max-market-cap').value;
    if (minMarketCap || maxMarketCap) {
        const capRange = `${minMarketCap || '0'}-${maxMarketCap || '不限'}亿`;
        conditions.push(`市值范围：${capRange}`);
    }
    
    const minPE = document.getElementById('min-pe').value;
    const maxPE = document.getElementById('max-pe').value;
    if (minPE || maxPE) {
        const peRange = `${minPE || '0'}-${maxPE || '不限'}`;
        conditions.push(`市盈率范围：${peRange}`);
    }
    
    const kline = document.querySelector('input[name="kline"]:checked').value;
    const klineText = kline === 'daily' ? '日线' : kline === 'weekly' ? '周线' : '月线';
    conditions.push(`K线周期：${klineText}`);
    
    const technicalIndicators = [];
    if (document.getElementById('check-macd').checked) technicalIndicators.push('MACD金叉');
    if (document.getElementById('check-rsi').checked) technicalIndicators.push('RSI超卖');
    if (document.getElementById('check-volume').checked) technicalIndicators.push('放量上涨');
    if (document.getElementById('check-breakout').checked) technicalIndicators.push('突破阻力');
    
    if (technicalIndicators.length > 0) {
        conditions.push(`技术指标：${technicalIndicators.join('、')}`);
    }
    
    const otherConditions = document.getElementById('other-conditions').value.trim();
    if (otherConditions) {
        conditions.push(`其他条件：${otherConditions}`);
    }
    
    if (conditions.length === 0) {
        alert('请至少选择一个选股条件');
        return null;
    }
    
    return `请推荐符合以下条件的股票：${conditions.join('，')}`;
}

// 提交分析
async function submitAnalysis(userData) {
    // 显示加载中
    document.getElementById('loading-overlay').style.display = 'flex';
    
    try {
        // 调用实际API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        document.getElementById('loading-overlay').style.display = 'none';
        
        if (data.success) {
            // 显示成功结果
            let resultText = `分析已完成！\n\n`;
            resultText += `用户输入：${userData.user_input}\n`;
            resultText += `发送渠道：${userData.send_channel}\n`;
            resultText += `收件人：${userData.email_recipients.join(', ') || '无'}\n\n`;
            
            if (data.details.formatted_result) {
                resultText += `=== 分析报告 ===\n${data.details.formatted_result}\n\n`;
            }
            
            resultText += `=== 发送状态 ===\n`;
            if (data.details.email_send_result) {
                resultText += `${data.details.email_send_result}\n`;
            }
            if (data.details.feishu_send_result) {
                resultText += `${data.details.feishu_send_result}\n`;
            }
            
            resultText += `\n总体状态：${data.result}`;
            
            document.getElementById('result-content').textContent = resultText;
            document.getElementById('result-panel').style.display = 'block';
        } else {
            // 显示错误
            alert(`分析失败：${data.error}`);
        }
        
    } catch (error) {
        document.getElementById('loading-overlay').style.display = 'none';
        alert(`请求失败：${error.message}\n\n请确保API服务器正在运行。`);
        console.error('API调用错误:', error);
    }
}

// 保存设置
function saveSettings() {
    saveData();
    alert('设置已保存');
}
