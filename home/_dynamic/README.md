# The heart of dynamic configuration

In the .tmpl files just use this to get access to the dynamic values:

    {{ $dyn := include "_dynamic/dyn_config.json" | mustFromJson -}}

and then you can access a value like this:

    {{ $dyn.some_value }}

but mosly you will need to enclose the value in quotes anyway, like this:

    {{ $dyn.some_value | quote }}

# Windows Gotchas

If a template variable contains a Windows path which is to be used in a PowerShell script, your `$dyn` variable will have it as a string with double backslashes. This will confuse PowerShell, so you also need to replace double backslashes with just a single backslash, e.g.:

    $bootstrap_path = {{ $dyn.bootstrap_path | quote }} -replace "\\\\", "\"
