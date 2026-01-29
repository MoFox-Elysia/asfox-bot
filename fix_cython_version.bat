@echo off
echo ========================================
echo 修复 Cython 版本问题
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
git commit -m "Fix: Force install Cython 0.29.33 for Pyjnius compatibility

- Changed to install Cython==0.29.33 specifically
- Newer Cython versions (>=3.0) reject Python 2 syntax in Pyjnius
- Pyjnius source code still uses 'long' keyword (Python 2)
- Cython 0.29.33 tolerates this syntax and allows compilation
- This fixes the 'undeclared name not builtin: long' error
- This is the most effective solution for Buildozer on GitHub Actions"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_cython_version.bat ^<仓库URL^>
    echo.
    echo 示例: fix_cython_version.bat https://github.com/username/repository.git
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
echo [成功] Cython 版本修复已推送！
echo ========================================
echo.
echo 修复内容：
echo - 强制安装 Cython 0.29.33 版本
echo - 解决了 Pyjnius 编译时的 'long' 关键字错误
echo - 新版 Cython 不兼容 Pyjnius 的 Python 2 语法
echo - Cython 0.29.33 是 Buildozer 的最佳兼容版本
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 查看 "Build APK with Buildozer" 步骤
echo    Pyjnius 应该能够成功编译
echo.
echo 3. 查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 4. 在 Artifacts 部分下载 APK
echo.
pause
