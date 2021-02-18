# MEP-DX: MindSpore Developer eXperience SIG

## Table of Contents

<!-- toc -->

- [Summary](#summary)
- [Motivation](#motivation)
- [Goals](#goals)
- [How to join](#how-to-join)

<!-- /toc -->

## Summary

DX (Developer eXperience) is what MindSpore community continuously focus on for both contributors and application developers. DX SIG aims to make the community healthy and sustainable,  topics are as follows:

- AI-based user portrait for developer recognition and adoption

- Contributing workflow improvement

    Issue & PR participants recommendation

    Good First Issue recommendation

- Research of Developer relationship model

- Community health metrics and monitoring

## Motivation

- AI-based user portrait for developer recognition and adoption

    At present, more and more developers come from different regions and fields, how to identify talents inside our community and let them release their potential energy is significant. Meanwhile, attracting AI developer or team from outside makes Mindspore more competitive.
    Using developer portrait based on developer interests vector and CNN to reveal the relations among different developers[1], find developers who is suitable and likely to join the community.

- Contributing workflow improvement

    Issue & PR participants recommendation

    The time required to reply is particularly important to the experience of novice developers[2]. However, the allocation of issue participants and PR review requires a lot of work and time for community managers. After training by historic data, tools can assist in recommending suitable developers, it can reduce the cost of community operations.
    By extracting the developer's skills and interest characteristics, integrating the developer's portrait, recommending the most suitable issue participants, and improving the efficiency of issue and PR processing.

    Good First Issue recommendation

    Helping newbie developers to into the community as soon as possible is important for growing the ecosystem. Good First Issue is an industry practice that Github provides easy-to-handle issues for new developers. By Good First Issue, new developers are guided to continue investing in the project due to development thresholds. However, Good First Issue classification is also a time consuming work for developers.
    CNN/RNN/Random Forest algorithm with massive Gitee issue data sets can be used for training the bot to label Good First Issue automatically.

- Research of Developer relationship model

    Developer relationship model is the theoretical basis for building high popularity communities. A high popularity community is one that excels at attracting and retaining members by providing an outstanding member experience. We hope the research can ask the questions like:

    How do I measure community's engagement and growth?

    How do I attract new people to my community?

    What contribution should I ask each community member to make?

- Community health metrics and monitoring

    Nowadays, the importance of open source community is how we understand the health of the open source projects we rely on. Unhealthy projects can have negative impacts. In response, people want to know more about the open source projects they are engaged with. We will cooperate with CHAOSS community of Linux Foundation to implement metrics, practices, and software(like GrimoireLab) for making open source project health more understandable. Our work including:

    Developer contribution statistics

    Issue/PR velocity statistics

    The contributor experience survey(s)

    Other community health statistics

## Goals

- To build user portrait for identifying and attracting core developers in the AI field to contribute to the community.

- To optimize processes, increase automation of issue and PR workflow, improve contribution efficiency.

- To establish a mentor mechanism and recommend good first issue to reduce the threshold for contributors to participate.

- To find a theoretical framework for building high popularity communities and implement metrics and dashboard for community health monitoring.

## How To Join：

- Submit an issue/PR based on community discussion for consultation or claim on related topics

## References

[1] Duo Wang, Jian Cao, Shiyou Qian, Qing Qi, Investigating Cross-Repository Socially Connected Teams on
GitHub, The 26th Asia-Pacific Software Engineering Conference, Putrajaya, Malaysia, 2-5 Dec. 2019.

[2] Yiran Wang, Jian Cao, Well Begun is Half Done: How First RespondenersAffect Issue Resolution Process in
Open Source Software Development? Chinese Conference on Computer Supported Cooperative Work and
Social Computing (ChineseCSCW 2020)， Nov. 7-9, Shenzhen, Accepted
