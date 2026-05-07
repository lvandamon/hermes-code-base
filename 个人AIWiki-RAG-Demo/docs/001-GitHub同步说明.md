# GitHub 同步说明

## 一、同步目标

`~/Documents/Hermes代码库/` 是用户后续代码项目的统一根目录，远端同步到：

```text
git@github-code:lvandamon/hermes-code-base.git
```

对应 GitHub 页面：

```text
https://github.com/lvandamon/hermes-code-base
```

## 二、自动同步

系统 crontab 已添加：

```text
*/30 * * * * /home/agentuser/.hermes/scripts/git-autosync.sh /home/agentuser/Documents/Hermes代码库
```

该任务每 30 分钟检查一次：

1. 如果有本地改动，自动 `git add -A && git commit`。
2. 拉取远端 `main` 分支。
3. 根据本地/远端关系执行 fast-forward、push 或 rebase 后 push。

## 三、手动同步

重要改动完成后建议立即执行：

```bash
cd ~/Documents/Hermes代码库
git status --short
git add -A
git commit -m "chore: 初始化个人 AI Wiki RAG Demo"
git push -u origin main
```

如果没有新改动，可以只执行：

```bash
git push origin main
```

## 四、注意事项

- 本目录保存代码和 Demo，不替代 `~/Documents/Hermes资料库/` 的中文知识资料库。
- `~/Documents/Hermes资料库/` 继续同步到 `hermes-knowledge-base`。
- `~/.hermes/` 继续同步到 Hermes 配置仓库。
- 本代码库不要提前创建空项目；有真实 Demo 或脚本时再新增子项目。
