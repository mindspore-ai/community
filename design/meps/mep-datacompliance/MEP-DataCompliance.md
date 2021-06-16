# MEP-DX: MindSpore Data Compliance SIG

## Table of Contents

<!-- toc -->

- [Summary](#summary)
- [Motivation](#motivation)
- [Goals](#goals)
- [How to join](#how-to-join)

<!-- /toc -->

## Summary

Data is valuable for the purposes of ML and AI when it is organized, labelled and tagged. In fundamental research, standardized datasets are more common, and may be used to train, develop and improve different ML and AI based tools.

According to statistics, 80+ open datasets are used in modelzoo, for example:

- CIFAR-10

- COCO2014 / COCO2017

- YouTube Faces

- Baidu Baike

- ...and other datasets

However, the right to use these datasets remains an open question in many cases. More pragmatically, the following questions need be answered: where is this data coming from? Can it be used for a proposed use-case? Are there any resulting obligations?

Data Compliance SIG aims to find out the risk of license compliance and help developers to use and sharing datasets legally.

## Motivation

- List all the licenses of open datasets used in modelzoo

    If we do not know what license the data have, our use of data creates legal risks.Find out whether the data has a license by looking for the source of the data itself. If there is no license, users are not recommended to use it. For data with a license, we must clearly identify the license and record it onto website.

- Categorize the dataset licenses into rights, obligations and limitations

    From a legal standpoint, depending on the nature of the data, collating and unifying data in databases could arguably have qualified (under certain legal systems) as copyright infringement or database right infringement (for jurisdictions such as the European Union where such a right exists). Without knowledgement of copyright law, people can hardly know which dataset can be used commercially.

    In cooperation with lawyers, we categorize the license clauses, for what we can do we call it rights. For what we have to do, we call it obligations, for what we do with restrictions, we call it a limitations.All analysis results will be output as a risk matrix.

- Build a process to review the risk of license compliance

    After we have a team and rules, we have to set up a process to help our development team use the dataset more easily, some steps we should do before we release a datasets to our community:

    Do the datasets have a license or term of use?

    Which license or term of use do the datasets have?

    Is it non-commercial or research-use-only?

    Give the feedback to the data development team.

- Form a standard license schema to resolve conceptual ambiguities

    As we gradually accumulate experience in data compliance, we will try to form a standard license language to help the entire industry reduce ambiguity. At the right time, we make it a standard.

## Goals

- To list all the datasets used and shared in modelzoo with license.

- To categorize the dataset licenses into rights, obligations and limitations.

- To review the risk of license compliance in MindSpore Community.

- To form a standard license schema to increase transparency and resolve conceptual ambiguities in existing licensing language.

## How To Join：

- Submit an issue/PR based on community discussion for consultation or claim on related topics

## References

- Misha Benjamin, Paul Gagnon, Negar Rostamzadeh, Chris Pal, Yoshua Bengio, Alex Shee, TOWARDS STANDARDIZATION OF DATA LICENSES:THE MONTREAL DATA LICENSE, 21 Mar. 2019.