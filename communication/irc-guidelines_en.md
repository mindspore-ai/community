## IRC guidelines

### Brief

MindSpore community holds its various public meetings on **[IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat)**, in the following channels:

* #mindspore-discuss
* #mindspore-sc

on Freenode. Everyone is encouraged to attend, [Connect to IRC via webclient](https://webchat.freenode.net/?randomnick=1&channels=%23mindspore-discuss%2C%23mindspore-sc&prompt=1&uio=d4)

webclient recommended:

* [freenode-chat](https://webchat.freenode.net/)
* [irccloud](https://www.irccloud.com/)

IRC channels and logged. You can find all channels and all logs here:
[IRC Channel Logs](http://meeting.mindspore.cn/)

### Use Case

The meeting channel can be managed by meeting chair with bot command, which is used by # prefix character. The basic commands are shown below:

#startmeeting - (chair) Start the meeting on channel. the meeting topic should be given on the rest. e.g. ``#startmeeting infra``
#topic - (chair) - (chair) Start a topic on channel to make sure all partners focus on a special topic.
#endmeeting - (chair) End the whole meeting.

For more other commands, please step into next section.

### Commands

All commands are case-insensitive, and use the ``#`` prefix character. Not all commands have output. The commands are.

#startmeeting

Start a meeting. The calling nick becomes the chair. If any text is given on the rest of the line, this becomes the meeting topic.

#endmeeting

End a meeting, save logs, restore previous topic, give links to logs. You know the drill.  (Chairs  only.)

#topic

Set  the  current  topic  of  discussion, the rest of the line will become the topic, change the topic in the channel (saving  the  original  topic  to  be  restored  at  the  end  of the  meeting).  (Chairs  only.)

#agreed  (alias  #agree)

Mark something as agreed on. The rest of the line is the details. (Chairs  only.) All the rest text will be recorded by system after the meeting end.

#chair  and  #unchair

Add new chairs to the meeting. The rest of the line is a list of nicks, separated by commas and/or spaces. The nick which started the meeting is the  ``owner`` and can't be de-chaired. The command replies with a list of the current chairs, for verification (Chairs only.)  Example::
```
<freesky-edward>  #chair MrGreen MsAlizarin
<mindspore-ci-bot>  Current chairs are: freesky-edward MsAlizarin MrGreen
```
#action

Add an ``ACTION`` item to the minutes. Provide irc nicks of people involved, and will be both a complete listing of action items, and a listing of action items sorted by nick at the end of the meeting. This is very useful for making sure this gets done.  Example::

```
<freesky-edward>  #action MrGreen will read the entire Internet to determine why the hive cluster is under attack.
```

#info

Add an ``INFO`` item to the minutes. Example::

```
<freesky-edward>  #info We need much effort before the next release.
```

#link

Add a link to the minutes. The URL will be properly detected within the line in most cases - the URL can't contain spaces. This command is automatically detected if the line starts with http:, https:. Examples::

```
<freesky-edward>  #link  [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/)  is  the  main  page
<freesky-edward>  [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/)  is  the  main  page
<freesky-edward>  #link  the  main  page  is  [http://wiki.debian.org/MeetBot/](http://wiki.debian.org/MeetBot/)
so go there
```
