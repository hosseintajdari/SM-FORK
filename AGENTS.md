# SmartTube maintenance

- Start with RUNBOOK.md. Confirm the working tree, branch, origin, and recursive submodule revisions before editing.
- Preserve the Persian subtitle changes in MediaServiceCore and publish a reachable dependency revision before updating its gitlink.
- Use tools/build_test_apk.py; use --checks before handing off or requesting publication. Record build results separately from playback on the TV.
- Keep test signing separate from release signing. Do not copy VPN subscriptions, keys, SDKs, caches, or local paths containing credentials into Git or artifacts.
- Review pending changes before requesting commit/push authorization. Never merge master, add a runner, or start unattended jobs on ct as part of routine maintenance.
