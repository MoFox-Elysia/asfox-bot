@echo off
echo ========================================
echo 使用简化版工作流构建
echo ========================================
echo.

echo 问题分析：
echo 主工作流 (build-apk.yml) 有复杂的 Android SDK/NDK 配置
echo 简化版工作流 (build-apk-simple.yml) 让 Buildozer 自动处理
echo.

echo 解决方案：
echo 使用简化版工作流，避免手动配置错误
echo.

echo 步骤 1: 重命名工作流文件
if exist .github\workflows\build-apk.yml (
    ren .github\workflows\build-apk.yml build-apk-complex.yml
    echo 已将 build-apk.yml 重命名为 build-apk-complex.yml
)

if exist .github\workflows\build-apk-simple.yml (
    copy .github\workflows\build-apk-simple.yml .github\workflows\build-apk.yml
    echo 已将 build-apk-simple.yml 复制为 build-apk.yml
)

echo.
echo 步骤 2: 提交更改
git add .github/workflows/

echo.
set /p COMMIT_MSG="请输入提交信息（默认：使用简化版工作流）: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG="使用简化版工作流"

git commit -m "%COMMIT_MSG%

- 使用简化版工作流 (build-apk-simple.yml)
- 避免手动配置 Android SDK/NDK 的错误
- 让 Buildozer 自动处理依赖下载
- 更稳定可靠的构建流程"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: use_simple_workflow.bat ^<仓库URL^>
    echo.
    echo 示例: use_simple_workflow.bat https://github.com/username/repository.git
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
echo [成功] 配置已更新！
echo ========================================
echo.
echo 下一步操作：
echo 1. 访问 GitHub Actions 页面：
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 点击 "Build Android APK (Simple and Fast)"
echo 3. 点击 "Run workflow" 手动触发构建
echo.
echo 4. 等待构建完成（约 15-20 分钟）
echo.
echo 5. 下载生成的 APK 文件
echo.
echo 简化版工作流优势：
echo - 自动处理 Android SDK/NDK 下载
echo - 减少配置错误
echo - 包含 Cython 依赖
echo - 更稳定的构建流程
echo.
pause
exit /b 0
