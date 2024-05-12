# Dotfiles

These are my dotfiles, managed by [chezmoi][chezmoi]. The special thing about them is that they utilize a dynamic configuration. While chezmoi enables me to use templates and variables, the dynamic configuration enables me to set the values of these variables dynamically. With that, I don't need if-statements in the template files and I can change the content of my templated files by running my `set-configuration` script. See [detailed description][home-readme]

- [home][home] contains user configurations that are automatically installed in  the home directory
- [system][system] contains system-wide configurations that cannot or should not be installed automatically


# Acknowledgements

Many thanks to [adamchristiansen][adam] for showing me how to make [dynamic templates][dynamic-templates] in chezmoi and how to use chezmoi smartly.

[chezmoi]: https://chezmoi.io
[home]: https://github.com/fleetingbytes/dotfiles/blob/master/home
[home-readme]: https://github.com/fleetingbytes/dotfiles/blob/master/home/README.md
[system]: https://github.com/fleetingbytes/dotfiles/blob/master/system
[adam]: https://github.com/adamchristiansen
[dynamic-templates]: https://github.com/twpayne/chezmoi/issues/1342
