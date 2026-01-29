@echo off
echo ========================================
echo 添加 APK 位置查找步骤
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加修复的文件...
git add .github/workflows/build-apk.yml

echo.
echo 创建提交...
git commit -m "Add: APK location finder step

- Added 'Find APK Location' step to print .buildozer directory structure
- This will help identify the exact location of generated APK files
- Uses find command to search for all .apk files in .buildozer directory
- Step runs after build and before upload to diagnose path issues"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: add_apk_finder.bat ^<仓库URL^>
    echo.
    echo 示例: add_apk_finder.bat https://github.com/username/repository.git
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
echo [成功] 查找步骤已添加！
echo ========================================
echo.
echo 添加内容：
echo - 在构建步骤后添加了 APK 位置查找步骤
echo - 会打印 .buildozer 目录下的所有 APK 文件
echo - 帮助诊断 APK 的确切位置
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 构建完成后，查看 "Find APK Location" 步骤的输出
echo    这会显示 APK 文件的完整路径
echo.
echo 3. 根据显示的路径，我们可以更新上传配置
echo.
pause
