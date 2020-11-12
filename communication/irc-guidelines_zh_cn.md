## IRC指引

### 简要介绍
MindSpore社区在**[IRC](https://zh.wikipedia.org/wiki/IRC)**举行相关的会议，频道有：

* #mindspore-discuss
* #mindspore-sc

在Freenode上，每个人都鼓励去参与，[连接到webclient](https://webchat.freenode.net/?randomnick=1&channels=%23mindspore-discuss%2C%23mindspore-sc&prompt=1&uio=d4)

webclient推荐：

* [freenode-chat](https://webchat.freenode.net/)
* [irccloud](https://www.irccloud.com/)

IRC频道与日志，您可以在这里找到所有的频道和记录[IRC Channel Logs](http://meeting.mindspore.cn/)

### 用户场景
会议主持者能通过bot命令管理会议频道，命令是采用`#作为前缀的字符，常用的命令有：

#startmeeting - (主持人) 开始一个会议，命令后面需要跟随一个会议的主题。例如：`#startmeeting infra`

#topic - (主持人) 开始一个议题讨论，命令后面的字符就是该议题的简要描述。例如：`#topic next release time`

#endmeeting -(主持人)结束当前的会议。

### 命令
所有的命令使用`#`字符前缀，但是并不是所有命令系统都有响应输出，具体的单个命令集有：

#startmeeting

开始一个会议，键入这个命令的人将成为该会议的主持人，命令后面的文字将成为该会议的主题。

#endmeeting

结束当前的会议，系统会记录会议日志，并给出相应的会议纪要地址。

#topic

设置当前会议的讨论主题，命令后面的文字将成为议题主题，当前会议结束后，系统将在会议记录中高亮会议主题以方便查看。

#agreed (alias #agree)

表示与会人达成一定的结论，命令行后面即是结论内容。会议结束后，系统将在会议结论中记录该结论。

#chair and #unchair

用于增加或者移除会议主持人，命令后跟IRC的昵称，开始会议的人将是会议的所有者，在会议过程中是不能被移除，命令将对执行结果给出回应信息，例如：
```
<freesky-edward>  #chair  MrGreen  MsAlizarin
<mindspore-ci-bot> Current  chairs  are: freesky-edward MsAlizarin MrGreen
```

#action

用于记录会议讨论后下一步需要某人采取的动作，命令后面的第一串字符表示动作的执行人，后续文字将是对动作的描述，待会议结束后，会议纪要将把该后续动作记录下来。命令样例：
```
<freesky-edward>  #action MrGreen 查找整个网络了解为啥集群受到攻击。
```

#info

用于在会议记录中高亮显示一个记录，例如：
```
<freesky-edward>  #info 在下一个版本发布前，我们还有很多工作需要做。
```

#link

用于添加一个网络连接，命令后即是该连接的地址，连接不能有空格，如果敲入的文字以http或者https开头，系统会默认执行该命令，例如：
```
<freesky-edward> #link [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/) 是主页
<freesky-edward> [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/) 是主页
<freesky-edward> #link the main page is [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/)
浏览这里
```
