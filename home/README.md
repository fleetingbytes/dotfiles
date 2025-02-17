# Introduction

Sorry, I still have not written a proper documentation of how dynamic templates work. Here is the concept:

At the very beginning of the `chezmoi apply` procedure, the [template generation script][template-generation-script] `10_generate_dynamic_template.sh` (which itself is a template) is run.
It generates the JSON file `_dynamic/dyn_config.json` (which is ignored by .gitignore).
Almost all template files I use have this line somewhere at the beginning of their content:
```
{{ $dyn := include "_dynamic/dyn_config.json" | mustFromJson -}}
```
This creates a variable `$dyn`, a structured object into which the generated data in `_dynamic/dyn_config.json` file are read.
The following content of the template file somewhere uses a value from the `$dyn` object.

Fox example in my [yt-dlp config][yt-dlp-config], depending on my machine's OS, I use different paths to download videos to.
I don't need to write complex logic statements `{{ if eq .chezmoi.os "..." }} ...` with all the if-branches but instead just
```
{{ $dyn.youtube_downloads | quote }}
```
That's all it needs.
Thanks to the [template generation script][template-generation-script] the `youtube_downloads` key in the `_dynamic/dyn_config.json` contains the correct value to use on the current machine.

The nice thing is that the values in the `_dynamic/dyn_config.json` don't have to change just on some hardware or software based logic but based on pretty much any logic I want at any time I want.
This would be implemented as a configuration profile (or simply "configuration") which can be changed on the fly by me running the script [set-configuration][set-configuration].
This script sets the configuration profile to be used in [.chezmoidata/dynamic_configuration.toml][dynamic-configuration-toml].
By this, chezmoi knows what configuration profile I want to use and exposes this information to the template files in the `{{ .dynconfig }}` datum. (This is viewable by `chezmoi data | grep dynconfig`, or `chezmoi execute-template '{{ .dynconfig }}'`.

Most crucially, the `{{ .dynconfig }}` value is used by the aforementioned [template generation script][template-generation-script].
The value is fed to the Python script [configurator.py][configurator-py] in which all the configuration logic resides.
It is this Python script which actually generates and creates or overwrites the `_dynamic/dyn_config.json` file from which all my templates take the dynamically generated values in the subsequent `chezmoi apply` procedure.

As a showcase of dynamically changing template values, I created three different configuration profiles: [default][default], [other][other], and [special][special]. They contain their respective config name and the greeting phrase by which I want to be greeted when I apply my dotfiles. The [configurator.py][configurator-py] script merges these data into the resulting `_dynamic/dyn_config.json`.
Based on these values, a [MOTD][motd]-like file [greeting][greeting-tmpl] is generated and printed out by the [95-greeting.sh][greeting-sh] script at the end of the `chezmoi apply` procedure.

Thus, the [greeting][greeting-tmpl] file has these possible contents:

default:
```
Hello Sven,
you are using your default dotfiles configuration.
```

other:
```
Greetings, dotfiles user,
you are using your other dotfiles configuration.
```

special:
```
How do you do, fleetingbytes,
you are using your special dotfiles configuration.
```

And it can be switched as I need it by me running the [set-configuration][set-configuration] script.

[configurator-py]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/configurator.py
[default]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/default.json
[dynamic-configuration-toml]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoidata/dynamic_configuration.toml
[greeting-sh]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoiscripts/run_after_95_greeting.sh.tmpl
[greeting-toml]: https://github.com/fleetingbytes/dotfiles/blob/master/home/greeting.tmpl
[motd]: https://en.wikipedia.org/wiki/Message_of_the_day 
[other]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/other.json
[set-configuration]: https://github.com/fleetingbytes/dotfiles/blob/master/home/dot_local/bin/executable_set-configuration
[special]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/special.json
[template-generation-script]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoiscripts/run_before_10_generate_dynamic_template.sh.tmpl
[yt-dlp-config]: https://github.com/fleetingbytes/dotfiles/blob/master/home/dot_config/yt-dlp/config.tmpl
