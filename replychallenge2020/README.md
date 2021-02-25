**Reply Challenge 2020 code and data**

Main file to use is ReplyChallengev3.py, to call in command line with following arguments:

1. -l <"letter"> with letter between a and f, to specify the input file
2. -d <"debug"> with a boolean, default false
3. -s <"simple"> with a boolean, to speficy which algorithms to use (default true)

---

## Init a repo and common errors

To link an empty repo to a directory follow https://confluence.atlassian.com/bitbucketserver/importing-code-from-an-existing-project-776640909.html, section Import code using the terminal

When commiting if you get an error "refusing to merge unrelated histories", first do a git pull origin "branch" --allow-unrelated-histories

When committing after having added new files not tracked do "git add ." tp add all untracked files and then commit

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).