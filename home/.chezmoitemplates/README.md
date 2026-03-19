# Crontab Reference

By "crontab reference" I mean the kind of file you'd use as a named file for crontab(1) to read and install.
`.crontab.age` is an encrypted template of a crontab reference. It is used by the `crontab-ref` shell script in ~/.local/bin

## Usage

```sh
crontab-ref show          # prints decrypted crontab reference (rendered template)
crontab-ref edit          # decrypt → edit → re-encrypt the crontab reference
crontab-ref apply         # alias for `crontab-ref show | crontab -`,
                          # a one-shot install of the crontab reference from my dotfiles
```
