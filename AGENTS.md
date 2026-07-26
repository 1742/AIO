# All in One 化身天灾 mod

## 概述

这是一个 Stellaris 模组，于 4.1 版本发布，现在游戏已更新至 4.4, 需要更新，并且调整一些模组内容。


## 模组内容

一个游戏原本化身天灾飞升宇宙创生（在游戏本体的项目里一般叫 *cosmogenesis*） 的分支，主要玩法是对宇宙创生的应用无限进行了扩展，根据超然逻辑的产出提供强力 buff.


## 开发原则

我使用的是 IntellJ 的 Paradox Language Support 插件。

本 mod 的对象会以 "AIO_" 开头，或者类似 "edict_AIO_"、"tech_AIO_" 开头。

复杂的 effect 实现会封装起来放到 `common/scripted_effects` 中。

事件按大类分，例如应用无限 `AIO_AIT_events` 命名，从 201 开始，该事件下我分了随机应用无限和定向应用无限，分别以30、40开头。


## 资料

官方 wiki 网站：https://stellaris.paradoxwikis.com/Modding

游戏本体在本机的路径：D:\ProgramFiles\Steam\steamapps\common\Stellaris

