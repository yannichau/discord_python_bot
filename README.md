# discord_python_bot

Discord is far more than an online social networking tool. The platform allows developers to create a wide variety of bots, allowing them and to bring a range of interactive activities to users' chats, and inhale a bit of life in an otherwise passive networking platform. Oddly, despite the widespread use of python for data science, very few python discord bot developers (or none, from observation) have attempted to create some some sort of discord bot that takes advantage of its python's beautifully simple data sciennce packages, such as Pandas.

This project is an attempt to wrap a couple "excel-like" functions into a python-scripted discord bot. At the moment it is relatively primitive, and it merely includes a couple file operation and column/row manipulation commands. At the moment, I can forsee it being a scoreboard tool on discord. Hopefully it will find its way into something more than this!

# Walkthrough

# Commands

Currently, to differentiate commands from regular messages, all commands must be accessed with a `^` prefix. The additional arguments required are specified in `[brackets]`. In addition, always use "double quotes"

## File Operation

    ^close       [filename]
        close and save the currently opened table.

    ^create      [filename] [col names]
        create a new table, specifying the table name as well as the column names.

    ^list        
        returns all available tables on my computer!

    ^open        [filename]
        open a table, specifying its name.

    ^print       [filename]
        print a table, specifying its name.

    ^save        [filename]
        save a table, specifying its name.
        note: the table is saved when ^closed or manipulated with commands in the next section.

## Dataframe Manipulation (Based on Pandas)

The following commands can only be run when a table is in appending mode. Or in other words run these commands after an `^open` or `^create` operation.

    ^append      [row name] [values]
        append one new row, specifying the row name, and values of all cells in the row.

    ^appendcol   [cols]
        append empty new column(s), specifying the name(s) for them

    ^appendtotal append total of column to bottom row
        same as ^total, except doing so appends the row of totals to the table.

    ^drop        [rows]
        delete rows, specifying the names of the row(s) to be removed.

    ^dropcol     [cols]
        delete cols, specifying the names of the columns(s) to be removed.

    ^sel         [rows]
        temporarily view selected rows by specifying their names.

    ^selcol      [cols]
        temporarily view selected columns by specifying their names.

    ^total       
        temporarily view the sum of every single cell for each column.

## General useless commands

There's not much going on here. I normally run them just to check that the bot is actually running.

    ^version     
        check version of clueless-bot. forever at version 0!

    ^ping        [your crazy thoughts]
        pong your crazy thoughts
