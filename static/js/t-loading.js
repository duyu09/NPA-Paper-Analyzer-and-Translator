/**
 * 全局加载遮罩控制函数 (单文件自包含版)
 * @param {boolean} show - true 显示，false 隐藏
 * @param {string} [text] - (可选) 加载提示文字，默认为 "正在解析..."
 * Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
 */
function toggleLoading(show, text = "正在解析...") {
    // 定义唯一的 ID，防止冲突
    const MASK_ID = '__u_loading_mask__';
    const STYLE_ID = '__u_loading_style__';

    // 1. 获取或创建 DOM 节点
    let mask = document.getElementById(MASK_ID);

    // 如果是要显示，且节点不存在，则进行初始化（注入 CSS 和 HTML）
    if (show && !mask) {
        // --- A. 动态注入 CSS ---
        if (!document.getElementById(STYLE_ID)) {
            const style = document.createElement('style');
            style.id = STYLE_ID;
            style.textContent = `
                #${MASK_ID} {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    z-index: 2147483647; /* Max Z-Index */
                    display: flex; flex-direction: column;
                    justify-content: center; align-items: center;
                    color: #fff; font-size: 14px; font-family: sans-serif;
                    user-select: none;
                }
                #${MASK_ID} ._u_spinner {
                    width: 30px; height: 30px; margin-bottom: 10px;
                    border: 3px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    border-top-color: #fff;
                    animation: _u_spin_anim 1s linear infinite;
                }
                @keyframes _u_spin_anim {
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }

        // --- B. 动态创建 HTML ---
        mask = document.createElement('div');
        mask.id = MASK_ID;
        mask.innerHTML = `<div class="_u_spinner"></div><div id="${MASK_ID}_text"></div>`;
        document.body.appendChild(mask);
    }

    // 2. 控制显示/隐藏逻辑
    if (mask) {
        if (show) {
            // 更新文字
            const textEl = document.getElementById(`${MASK_ID}_text`);
            if (textEl) textEl.innerText = text;
            mask.style.display = 'flex';
        } else {
            mask.style.display = 'none';
        }
    }
}