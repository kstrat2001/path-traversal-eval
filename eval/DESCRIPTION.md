# A file name that walks out of its folder

An app stores files in one folder and lets users name the file they want: a download link, an upload, a delete button. If the app joins that name onto the folder without checking where the result lands, a name like `../../etc/passwd` walks up and out. Security people call this path traversal. It hides well because the obvious attack is easy to block, and the real escapes come through the side doors: a decoded `%2e`, a symlink, a folder whose name starts the same way, or the file names inside an uploaded archive.

## Real-world incidents

- **Zip Slip, June 2018.** Snyk found that code unpacking archives often trusted member names like `../../evil.sh`, so uploading a crafted zip or tar wrote files anywhere on the server. They found it in libraries across many ecosystems and in thousands of projects ([Snyk](https://snyk.io/blog/behind-the-disclosure-the-zip-slip-vulnerability/)).
- **Apache HTTP Server 2.4.49, October 2021.** URL-encoded dots in a request got past the traversal check, letting attackers read files outside the web root, and with CGI enabled run code. It was exploited in the wild within days, and the first fix was incomplete (CVE-2021-41773, then CVE-2021-42013; [Rapid7](https://www.rapid7.com/blog/post/2021/10/06/apache-http-server-cve-2021-41773-exploited-in-the-wild/)).
- **Jupyter Server, June 2026.** The root-folder check compared paths as strings with `startswith(root)`, so a sibling folder whose name began with the root's name passed it (CVE-2026-5422; [GitLab advisory](https://advisories.gitlab.com/pypi/jupyter-server/CVE-2026-5422/)).

## How the eval shows a model knows the fix

The model reviews a storage module that already blocks these escapes and has only happy-path tests. The grader then plants one bug at a time: one operation skips the check, archive members are joined without checking, half an archive is written before a bad member is refused, the check compares strings instead of path components, or symlinks are not resolved. A model's tests pass only if they try each escape and go red on every one.

Results claim only that a model's tests caught these planted bugs, not that any code or model is secure.
