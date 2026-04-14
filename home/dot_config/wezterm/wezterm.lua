local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font 'Hack Nerd Font Mono'
config.font_size = 14.0
config.adjust_window_size_when_changing_font_size = false

config.scrollback_lines = 10000

config.hide_tab_bar_if_only_one_tab = true
config.window_padding = {
  left = 0,
  right = 0,
  top = 0,
  bottom = 0,
}

config.color_scheme = 'Alacritty Default'

-- Define color schemes
config.color_schemes = {
  ['Alacritty Default'] = {
    foreground    = "#d8d8d8",
    background    = "#181818",

    cursor_bg     = "#d8d8d8",
    cursor_fg     = "#181818",
    cursor_border = "#d8d8d8",

    selection_fg  = "#181818",
    selection_bg  = "#d8d8d8",

    ansi = {
      "#181818", -- black
      "#ac4242", -- red
      "#90a959", -- green
      "#f4bf75", -- yellow
      "#6a9fb5", -- blue
      "#aa759f", -- magenta
      "#75b5aa", -- cyan
      "#d8d8d8", -- white
    },

    brights = {
      "#6b6b6b", -- bright black
      "#c55555", -- bright red
      "#aac474", -- bright green
      "#feca88", -- bright yellow
      "#82b8c8", -- bright blue
      "#c28cb8", -- bright magenta
      "#93d3c3", -- bright cyan
      "#f8f8f8", -- bright white
    },

  },
}

config.enable_wayland = false
config.mux_enable_ssh_agent = false
config.term = 'wezterm'

return config
