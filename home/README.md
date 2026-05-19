# Dynamically Generated Values Used in Templates

At the very beginning of the `chezmoi apply` procedure, the [template generation script][template-generation-script] `10_generate_dynamic_template.sh` (which itself is a template) is run.
It generates the JSON file `_dynamic/dyn_config.json` (which is ignored by .gitignore).
Almost all template files I use read this JSON object at the beginning and provide it as `$dyn`:
```
{{ $dyn := include "_dynamic/dyn_config.json" | mustFromJson -}}
```

The following content of the template file somewhere uses a value from the `$dyn` object.

Fox example, in my [yt-dlp config][yt-dlp-config], depending on my machine's OS, I use different paths to download videos to.
I don't need to write complex logic statements `{{ if eq .chezmoi.os "..." }} ...` with all the if-branches but instead just
```
{{ $dyn.youtube_downloads | quote }}
```
That's all it needs.
Thanks to the [template generation script][template-generation-script] the `youtube_downloads` key in the `_dynamic/dyn_config.json` contains the correct value to use on the current machine.

The nice thing is that the values in the `_dynamic/dyn_config.json` don't have to change just on some hardware or software based logic but can cange based on pretty much any logic I want at any time I want.
This is implemented as a configuration profile (or simply *configuration*) which can be changed on the fly by me running the script [set-configuration][set-configuration].
That script sets the name of the desired configuration profile in [.chezmoidata/dynamic_configuration.toml][dynamic-configuration-toml].
By this, chezmoi knows what configuration profile I want to use and exposes this information to the template files in the `{{ .dynconfig }}` datum. (The user can view the currently set configuration by `chezmoi data | grep dynconfig`, or `chezmoi execute-template '{{ .dynconfig }}'`.)

Most crucially, the `{{ .dynconfig }}` value is used by the aforementioned [template generation script][template-generation-script].
The value is fed to the Python script [configurator.py][configurator-py] in which all the configuration logic resides.
It is this Python script which actually generates and creates or overwrites the `_dynamic/dyn_config.json` file from which all my templates take the dynamically generated values in the subsequent `chezmoi apply` procedure.

As a showcase of dynamically changing template values, I created three different configuration profiles: [default][default], [other][other], and [special][special].
They contain a greeting phrase by which I want to be greeted when I apply my dotfiles, and (redundantly) their respective config name. The [configurator.py][configurator-py] script reads the data of these configuration profiles and could potentially use them in its logic. Currently it plainly merges them into the resulting `_dynamic/dyn_config.json`.
The [MOTD][motd]-like file [greeting][greeting-tmpl] is generated based on the values in `_dynamic/dyn_config.json`. It is printed out by the [95-greeting.sh][greeting-sh] script at the end of the `chezmoi apply` procedure.

Ultimately, the [greeting][greeting-tmpl] file can have any of the following contents:

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

And its content can be switched as I need it by me running the [set-configuration][set-configuration] script. This way I can change a configuration file or even the contents of an executable script by switching my dotfiles configuration.


# Maintaining Sensitive Data in the Templates and Switching Between Work and Home Config

Some config files have sensitive data, either from work environment, or from the home environment. The sensitive data (which may themselves be templates, but ofter are not), reside encrypted as `.age` files in `.chezmoitemplates`.

The configuration files which use them, are templates because they contain instructions which encrypted data/templates to pull in. For example, my carago configuration at work contains some data nobody needs to see. This data lies encrypted in `.chezmoitemplates/.cargo-config.work.toml.age`. By starting the file name with a `.`, chezmoi will automatically ignore it.

The actual cargo config file is then templated in `dot_config/cargo/config.toml.tmpl` and it pulls in the sensitive data by

```
{{ $work_config := joinPath .chezmoi.sourceDir ".chezmoitemplates" ".cargo-config.work.toml.age" | include | decrypt -}}
{{ $work_config | trimAll "\n" -}
```

This all is then part of an if-fork which distinguishes whether this config file should contain data for the work environment or for the home environment:

```
{{ $dyn := include "_dynamic/dyn_config.json" | mustFromJson -}}
{{ if $dyn.at_work -}}
{{ $work_config := joinPath .chezmoi.sourceDir ".chezmoitemplates" ".cargo-config.work.toml.age" | include | decrypt -}}
{{ $work_config | trimAll "\n" -}}
{{ else -}}
# Cargo config for home environment
# Nothing here yet, using default config
{{ end }}
```

Whenever I need the secret or sensitive data in the `.age` files I can use the shell script `edit-encrypted-template` (in `.local/bin`) to list or edit the templates.



[configurator-py]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/configurator.py
[default]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/default.json
[dynamic-configuration-toml]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoidata/dynamic_configuration.toml
[greeting-sh]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoiscripts/run_after_95_greeting.sh.tmpl
[greeting-tmpl]: https://github.com/fleetingbytes/dotfiles/blob/master/home/greeting.tmpl
[motd]: https://en.wikipedia.org/wiki/Message_of_the_day 
[other]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/other.json
[set-configuration]: https://github.com/fleetingbytes/dotfiles/blob/master/home/dot_local/bin/executable_set-configuration
[special]: https://github.com/fleetingbytes/dotfiles/blob/master/home/_dynamic/special.json
[template-generation-script]: https://github.com/fleetingbytes/dotfiles/blob/master/home/.chezmoiscripts/run_before_10_generate_dynamic_template.sh.tmpl
[yt-dlp-config]: https://github.com/fleetingbytes/dotfiles/blob/master/home/dot_config/yt-dlp/config.tmpl
