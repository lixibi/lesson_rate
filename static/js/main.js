// 主要JavaScript功能
document.addEventListener('DOMContentLoaded', function() {
    // 表单提交处理
    const surveyForm = document.getElementById('surveyForm');
    if (surveyForm) {
        surveyForm.addEventListener('submit', function(e) {
            // 表单已有默认值，直接提交
            const submitBtn = surveyForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                showSubmitLoading(submitBtn);
            }
        });
    }

    // 选项卡片点击效果
    const optionCards = document.querySelectorAll('.option-card');
    optionCards.forEach(card => {
        card.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                updateCardSelection(radio);
            }
        });
    });

    // 监听单选按钮变化
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            updateCardSelection(this);
        });
    });

    // 自动保存功能（可选）
    const textarea = document.querySelector('textarea[name="suggestions"]');
    if (textarea) {
        textarea.addEventListener('input', function() {
            localStorage.setItem('survey_suggestions', this.value);
        });

        // 恢复保存的内容
        const savedSuggestions = localStorage.getItem('survey_suggestions');
        if (savedSuggestions) {
            textarea.value = savedSuggestions;
        }
    }

    // 初始化默认选择
    initializeDefaultSelections();

    // 页面加载动画
    animateElements();
});

// 初始化默认选中状态
function initializeDefaultSelections() {
    // 确保默认选项被正确标记为选中状态
    const defaultSelections = [
        'input[name="content_preparation"][value="准备充分"]',
        'input[name="practical_relevance"][value="非常好"]',
        'input[name="overall_score"][value="10"]'
    ];

    defaultSelections.forEach(selector => {
        const input = document.querySelector(selector);
        if (input && !document.querySelector(`input[name="${input.name}"]:checked`)) {
            input.checked = true;
            updateCardSelection(input);
        }
    });
}

// 更新卡片选择状态
function updateCardSelection(radio) {
    const name = radio.name;
    const cards = document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
        const card = r.closest('.option-card');
        if (card) {
            card.classList.remove('selected');
        }
    });

    const selectedCard = radio.closest('.option-card');
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
}

// 显示警告信息
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('main.container');
    container.insertBefore(alertDiv, container.firstChild);

    // 自动消失
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 页面元素动画
function animateElements() {
    const elements = document.querySelectorAll('.course-card, .question-group');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';

        setTimeout(() => {
            element.style.transition = 'all 0.6s ease-out';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// 提交表单时的加载效果
function showSubmitLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>提交中...';
    button.disabled = true;

    // 清除本地存储的建议
    localStorage.removeItem('survey_suggestions');

    return originalText;
}

// 平滑滚动到顶部
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 检测移动设备
function isMobile() {
    return window.innerWidth <= 768;
}

// 优化移动端体验
if (isMobile()) {
    document.body.classList.add('mobile-device');

    // 移动端特殊处理
    const cards = document.querySelectorAll('.option-card');
    cards.forEach(card => {
        card.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });

        card.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
}
