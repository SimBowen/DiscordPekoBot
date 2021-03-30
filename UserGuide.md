---
layout: page
title: User Guide
---
* Table of Contents
{:toc}

# 1. Introduction

Welcome to the User Guide of **NUSMaze**!

**NUSMaze** is a Command Line Interface (CLI) based application that aims to **simplify NUS
Computer Engineering students’ journey** from one point to another within the NUS
Engineering and Computing buildings. The application allows users to find the shortest route
from one block to another, locate the nearest eatery, add personal notes to the location and
many more.

The application uses a Command Line Interface (CLI); this means that you operate the application by typing commands 
into a Command Box. If you are fast at typing, you can operate the application faster than other Graphical User Interface 
(GUI) applications; GUI applications allow users to interact with the application through graphical icons such as buttons.

This user guide will take you through how various features of the NUSMaze can be utilised, all
geared towards providing the best possible experience to the user.

If you are interested, jump to [Section 2 - Quick Start](#2-quick-start) to learn how to start find your way through school with **NUSMaze**.

--------------------------------------------------------------------------------------------------------------------

# 2. Quick start

This section gives you step-by-step instructions on how to download and open the application.

1. Ensure you have Java `11` or above installed in your Computer. You may install it [here](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html). 

2. Download the latest `NUSMaze.jar` [here](https://github.com/AY2021S2-CS2113T-T09-2/tp/releases).

3. Copy the file to the folder you want to use as the _home folder_ **NUSMaze**.

4. Double-click the file to start the app. If you are using Windows, please ensure that your Computer's Display Settings are set to 100%. 

5. A CLI similar to Figure 1 below should appear in a few seconds.  <br><br>
   [img_1.png](img_1.png)
   _Figure 1 - CLI of NUSMAze_
   
6. Type your command into the command box at the bottom of the screen, and press `Enter` on your keyboard to execute it. E.g. typing `help` and pressing `Enter` will open a help window.<br>

7. Refer to [Section 4 - Features](#4-features) for details on the commands you can use for each feature. <br> <br>


--------------------------------------------------------------------------------------------------------------------
# 3. About

## 3.1. Structure of this document

We have structured this User Guide in a way to help you find what you need easily and quickly. 
In the next subsection, [Section 3.2 - reading this document](#32-reading-this-document), you can find several useful tips on how to read this guide.
The following section, [Section 4 - Features](#4-features), documents the seven main features in **Homerce**, namely:

* Client Management

* Service Management

* Appointment Management

* Revenue Tracking

* Expense Tracking

* Schedule Viewing

* Finance Tracking

## 3.2. Reading this document

This section introduces you to some technical terms, symbols and syntax that are used throughout the guide. You may want to
familiarize yourself with them before moving to the next section. 


### 3.2.2. General Symbols and Syntax

The table below explains the general syntax used throughout the user guide.

| Syntax |  What it means |
|----------|-------------|
| `command` |  A grey highlighted block specifies a executable command that can be entered into the command box.  |
| _italics_ | Italicised text indicates that the text has a definition specific to Homerce, or it is a caption for a Figure in the guide. |
|<div markdown="block" class="alert alert-info"> :information_source: </div>  | An exclamation mark indicates that the following text is a tip. |
|<div markdown="block" class="alert alert-danger"> :warning: </div> | A warning sign indicates that the following text is important. |

### 3.2.3. Command Syntax and Usage

The table below explains some important technical terms to help you understand and use commands in NUSMaze.

| Technical Term | What it means |
| ---------------| --------------|
| Command Word | The first word of a command. It determines the action that NUSMaze should perform. |
| Prefix | The characters at the start of a parameter. It distinguishes one parameter from another.|
| Parameter | The word following each prefix. They are values given to a command to perform the specified action.|

**Example:** <br>
`addexp d/DESCRIPTION f/IS_FIXED v/VALUE dt/DATE [t/TAG]`

**Breakdown:** 
* Command Word - `addexp` <br>
* Prefixes - `d/`, `f/`, `v/`, `dt/`, `t/`  <br>
* Parameters - `DESCRIPTION`, `IS_FIXED`, `VALUE`, `DATE`, `TAG`

The following points explain the format of a command. 
More examples will be provided for each command in [Section 4 - Features](#4-features).

1. Words in `UPPER_CASE` are the parameters to be supplied<br>
    - In `deletesvc s/SERVICE_CODE`, `SERVICE_CODE` is a parameter and the command can be used as `deletesvc s/SC001`.

2. Items in square brackets are optional.<br>
    - `v/VALUE [t/TAG]` can be used as `v/15.00 t/equipment` or as `v/15.00`.

3. Items with `…​` after them can be used multiple times, including zero times.<br>
    - `[t/TAG]…​` can be used as ` ` (i.e. 0 times), `t/blacklist`, `t/VIP t/friend` etc.

4. Parameters can be in any order.<br>
    - If the command specifies `d/DESCRIPTION dt/DATE`, `dt/DATE d/DESCRIPTION` is also acceptable.
    
5. A series of parameters in square brackets with asterisks indicate that only exactly one parameter among them should be specified<br>
    - If the command specifies `[t/TITLE]* [s/SERVICE_CODE]*`, `t/nail` is acceptable, but not `t/nail s/sc000` or ` ` (i.e. no parameters).
    
6. If the same parameter is entered multiple times within the same command, only the last entry will be used. (excludes items with `…​` after them in Point #3)
    - If `v/20.00 v/25.00` is entered, the value will be taken as 25.00.
    
<div markdown="block" class="alert alert-info">

**:information_source: Note:**<br>

* Since Homerce is optimized for CLI-based usage, it is recommended to rely purely on CLI commands rather than using a
mouse to navigate between the different managers of Homerce. For example, it is better to do `listapt` rather than clicking
on the appointments tab as `listapt` will sort appointments by chronological order if there are changes made by previous commands.

</div>


# 4. Features

This section contains all the information about the features of **NUSMaze**. 
You may enter a command into the _CLI_ to use each feature.

##4.1 Viewing Help

Lists all commands and functions of each feature.<br>
Format: `help`

## 4.2 Routing

### 4.2.1 Routing between blocks: `go`

Finds the shortest route to go from one block to another.<br>
Format: `go → STARTING_BLOCK → DESTINATION BLOCK`
- When the `go` command is given NUSMaze will prompt you for the `STARTING_BLOCK`
followed by the `DESTINATION BLOCK`.
- Both parameters must be one of the Engineering or Computing buildings.

### 4.2.2 Routing to the closest eatery
It is also possible to find the closest eatery using the go feature.<br>
Format 1: `go → STARTING_BLOCK → EATERY_NAME`
- By entering the name of the eatery that you wish to go in the EATERY_NAME parameter,
  NUSMaze will display the shortest route to go from the STARTING_BLOCK to the
  desired eatery. 
  
Format 2: `go → STARTING_BLOCK → eatery → EATERY_NAME`
- It is also possible to see the list of Eateries, from closest to furthest by entering eatery
  when NUSMaze prompts for the destination block.
   
- When NUSMaze prompts for entry to the eatery, you can enter `EATERY_ENTRY` that you
    wish to go.
  
- `EATERY_ENTRY` must be an integer from 1 to 5.


## 4.3 History
### 4.3.1 Viewing History: `history`

Lists the past 10 route searches.<br>
Format : `history`

### 4.3.2 Clearing History: `clear history`

Deletes all histories (past route searches).<br>
Format : `clear history`

### 4.3.3 Repeating History: `repeat`

Repeats past route search history.<br>
Format : `repeat → REPEAT_ENTRY`
- When the repeat command is entered, NUSMaze will show a list of past route searches.

- Followed by a prompt asking for the `REPEAT_ENTRY` index that you want to repeat.

- `REPEAT_ENTRY` must be an integer number within the numbered list.

## 4.4 Alias
### 4.4.1 Adding an alias for block name: `add alias`
Creates an alias for existing blocks.<br>
Format : `add alias → BLOCK → ALIAS_NAME`
- When add alias command is called, NUSMaze will prompt for the `BLOCK` that you
  wish to set the alias for.
  
- NUSMaze then prompts you to input a desired `ALIAS_NAME`.
  
- Note that there cannot be more than multiple blocks sharing the same alias.

### 4.4.2 Viewing all aliases: `show alias`
Lists all aliases that are currently active.<br>
Format : `show aliase`

### 4.4.3 Deleting aliases: `delete alias`
Deletes an alias that was previously created.<br>
Format : `delete alias → ALIAS_NAME`
- When the `delete alias` command is given, NUSMaze will prompt you for the
  `ALIAS_NAME` that you wish to delete.

## 4.5 Daily Routes
### 4.5.1 Adding a daily route: `add day`
Adds a schedule for the selected day.<br>
Format : `add day → DAY_ENTRY → BLOCK/END`
- You will be prompted to select the `DAY_ENTRY` of the day which you want to schedule.

- `DAY_ENTRY` must be an integer between 1 and 7, each representing a day of the week
  (1 represents Monday and 7 represents Sunday).

- You will then be prompted to enter the location of the activities(`BLOCK`) of the day one at
  a time.
  
- NUSMaze will continuously ask for locations until you input ``.

### 4.5.2 Viewing daily route: `day`
Shows the generated route for the schedule of the selected day, if applicable.<br>
Format : `day → DAY_NUMBER`
- When the day command is entered, the application will display the list of available days
  for which daily routes have been saved.
  
- NUSMaze will then prompt you for a `DAY_NUMBER`.

- The `DAY_NUMBER` must be the index of one of the available days which has been
  displayed.

## 4.6 Notes
### 4.6.1 Adding notes: `add note`
Adds a note about a particular location.<br>
Format : `add note LOCATION/DESCRIPTION`
- When the add note command is given, the application will expect `LOCATION` followed
  by the `/`,and then the `DESCRIPTION` of the note that is to be added.
  
- The `LOCATION` must be one of the Engineering or Computing buildings.

### 4.6.2 Viewing notes: `list notes`
Lists all notes which had been tagged to the given location, if applicable.<br>
Format : `list notes LOCATION`
- The `LOCATION` must be one of the Engineering or Computing buildings.

### 4.6.3 Delete note: `delete note`
Deletes notes based on index number tagged to the given location.<br>
Format : `delete note LOCATION/NOTE_INDEX`
- When the delete note command is entered, the application will expect `LOCATION`
  followed by the / and then the `NOTE_INDEX` of the note that is to be deleted. 
  
- The `LOCATION` must be one of the Engineering or Computing buildings. 
  
- The `NOTE_INDEX` must be an integer within the bounds of the existing note’s indexes for
  that location.

  
## 4.6 Exiting the application: `bye`

Exits the application.<br>
Format: `bye`

#### 4.7 Saving the Data

NUSMaze data is saved in the hard disk automatically after any command that changes the data. There is no need to save manually.

--------------------------------------------------------------------------------------------------------------------

## 5. FAQ

**Q**: Do i lose all my personalised routes and preferences when i close the application? <br>
**A**: Aliases, daily scheduled routes, history and notes are all stored once you exit the app and loaded upon next entry so you do not lose any data.

**Q**: How do I transfer my personalised routes and preferences to another computer? <br>
**A**: Copy the entire data folder that can be found together with the NUSMaze.jar file on the first computer and copy it over to the same directory where the NUSMaze.jar file
can be found on the second computer.



--------------------------------------------------------------------------------------------------------------------

## 6. Glossary

* **Alphanumeric**: Alphanumeric does not include special characters, it only includes letters a to z (uppercase and lowercase) and digits 0 to 9.
* **Special Characters**: Refers to any of the characters within these set of characters: +!#$%&'*+/=?\`{}~^.-&#124;

--------------------------------------------------------------------------------------------------------------------

## 7. Command summary

|Action | Format |
|---------------|------------------------------------------------------------------|
|[**Viewing help**](#41-viewing-help)        | `help` | 
|**Finding the route**       | `go → START → DESTINATION` or `go → START → eatery → EATERY_ENTRY` |
|**Viewing history**     | `history` | 
|**Clearing history**       | `clear history` |
|**Repeating history**       | `repeat → REPEAT_ENTRY` |
|**Adding alias for block names**| `add alias → BLOCK → ALIAS`| 
|**Showing all aliases**  | `show alias` | 
|**Deleting alias**       | `delete alias → ALIAS` |
|**Adding a daily route**     | `add day → DAY_NUMBER → BLOCK → … → BLOCK → END` | 
|**Showing a daily route**       | `day → DAY_NUMBER` |
|**Adding notes**       | `add note LOCATION/DESCRIPTION` |
|**Viewing notes**      | `list notes LOCATION`| 
|**Deleting notes**       | `delete note LOCATION/NOTE INDEX` |
|**Exiting the application**       | `bye` |

