@echo off
echo ========================================
echo 修复清理构建错误
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加修复的文件...
git add .github/workflows/build-apk.yml buildozer.spec

echo.
echo 创建提交...
git commit -m "Fix: Remove clean step that causes FileNotFoundError

- Removed 'buildozer android clean' step
- This step fails on first build when dependencies aren't downloaded yet
- Added cython to requirements for better compilation
- Build will now proceed directly to compilation"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_clean_error.bat ^<仓库URL^>
    echo.
    echo 示例: fix_clean_error.bat https://github.com/username/repository.git
    echo.
    pause
    exit /b 1
)

set REPO_URL=%1

echo 设置远程仓库...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo 远程仓库已存在，更新 URL...
    git remote set-url origin %REPO_URL%
)

echo.
echo 推送代码到 GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo [错误] 推送失败！
    echo ========================================
    echo.
    echo 如果遇到身份验证问题，请：
    echo 1. 创建 GitHub Personal Access Token
    echo    访问: https://github.com/settings/tokens
    echo 2. 使用以下命令手动推送：
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [成功] 修复已推送！
echo ========================================
echo.
echo 修复内容：
echo - 移除了导致 FileNotFoundError 的清理步骤
echo - 添加了 cython 到依赖列表
echo - 构建将直接开始编译，跳过清理
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 这次构建应该能够成功下载依赖并开始编译
echo 3. 首次构建需要 20-30 分钟
echo.
pause
