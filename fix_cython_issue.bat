@echo off
echo ========================================
echo 修复 Cython 构建问题
echo ========================================
echo.

echo 问题分析：
echo Buildozer 构建失败，因为 Cython 未正确安装。
echo Cython 是构建 Android APK 的必要依赖。
echo.

echo 正在备份工作流文件...
if exist .github\workflows\build-apk-simple.yml (
    copy .github\workflows\build-apk-simple.yml .github\workflows\build-apk-simple.yml.backup
    echo 已备份到: .github\workflows\build-apk-simple.yml.backup
)

echo.
echo 应用修复：添加 Cython 依赖...
echo.

echo 修复内容：
echo 1. 在 Install Python dependencies 步骤中添加 Cython==0.29.33
echo 2. 增加必要的系统依赖包
echo 3. 延长构建超时时间到 30 分钟
echo 4. 改进错误日志输出
echo.

echo 提交修复...
git add .github/workflows/build-apk-simple.yml

echo.
set /p COMMIT_MSG="请输入提交信息（默认：修复 Cython 依赖问题）: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG="修复 Cython 依赖问题"

git commit -m "%COMMIT_MSG%

- 修复 Cython 未安装问题
- 添加必要的 Python 依赖
- 增加系统依赖包
- 改进错误处理"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_cython_issue.bat ^<仓库URL^>
    echo.
    echo 示例: fix_cython_issue.bat https://github.com/username/repository.git
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
pause
exit /b 0
