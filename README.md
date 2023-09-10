# Ulauncher RCE

## Description

Ulauncher v5 is vulnerable to a 1-click remote code execution (RCE)
vulnerability due to:

- A publicly accessible WebSocket API, which can be used from any website
  opened in a browser (since there is no same-origin policy for WebSockets).
- The use of pickle to deserialize data received from the WebSocket API,
  [which can be used to execute arbitrary code during deserialization][1].

## POC

Add `poc.js` to a website and visit it in a browser (no click required).
The [command][2] will be executed on the machine. In this case, it sends a
system notification (using notify-send) and opens the file browser (using
xdg-open).

You can test the POC [here on JSFiddle][3] (only triggered after a click for
convenience).

[![POC Screenshot](./.readme/poc_screenshot.png?raw=true)](https://www.youtube.com/watch?v=llUw-SVjRvQ)

## Limitations

To use the WebSocket API it's required to provide the ID of an extension
currently installed on Ulauncher.
Since a list of extensions is available on [the Ulauncher website][4], it's
possible to try all of them, trying the most popular ones first (most web
browsers throttle WebSocket connections so it can take a some time to try all).
Users who have not installed any extensions are not vulnerable.

The future Ulauncher v6 will not be vulnerable to this issue since it uses unix
sockets.

## Mitigation

The vulnerability can be mitigated by:

- A. Using unix sockets instead of TCP for the WebSocket API.
  This is the best solution and will also mitigate other issues (like
  privilege escalation from local users).

_or_

- B. Checking the Origin header of the WebSocket connection.
  This will prevent the vulnerability from being exploited from a website
  (which is the real threat here).
  However, it will still be possible to exploit the vulnerability locally for
  privilege escalation (already discussed here [Ulauncher issue #456][5]).

The use of pickle wouldn't be an issue if only same-privilege users could use
the WebSocket API.
But it would still be a good idea to use a safer serialization method which
cannot execute code during deserialization (already discussed here
[Ulauncher issue #1032][6]).

## Timeline

- 2023-09-10: Vulnerability discovered.
- 2023-09-10: Vulnerability reported to the Ulauncher team.

## Disclaimer

This POC code is provided for educational and research purposes only.
Use at your own risk.
The author is not responsible for any damages or illegal use of this code.

[1]: https://web.archive.org/web/20230910030644/https://docs.python.org/3/library/pickle.html
[2]: https://github.com/nathan818fr/ulauncher-vulnerability-RCE/blob/main/generate_poc.py#L48
[3]: https://jsfiddle.net/nathan818/9apgorv1/3/
[4]: https://ext.ulauncher.io/
[5]: https://github.com/Ulauncher/Ulauncher/issues/456
[6]: https://github.com/Ulauncher/Ulauncher/issues/1032
