# All in One 化身天灾 mod

## 概述

这是一个 Stellaris 模组，于 4.1 版本发布，现在游戏已更新至 4.5, 需要更新，并且调整一些模组内容。


## 模组内容

一个游戏原本化身天灾飞升宇宙创生（在游戏本体的项目里一般叫 *cosmogenesis*） 的分支，主要玩法是对宇宙创生的应用无限进行了扩展，根据超然逻辑的产出提供强力 buff.


## 开发习惯

我使用的是 IntellJ 的 Paradox Language Support 插件。

本 mod 的对象会以 "AIO_" 开头，或者类似 "edict_AIO_"、"tech_AIO_" 开头。

复杂的 effect 实现会封装起来放到 `common/scripted_effects` 中。

事件按大类分，例如应用无限 `AIO_AIT_events` 命名，从 201 开始，该事件下我分了随机应用无限和定向应用无限，分别以30、40开头。


## 开发原则

- 如果在修改过程中发现其他地方有明显错误，请直接修复而非使用 wrap 隔离
- 修改过程中如果发现要实现的功能受制于原本的项目结构设计，优先改成优化的结构而非采取隔离、打补丁的方式
- 以优雅简洁清晰的实现优先，不用考虑旧存档兼容问题

总的来说发挥你的主动性和判断力，允许对要求以外的 scope 做出调整，出 bug 了我们继续修。


## 资料

官方 wiki 网站：https://stellaris.paradoxwikis.com/Modding

游戏本体在本机的路径：F:\ProgramFiles\Steam\steamapps\common\Stellaris

日志在：C:\Users\13632\Documents\Paradox Interactive\Stellaris\logs

日志在本机：C:\Users\13632\Documents\Paradox Interactive\Stellaris\logs

